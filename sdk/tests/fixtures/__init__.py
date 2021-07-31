import json
import os


def get_fixture(fixture_file_name):
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, fixture_file_name), "r+") as f:
        return json.load(f)
