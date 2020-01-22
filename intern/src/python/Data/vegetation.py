import yaml


class Vegetation:
    def __init__(self, name, energy_demand, water_demand, soil_demand, soil_depth_demand):
        self.name = name
        self.energy_demand = energy_demand
        self.water_demand = water_demand
        self.soil_demand = soil_demand
        self.soil_depth_demand = soil_depth_demand

    def save_vegetation(self):
        data = {self.name: {
            'energy_demand': self.energy_demand,
            'water_demand': self.water_demand,
            'soil_demand': self.soil_demand,
            'soil_depth_demand': self.soil_depth_demand }
        }

        with open('resources/data/vegetation_types.yml', 'a') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
