from pathlib import Path
from lxml import etree as ET
from datetime import datetime
import re

class MapManNode():
    def __init__(self, gmm, x, y, recursive, visualizationType):
        self.gmm = gmm
        self.x = x
        self.y = y
        self.visualizationType = visualizationType
        self.recursive = recursive

def create_diagram_xml(xml_fp: Path, base_fn: str, width: float, height: float, nodes: list):
    """Write MapMan XML coordinate file."""
    root = ET.Element(
        "Image",
        image=base_fn,
        size=f"{width:.0f}x{height:.0f}",
        modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scaling="1.0",
    )

    for node in nodes:
        data_area = ET.SubElement(
            root,
            "DataArea",
            x=f"{node.x:.0f}",
            y=f"{node.y:.0f}",
            visualizationType=node.visualizationType,
        )
        ET.SubElement(
            data_area,
            "Identifier",
            id=node.gmm,
            recursive=node.recursive,
        )

    tree = ET.ElementTree(root)
    tree.write(str(xml_fp), pretty_print=True, xml_declaration=True, encoding="UTF-8")

def diagram_from_svg(
    svg_in_fp: Path,
    base_fn: str | None = None,
    output_dir: Path | None = None,
    recursive_default: str = "true",
    visualizationType_default: str = "1",
) -> tuple[Path, Path]:
    """
    Convert an input SVG into a "MapMan diagram" consisting of a cleaned background SVG and a associated XML file.

    Returns
    -------
    svg_out_fp, xml_fp : Path
        Paths to the written output files.
    """
    # prepare paths

    if output_dir is None:
        output_dir = svg_in_fp.parent
    if base_fn is None:
        base_fn = f"{svg_in_fp.stem}-mm"

    svg_out_fp = output_dir / f"{base_fn}.svg"
    xml_fp = output_dir / f"{base_fn}.xml"

     # print all input parameters
    print(f"Input SVG: {svg_in_fp}")
    print(f"Output background SVG: {svg_out_fp}")
    print(f"Output MapMan XML: {xml_fp}")
    print(f"Default recursive: {recursive_default}")
    print(f"Default visualizationType: {visualizationType_default}")

    # print date and time now
    print(f"Processing started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # parse SVG
    tree = ET.parse(str(svg_in_fp))
    root = tree.getroot()
    width, height = float(root.get("width")), float(root.get("height"))

    # extract bins and coordinates, and remove nodes
    nodes = []
    for n in list(tree.iter()):
        id_ = n.attrib.get("id")
        if id_ and (match := re.match(r"^gmm\:([0-9]+(?:\.[0-9]+)*)$", id_)):
            gmm = match[1]
            x, y = float(n.attrib.get("x")), float(n.attrib.get("y"))
            recursive = n.attrib.get("mm_recursive", recursive_default)
            visualizationType = n.attrib.get("mm_visualizationType", visualizationType_default)
            nodes.append(MapManNode(gmm, x, y, recursive, visualizationType))

            # remove node to clear background in image
            parent = n.getparent()
            if parent is not None:
                parent.remove(n)

    # save cleaned SVG
    tree.write(str(svg_out_fp), pretty_print=True, xml_declaration=True, encoding="UTF-8")

    # write MapMan coordinates XML
    create_diagram_xml(xml_fp, base_fn, width, height, nodes)

    # print date and time now
    print(f"Processing finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return svg_out_fp, xml_fp
