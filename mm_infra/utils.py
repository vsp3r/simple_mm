import json
import os


def config_parse(config_file):
    current_dir = os.path.dirname(__file__)

    config_path = os.path.join(os.path.dirname(current_dir), config_file)
    with open(config_path) as f:
        return json.load(f)

def auth_parse(auth_file):
    current_dir = os.path.dirname(__file__)

    auth_path = os.path.join(os.path.dirname(current_dir), auth_file)
    with open(auth_path) as f:
        return json.load(f)

