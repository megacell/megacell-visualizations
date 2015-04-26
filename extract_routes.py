'''
This script extracts route geometry
'''

import json

from pdb import set_trace as T
from utils import FeatureCollection, gyr_cmap

routes_sql = '''
SELECT ST_AsGeoJSON(geom), flow_count
FROM experiment2_routes
WHERE orig_taz=%s;
'''
OD_sql = '''
SELECT ST_AsGeoJSON(ST_ConvexHull(ST_Collect(start_point)))
FROM experiment2_routes
WHERE orig_taz=%s;
'''

ORIGIN_ID = 21107000

def execute(conn, outfile):

    cur = conn.cursor()
    fc = FeatureCollection()
    cmap = gyr_cmap(100)

    cur.execute(routes_sql, (ORIGIN_ID,))
    all_data = cur.fetchall()
    for geom, flow_count in all_data:
        fc.add(json.loads(geom), {'stroke': cmap(flow_count)})

    cur.execute(OD_sql, (ORIGIN_ID,))
    fc.add(json.loads(cur.fetchone()[0]), {})

    fc.dump(open(outfile, 'w'))

if __name__ == "__main__":
    main()
