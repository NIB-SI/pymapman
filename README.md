# pymapman
Python tool to help create MapMan diagrams

## Background

[MapMan](https://www.plabipd.de/mapman_main.html) is a GUI application that can overlay large datasets (e.g. gene expression) onto biological pathway diagrams. Each diagram consists
of a background image (e.g. SVG, PNG) and an associated XML file that defines  points on the image and the annotation for each point. Given a background image, the XML file mapping annotations to points on the background image can be manually created in the MapMan application, but this can be tedious, especially for large images with many annotations.

This python tool helps automate the creation of MapMan diagrams files from a SVG file, so that the background and annotations can be created in a single step. 

The input SVG is created in a SVG editing tool, such as Inkscape. The locations of the annotated points on the image are defined by including additional SVG elements with the appropriate annotation as the element ID. `pymapman` can then create the background image and associated XML file from the SVG file.

## Installation

You can install pymapman from GitHub via pip:

```bash
pip install "pymapman @ git+git@github.com:NIB-SI/pymapman.git"
```

## Usage

The main command line tool is `pymapman from-svg`. You can see the available options by running:

```bash
pymapman from-svg --help
```

The basic usage is:

```bash
pymapman from-svg <input SVG diagram> [options]

```

For example, to create a MapMan diagram from an SVG file called `stress_responses-inkscape.svg` (see the example image [here](resources/input_diagrams), you can run:

```bash
pymapman from-svg stress_responses-inkscape.svg --base-fn stress_responses-mm --output-dir .
```

This will create two files: `stress_responses-mm.svg` (the background image) and `stress_responses-mm.xml` (the associated XML file). As long as they have the same base name, MapMan will recognize them as a pair when loading the background image as a new Pathway diagram.

### Creating the input SVG file

The input SVG file should contain elements with IDs corresponding to the annotations you want to include in the MapMan diagram. For example, if you want to annotate a point with the MapMan annotation 20.2 (`stress.abiotic`), you can create a rectangle element in the SVG file like this:

```xml
<rect id="mm:20.2" x="100" y="100" r="5" fill="red" />
```

You can use any SVG elements, as long as they have `x` and `y` (or `cx` and `cy`) attributes (e.g. `circle`, `rect`, `ellipse`, etc.), and an ID corresponding to a MapMan annotation.

Here is an example of annotating such an ID in Inkscape:

![Inkscape example](docs/inkscape_rec-id.png)

`pymapman` will extract the position of the element (`x` and `y` in this case), __remove__ the element from the SVG to create a "clean" background image, and use the extracted position to create the XML file. 
