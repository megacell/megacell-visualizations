import json
import matplotlib.pyplot as plt

class FeatureCollection:
    def __init__(self):
        self.features = []

    def __str__(self):
        json.dumps(self.export())

    def export(self):
        return {'type': 'FeatureCollection',
                'features': self.features}

    def dump(self, file_ob):
        json.dump(self.export(), file_ob)

    def add(self, geom, props):
        self.features.append({'type': 'Feature',
                              'geometry': geom,
                              'properties': props})

def gyr_cmap(N):
    cmap = plt.get_cmap('RdYlGn')
    return lambda x: '#{:02x}{:02x}{:02x}'.format(*cmap(((N-x) * 256)/N, bytes=True))
