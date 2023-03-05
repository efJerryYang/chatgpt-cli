from datetime import datetime
import json
from typing import Dict, List
import os
from rich import print


def get_main_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_dir() -> str:
    return os.path.join(get_main_dir(), "data")


def save_data(data: List[Dict[str, str]], filename: str) -> None:
    """Save list of dict to JSON file"""

    data_dir = get_data_dir()
    print("Data Directory: ", data_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if filename.endswith(".json"):
        filepath = os.path.join(data_dir, filename)
    else:
        filepath = os.path.join(data_dir, filename + ".json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")


def load_data(messages: List[Dict[str, str]]) -> str:
    """Load JSON file from 'data' directory to 'messages', and return the filepath"""

    data_dir = get_data_dir()
    print("Data Directory: ", data_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    if not files:
        print("No data files found in 'data' directory")
        return ""

    # prompt user to select a file to load
    print("Available data files:\n")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    for a in range(3):
        selected_file = input(
            f"\nEnter file number to load (1-{len(files)}), or Enter to start a fresh one: "
        )
        if not selected_file.strip():
            return ""
        try:
            index = int(selected_file) - 1
            if not 0 <= index < len(files):
                raise ValueError()
            filepath = os.path.join(data_dir, files[index])
            with open(filepath, "r") as f:
                data = json.load(f)
                messages.clear()
                messages.extend(data)
            print(f"Data loaded from {filepath}")
            return filepath
        except (ValueError, IndexError):
            print("Invalid input, please try again")
    print("Too many invalid inputs, aborting")
    exit(1)
