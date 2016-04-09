__author__ = 'tobchen'

from model import Scene


def get_paths(path_obj: str) -> (str, str, str):
    if path_obj.lower()[-4:] != ".obj":
        path_obj += ".obj"
    path_mtl = path_obj[:-4] + ".mtl"
    path_data = path_obj[:-4] + "_data"
    return path_obj, path_mtl, path_data


def save(path_obj: str, path_mtl: str, path_data: str, scene: Scene):
    

    # TODO Yeah, obviously
    pass
