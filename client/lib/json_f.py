import json


def load_config(dir):
        with open(dir, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        return json_data
