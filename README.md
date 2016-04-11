# Layered Polygons

## Introduction
*Layered Polygons* is a Python 3 program that loads a layered image file for
defining polygons per layer. Those polygons can then be exported as 3d models.

## Manual
### Menu
- **File**
  - **New...** Open a layered image file to work on
  - **Open...** Open a Layered Polygon file
  - **Save (As...)** Save as a Layered Polygon file
  - **Export As** Export as a 3d model
  - **Quit** Quit program

### Supported File Formats
*Layered Polygons* currently imports OpenRaster images as layered images and
exports Wavefront Object files (together with material files).

### Work Flow
After opening a layered image choose a layer in the list box.

To define a polygon start and continue left-clicking on the canvas to place
vertices. Finish the polygon by left-clicking on the first vertex. If you
left-click near enough to an existing vertex (of another polygon) the polygon
will use *it* instead of creating a new one. Cancel a polygon in progress by
right-clicking on the canvas. If the polygon is supposed to be greater than the
current view port the scroll bars can be used without breaking anything.

To delete a polygon when not in polygon creation mode right-click on it.

Finally export the layered polygons as a 3d model.

## Layered Polygons File Format (.lp)
*Layered Polygons* writes and reads the *Layered Polygons File Format (.lp)*.
An .lp file is a ZIP file containing a *data.json* and one image file per
layer. The *data.json* is structured as follows:
```javascript
{
  "width": Integer, // scene's width
  "height": Integer, // scene's height
  "layers": // array of scene's layers (optional, default: empty)
    [
      {
        "name": String, // layer's name (optional, default: "Layer <index>")
        "x": Integer, // layer's image's x offset
        "y": Integer, // layer's image's y offset
        "image": String, // path to layer's image in ZIP file
        "vertices": // array of layer's vertices (optional, default: empty)
          [
            {
              "x": Integer, // vertex's x coordinate
              "y": Integer // vertex's y coordinate
            },
            ...
          ],
        "polygons": // array of layer's polygons (optional, default: empty)
          [
            [
              Integer, // vertex index from "vertices" array
              ...
            ],
            ...
          ]
      },
      ...
    ]
}
```

## Applications
### Motion Comics
*Layered Polygons* can be used to easily polygonify elements in comic book
panels to then be animated in a 3d software. (Example videos to follow.)
