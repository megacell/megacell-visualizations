'''
This script extracts the geometry of each TAZ
'''

import json
from pdb import set_trace as T
from utils import *

select_sql = '''
SELECT ST_AsGeoJSON(geom), taz_id
FROM taz_geometry;
'''

@cache('web/data/od_geom.pkl')
def get_od_geom():
    cur = get_conn().cursor()
    cur.execute(select_sql)
    data = {int(taz_id): json.loads(polygon) for polygon, taz_id in cur.fetchall()}
    return data

def get_od_geojson():
    fc = FeatureCollection()
    for taz_id, geom in get_od_geom().items():
        fc.add(geom, {'taz_id':  taz_id})
    fc.dump(open('web/data/od_geom.geojson', 'w'))

if __name__ == "__main__":
    get_od_geom(refresh=True)
    get_od_geojson()
