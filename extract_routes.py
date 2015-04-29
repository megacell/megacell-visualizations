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

od_routes_sql = '''
SELECT ST_AsGeoJSON(geom), flow_count
FROM experiment2_routes
WHERE orig_taz=%s and dest_taz=%s;
'''

OD_sql = '''
SELECT ST_AsGeoJSON(ST_ConvexHull(ST_Collect({0}_point)))
FROM experiment2_routes
WHERE {1}_taz=%s;
'''
orig_sql = OD_sql.format('start','orig')
dest_sql = OD_sql.format('end','dest')

ORIG_ID = 22113000 # 21107000
DEST_ID = 22091000

def execute(conn, outfile):

    cur = conn.cursor()
    fc = FeatureCollection()
    cmap = gyr_cmap(100)

    #cur.execute(routes_sql, (ORIG_ID,))
    cur.execute(od_routes_sql, (ORIG_ID, DEST_ID))
    all_data = cur.fetchall()
    for geom, flow_count in all_data:
        fc.add(json.loads(geom), {'stroke': cmap(flow_count)})

    cur.execute(orig_sql, (ORIG_ID,))
    fc.add(json.loads(cur.fetchone()[0]), {})
    cur.execute(dest_sql, (DEST_ID,))
    fc.add(json.loads(cur.fetchone()[0]), {})

    fc.dump(open(outfile, 'w'))

if __name__ == "__main__":
    main()
