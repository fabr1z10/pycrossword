import yaml

class Configuration():
    def __init__(self):
        with open('config.yaml') as stream:
            try:
                cf = yaml.safe_load(stream)
                self.schema_file = cf['schema_file']
                self.dictionary_file = cf['dictionary_file']
            except yaml.YAMLError as exc:
                print(exc)