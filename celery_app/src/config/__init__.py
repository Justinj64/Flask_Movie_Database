import os
import json


def get_config(config_names):
    '''
        will check for config .json file in the /config folder
        for eg. if the config file is named development.json, set the `env=development`
        all config parameters will be loaded onto the app context
    '''
    configs = config_names.split()
    config_data = dict()
    for config_name in configs:
        config_file = ".".join([config_name.lower(), "json"])
        config_file_path = os.path.join(os.path.dirname(__file__), config_file)

        if not os.path.exists(config_file_path):
            raise FileNotFoundError("{}.json configuration file do not exist in `config` directory.".format(config_name))

        with open(config_file_path) as file:
            config_data.update(json.loads(file.read()))

    return config_data
