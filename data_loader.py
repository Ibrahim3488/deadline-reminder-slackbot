import json


def load_json_file(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"{file_name} file not found")
        return []

    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_name}")
        return []