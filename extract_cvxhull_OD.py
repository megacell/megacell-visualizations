'''
This script extracts the geometry of each TAZ as a convex hull of routes
starting in it, grouped by each TAZ id.

We can get the start/end points from either trajectories or routes, they should
give the same result
'''

import json
from pdb import set_trace as T
from utils import *

drop_tables_sql = '''
DROP TABLE IF EXISTS tmp_orig_taz;
DROP TABLE IF EXISTS tmp_dest_taz;
'''

od_trajectory_tables_sql = '''
-- Set of start points of every trajectory from each orig_taz
CREATE TEMPORARY TABLE tmp_orig_taz (points, id) AS
SELECT ST_Collect(ST_StartPoint(l.geom)), t.orig_taz
FROM experiment2_trajectories AS t, link_geometry AS l
WHERE t.link_ids[1]=l.link_id
GROUP BY t.orig_taz;

-- Set of end points of every trajectory to each dest_taz
CREATE TEMPORARY TABLE tmp_dest_taz (points, id) AS
SELECT ST_Collect(ST_EndPoint(l.geom)), t.dest_taz
FROM experiment2_trajectories AS t, link_geometry AS l
WHERE t.link_ids[array_length(t.link_ids, 1)]=l.link_id
GROUP BY t.dest_taz;
'''

od_route_tables_sql = '''
-- Set of start points of every route from each orig_taz
CREATE TEMPORARY TABLE tmp_orig_taz (points, id) AS
SELECT ST_Collect(start_point), orig_taz
FROM experiment2_routes
GROUP BY orig_taz;

-- Set of end points of every route to each dest_taz
CREATE TEMPORARY TABLE tmp_dest_taz (points, id) AS
SELECT ST_Collect(end_point), dest_taz
FROM experiment2_routes
GROUP BY dest_taz;
'''

select_sql = '''
-- Convex hull of points in each TAZ
SELECT ST_AsGeoJSON(ST_ConvexHull(ST_Collect(o.points, d.points))), o.id
FROM tmp_orig_taz AS o, tmp_dest_taz AS d
WHERE o.id = d.id;
'''

def execute(conn, outfile, routes=True):
    cur = conn.cursor()
    cur.execute(drop_tables_sql)
    if routes:
        cur.execute(od_route_tables_sql)
    else:
        cur.execute(od_trajectory_tables_sql)
    cur.execute(select_sql)

    fc = FeatureCollection()
    for polygon, taz_id in cur.fetchall():
        fc.add(json.loads(polygon), {'taz_id': int(taz_id)})
    fc.dump(open(outfile, 'w'))

@cache('web/data/od_geom.pkl')
def get_od_geom():
    cur = get_conn().cursor()
    cur.execute(drop_tables_sql)
    cur.execute(od_trajectory_tables_sql)
    cur.execute(select_sql)
    data = {int(taz_id): json.loads(polygon) for polygon, taz_id in cur.fetchall()}
    return data

if __name__ == "__main__":
    execute(get_conn(), 'web/data/od_route_polygons.geojson', routes=True)
    execute(get_conn(), 'web/data/od_trajectory_polygons.geojson', routes=False)
