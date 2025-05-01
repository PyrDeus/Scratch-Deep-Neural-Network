###
# utils.py
# Contains utility classes and functions
# 

from enum import Enum
import random

import pandas as pd
from pathlib import Path
from typing import List

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GRAY = (128, 128, 128)
    LIME = (0, 255, 0)
    OLIVE = (128, 128, 0)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    MAROON = (128, 0, 0)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)
    BACKGROUND = 245

def extractMonitorDimensions() -> tuple[int, int]:
    from screeninfo import get_monitors

    # Get screen resolution
    monitor = get_monitors()[0]

    return monitor.width, monitor.height

def listFiles(dir_path, extension=".csv"):
    p = Path(dir_path)
    if not p.exists() or not p.is_dir():
        raise Exception
    files = list(sorted(Path(dir_path).glob(f"*{extension}")))
    return files

def askFile(dir_path, name="file", extension=".csv"):
    print(f"Which {name} do you want to load?")

    files = listFiles(dir_path, extension)
    if len(files) == 0:
        print(f"There is no {name} saved in this directory.\nContinue process.")

    while True:
        for i, f in enumerate(files):
            print(f"\t{i+1}:\t{str(f.stem)}")

        response = input()
        try:
            index = int(response)
            if 0 < index <= len(files):
                print(f"{name} \"{files[index - 1]}\" selected.")
                return files[index - 1]
            print(f"\nThe listing ends at {len(files)}. Choose a valid listed file in:")
        except:
            for index, f in enumerate(files):
                if response == f.stem:
                    print(f"{name} \"{files[index]}\" selected.")
                    return files[index]
            print(f"\nThe {name} {response} is not valid. Choose a valid listed file in:")


def askLevelFile():
    dir_path = "../levels"
    file = askFile(dir_path, name="level", extension=".csv")
    return file

def askWeightFile():
    response = input("Do you want weights? ")
    if response.lower() in ["yes", "y", "1", "true"]:
        dir_path = "../weights"
        file = askFile(dir_path, name="weights", extension=".w8")
        return file

def askNewLevelFile():
    dir_path = "../levels"
    name = "level"
    extension = ".csv"
    files = listFiles(dir_path, extension=extension)

    response = input("Which name du you want? ")

    while True:
        end = True
        for i, f in enumerate(files):
            if response != f.stem:
                continue
            end = False
            previous_response = response
            print(f"\nThe {name} \"{dir_path}/{response}{extension}\" already exists. Retype it if you want to write on it or type a valid name not in:\n\t{[f.stem for f in files]}")
            response = input()
            if response == previous_response: end = True
            break
        if end:
            print(f"{name} \"{dir_path}/{response}{extension}\" selected.")
            return f"{dir_path}/{response}{extension}"


def saveCSVLayout(filename, shape_df: pd.DataFrame, overwrite=True):
    p = Path(filename)
    if overwrite or not p.exists():
        shape_df.to_csv(p, index=False)
        return 1
    return 0

def loadCSVLayout(filename) -> pd.DataFrame:
    shape_df: pd.DataFrame = None
    p = Path(filename)
    if p.exists() and p.is_file() and p.suffix == ".csv":
        shape_df = pd.read_csv(p)
        return shape_df
    return shape_df
