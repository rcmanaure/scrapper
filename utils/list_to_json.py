# Python program to store list to JSON file
import json


def write_list(a_list: list, file_name: str):
    """
    Save the list of responses in a json file.
    """
    print("Started writing list data into a json file")
    with open(f"scrap_files/{file_name}.json", "w") as fp:
        json.dump(a_list, fp)
        print("Done writing JSON data into .json file")


def read_list(file_name: str) -> list:
    """Read list to memory"""
    # for reading also binary mode is important
    print("Started reading list data")
    with open(f"scrap_files/{file_name}.json", "rb") as fp:
        n_list = json.load(fp)
        return n_list
