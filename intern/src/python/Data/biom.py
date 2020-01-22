import yaml


class Biom:
    def __init__(self, name, atmospheric_diffusion, atmospheric_absorption, cloud_reflection,
                 avg_rainfall_per_day, groundwater):
        self.name = name
        # this value corresponds to the diffuse sun beam scattering by the atmosphere
        self.atmospheric_diffusion = atmospheric_diffusion  # in percent
        self.atmospheric_absorption = atmospheric_absorption  # in percent
        self.cloud_reflection = cloud_reflection  # in percent
        self.avg_rainfall_per_day = avg_rainfall_per_day  # in l/cm²
        self.groundwater = groundwater  # in l/cm²

    def save_biom(self):
        data = {self.name: {
            'atmospheric_diffusion': self.atmospheric_diffusion,
            'atmospheric_absorption': self.atmospheric_absorption,
            'cloud_reflection': self.cloud_reflection,
            'avg_rainfall_per_day': self.avg_rainfall_per_day,
            'groundwater': self.groundwater}
        }

        with open('resources/data/bioms.yml', 'a') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
