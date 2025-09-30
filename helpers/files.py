from pathlib import Path
import logging
import json
import yaml
from ruamel.yaml import YAML
from helpers import ubuntu


LOGGER = logging.getLogger(__name__)


def create_dummy_file(filename: str, ssh_host=None, empty=True, random=True, size=0):
    """Creates a dummy file.
    Args:
        filename (str): The complete filename, with path and extension
        empty (bool, optional): If the file should be empty. Defaults to True.
        random (bool, optional): If it should be filled with random characters. Defaults to True.
        size (int, optional): Size in KB. Defaults to 0.
    """
    if size < 0:
        raise ValueError("Size can't be lower than 0!")
    if empty and size != 0:
        raise ValueError("If empty, size need to be 0!")
    if not empty and size == 0:
        raise ValueError("Size can't be 0 if not empty!")
    if not empty and not random:
        raise AttributeError("Can't handle this case yet - TO DO")

    assert ubuntu.is_execute_cmd_successful_remote(
        f"head -c {size}KB /dev/urandom > {filename}", ssh=ssh_host
    ), "Can't create dummy file"


def update_yml_file(src_file_path, key_path, dst_file_path=None, **kwarg):
    """Update Yaml file key value of key_path referred nested block
    Args:
        src_file_path (str): Source file path of YAML file to be modified
        key_path (str): Key path up to the block to be modified, where path key separated by '.'
        dst_file_path (str): Destination file path of YAML file to be save
        kwarg: key value pair have to be modified.
    """
    yml = YAML()
    yml.preserve_quotes = True
    if not dst_file_path:
        dst_file_path = "temp/docker-compose.yaml"
    with open(src_file_path) as f:
        data = yml.load(f)
    accessible = data
    for k in key_path.split("."):
        accessible = accessible[k]
    for k, v in kwarg.items():
        accessible[k.upper()] = v
    with open(dst_file_path, "w") as f:
        yml.dump(data, f)


def parametrize(file_and_key: str) -> list:
    """Returns a proper list of parameters for the parametrize method of Pytest
    Args:
        file_and_key (str): The file and key separated by a colon
    Returns:
        list: The list of constants/parameters
    """
    filename, key = file_and_key.split(":")

    # Prepend the default directory to the filename
    filename = f"constants/{filename}"

    # Auto detect if it's a YAML or JSON file
    if Path(f"{filename}.yml").exists() or (Path(filename).exists() and filename.endswith(".yml")):
        # It's a YAML file
        with open(f'{filename.rstrip(".yml")}.yml', "r") as file:
            constants = yaml.safe_load(file)

    elif Path(f"{filename}.json").exists() or (
        Path(filename).exists() and filename.endswith(".json")
    ):
        # It's a JSON file
        with open(f'{filename.rstrip(".json")}.json', "r") as file:
            constants = json.load(file)
    else:
        # Could not find the specified file
        raise FileNotFoundError
    return constants[key]
