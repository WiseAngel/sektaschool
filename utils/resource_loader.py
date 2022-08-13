import json
import os


def get_environment_resource(resource_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root_path, "resources", "environment", resource_name)
    with open(path) as f:
        result = json.load(f)
    return result


def get_path_environment_resource(file_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root_path, "resources", "environment", file_name)
    return path


def get_path_static_resource(file_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root_path, "resources", "static", file_name)
    return path


def get_static_resource(file_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root_path, "resources", "static", file_name)
    return open(path, "rb")


def get_test_data(resource_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    resource_dirs = resource_name.split(".")
    resource_dirs[-1] = f"{resource_dirs[-1]}.json"
    path = os.path.join(root_path, "resources", "test_data", *resource_dirs)
    with open(path) as f:
        result = json.load(f)
    return result


def get_test_data_non_local(resource_name: str):
    root_path = os.path.dirname(os.path.dirname(__file__))
    resource_dirs = resource_name.split(".")
    resource_dirs[-1] = f"{resource_dirs[-1]}.json"
    path = os.path.join(root_path, "resources", "test_data", *resource_dirs)
    with open(path) as f:
        result = json.load(f)
    return result
