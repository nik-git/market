import os
from pathlib import Path
import json

this_file_path = Path(os.path.abspath(__file__))


def get_dict_from_json_file(dir_name, json_file_name):
    """
    read the json file under data dir.
    :param json_file_name:
    :param dir_name :
    :return:
    """
    file_path = os.path.join(this_file_path.parent, '..', dir_name, json_file_name)
    with open(file_path, 'r') as fp:
        return json.load(fp)


def write_dict_into_json_file(dir_name, json_file_name, data_dict):
    """
    Write dict into Json file.
    :param dir_name:
    :param json_file_name:
    :param data_dict:
    :return:
    """
    file_path = os.path.join(this_file_path.parent, '..', dir_name, json_file_name)
    with open(file_path, 'w') as fp:
        json.dump(data_dict, fp, indent=4, sort_keys=True)