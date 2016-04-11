__author__ = 'tobchen'

from model import *
from zipfile import ZipFile
from xml.etree import ElementTree
from PIL import Image
from io import BytesIO


def read(path: str) -> Scene:
    zipfile = ZipFile(path, 'r')

    # Read stack
    stack_file = zipfile.open('stack.xml', 'r')
    stack_content = stack_file.read()
    stack_file.close()

    # Image tag
    stack_root = ElementTree.fromstring(stack_content)
    if stack_root.tag != "image" or not "w" in stack_root.attrib\
            or not "h" in stack_root.attrib:
        return None
    width = stack_root.attrib["w"]
    height = stack_root.attrib["h"]

    # TODO type hint list return
    def get_imagelayers(x: int, y: int, tag: ElementTree.Element) -> list:
        layers = list()

        if "x" in tag.attrib:
            x += int(tag.attrib["x"])
        if "y" in tag.attrib:
            y += int(tag.attrib["y"])

        if tag.tag == "layer":
            name = ""
            if "name" in tag.attrib:
                name = tag.attrib["name"]

            image = None
            if "src" in tag.attrib:
                image = Image.open(BytesIO(zipfile.read(tag.attrib["src"])))

            if image:
                layers.append(ImageLayer(name, x, y, image))

        elif tag.tag == "stack":
            for child in tag:
                layers.extend(get_imagelayers(x, y, child))

        return layers

    imagelayers = get_imagelayers(0, 0, stack_root.find("stack"))
    for i in range(0, len(imagelayers)):
        if imagelayers[i].get_name() == "":
            imagelayers[i].set_name("Layer " + str(i))

    scene = Scene(width, height)
    for layer in imagelayers:
        scene.add_layer(layer)

    return scene
