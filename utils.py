import os.path
import psycopg2
import pickle
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

    def dump(self, file_name):
        json.dump(self.export(), open(file_name, 'wb'))

    def add(self, geom, props):
        self.features.append({'type': 'Feature',
                              'geometry': geom,
                              'properties': props})

def gyr_cmap(N):
    cmap = plt.get_cmap('RdYlGn')
    return lambda x: '#{:02x}{:02x}{:02x}'.format(*cmap(((N-x) * 256)/N, bytes=True))

def cache(cache_file):
    def wrap(f):
        def cached(*args, **kwargs):
            if not os.path.isfile(cache_file) or kwargs.get('refresh'):
                res = f(*args)
                pickle.dump(res, open(cache_file, 'wb'))
            else:
                res = pickle.load(open(cache_file))
            return res
        return cached
    return wrap

def get_conn():
    return psycopg2.connect(database='geodjango', user='megacell')

def get_scale(max_val):
    return lambda x: float(x) / max_val
