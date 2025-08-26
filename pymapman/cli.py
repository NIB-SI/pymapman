#!/usr/bin/env python3

from pathlib import Path
import click
from pymapman import diagram_from_svg

@click.group()
def cli():
    """Top-level CLI entrypoint."""
    pass

@cli.command()
@click.argument("svg_in_fp", type=click.Path(exists=True, path_type=Path))
@click.option("--base-fn", type=str, default=None, help="Base filename for outputs (default: SVG stem)")
@click.option("--output-dir", type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path), default=None, help="Output directory (default: same as input SVG)")
@click.option("--recursive-default", type=str, default="true", show_default=True, help="Default recursive attribute")
@click.option("--visualizationtype-default", type=str, default="1", show_default=True, help="Default visualizationType")
def from_svg(svg_in_fp: Path, base_fn: str | None, output_dir: Path | None, recursive_default: str, visualizationtype_default: str):
    """Convert an SVG file into a cleaned SVG and MapMan XML coordinate file."""
    svg_out_fp, xml_fp = diagram_from_svg(
        svg_in_fp,
        base_fn=base_fn,
        output_dir=output_dir,
        recursive_default=recursive_default,
        visualizationType_default=visualizationtype_default,
    )
    click.echo(f"Written background SVG: {svg_out_fp}")
    click.echo(f"Written associated XML: {xml_fp}")

if __name__ == '__main__':
    cli()
