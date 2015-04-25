'''
This script extracts the geometry of each TAZ as a convex hull of routes
starting in it, grouped by each TAZ id.
'''

import psycopg2
import sys
import json
from pdb import set_trace as T

od_tables_sql = '''
-- Set of start points of every trajectory from each orig_taz
CREATE TEMPORARY TABLE origin_taz (points, id) AS
SELECT ST_Collect(ST_StartPoint(l.geom)), t.orig_taz
FROM experiment2_trajectories AS t, link_geometry AS l
WHERE t.link_ids[1]=l.link_id
GROUP BY t.orig_taz;

-- Set of end points of every trajectory to each dest_taz
CREATE TEMPORARY TABLE dest_taz (points, id) AS
SELECT ST_Collect(ST_EndPoint(l.geom)), t.dest_taz
FROM experiment2_trajectories AS t, link_geometry AS l
WHERE t.link_ids[array_length(t.link_ids, 1)]=l.link_id
GROUP BY t.dest_taz;
'''

select_sql = '''
-- Convex hull of points in each TAZ
SELECT ST_AsGeoJSON(ST_ConvexHull(ST_Collect(o.points, d.points))), o.id
FROM origin_taz AS o, dest_taz AS d
WHERE o.id = d.id;
'''

def make_feature_collection(features):
    return {'type': 'FeatureCollection',
            'features': features}

def make_feature(geom, props):
    return {'type': 'Feature',
            'geometry': geom,
            'properties': props}

def main():
    conn = psycopg2.connect(database='geodjango', user='megacell')
    cur = conn.cursor()
    try:
        cur.execute(od_tables_sql)
        cur.execute(select_sql)
        feature_list = [make_feature(json.loads(polygon),
                                     {'taz_id': int(taz_id)})
                        for polygon, taz_id in cur.fetchall()]
        feature_collection = make_feature_collection(feature_list)
        json.dump(feature_collection, open('data/od_polygons.geojson', 'w'))
    finally:
        conn.close()

if __name__ == "__main__":
    main()
