from os import close, path
from pathlib import Path


def create_file(path_dir: str, file_name: str, content: str, obsidian: bool = True) -> str:

    print("-"*40)
    print(f"path: {path_dir}, name: {file_name}")
    print("-"*40)

    if obsidian:
        # path_dir = OBSIDIAN_PATH
        path_dir = ("/home/raulzada/Obsidian/Zada/")

    with open(f"{path_dir}{file_name}", "a", encoding="UTF-8") as file:
        file.write(content) 

    return "File generated with success!"

def next_function():
    pass
