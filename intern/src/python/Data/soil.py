import yaml


class Soil:
    def __init__(self, id, name, albedo, water_absorption):
        self.id = id
        self.name = name
        self.albedo = albedo
        self.water_absorption = water_absorption

    def save_soil(self):
        data = {self.name: {
            'id': self.id,
            'albedo': self.albedo,
            'water_absorption': self.water_absorption }
        }

        with open('resources/data/soil_types.yml', 'a') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
