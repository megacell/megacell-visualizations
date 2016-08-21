'''
This script extracts routes that flow through a link.

If a link is blocked, show the routes that flows through it, as well as the
percentage of drivers in each origin TAZ affected by the blockage.
'''

import json
from pdb import set_trace as T
from collections import defaultdict

from utils import *
from extract_links import get_flows, get_links
from extract_OD import get_od_geom

NUM_ROUTES = 10
LINK_ID = 739#1051#6734#
PERCENT_THRESHOLD = 0.05
FLOW_THRESHOLD = 5


routes_sql = '''
SELECT flow_count, ST_AsGeoJSON(geom)
FROM experiment2_routes
WHERE orig_taz=%s and od_route_index < %s;
'''

od_count_sql = '''
SELECT sum(flow_count), {0}_taz
FROM experiment2_routes
WHERE od_route_index < %s
GROUP BY {0}_taz;
'''

orig_count_sql = od_count_sql.format('orig')
dest_count_sql = od_count_sql.format('dest')

od_blocked_sql = '''
SELECT flow_count, orig_taz, ST_AsGeoJSON(geom)
FROM experiment2_routes
WHERE od_route_index < %s AND links @> array[%s];
'''

def execute(conn, outfile):
    cur = conn.cursor()
    fc = FeatureCollection()

    fc.add({'type': 'Point',
            'coordinates': get_links()[LINK_ID]['coordinates'][0]}, {})

    total_counts = {}
    cur.execute(orig_count_sql, (NUM_ROUTES, ))
    for count, taz_id in cur:
        total_counts[taz_id] = count

    blocked_counts = defaultdict(int)
    cur.execute(od_blocked_sql, (NUM_ROUTES, LINK_ID))
    results = sorted(cur.fetchall())
    scale = get_scale(results[-1][0]) # max flow

    for flow_count, orig_taz, route_geom in results:
        if flow_count > FLOW_THRESHOLD:
            fc.add(json.loads(route_geom), {'weight': scale(flow_count)})
        blocked_counts[orig_taz] += flow_count

    print len(fc.features)

    percents = []
    for taz_id, od_geom in get_od_geom().items():
        if taz_id not in total_counts or blocked_counts[taz_id] == 0:
            continue
        percent = float(blocked_counts[taz_id]) / total_counts[taz_id]
        if percent <= PERCENT_THRESHOLD:
            continue
        percents.append(percent)
        fc.add(od_geom, {'weight': percent})

    print len(fc.features)
    fc.dump(outfile)

if __name__ == "__main__":
    execute(get_conn(), 'web/data/routes_through_link.geojson')
