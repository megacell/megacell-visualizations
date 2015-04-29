"""
Extract true link flows
"""

import psycopg2
import json
from collections import defaultdict

from utils import cache

# This is the value used for ISTTT experients, see route_loader in experiment 2
COMMUTE_DIRECTION = 0
FLOWS_FILE = 'web/data/link_flows.pkl'
LINKS_FILE = 'web/data/links.pkl'

TRAJECTORIES_SQL = '''
SELECT link_ids
FROM experiment2_trajectories
WHERE commute_direction=%s;
'''

LINKS_SQL = '''
SELECT link_id, ST_AsGeoJSON(geom)
FROM link_geometry;
'''

@cache(FLOWS_FILE)
def get_flows():
    conn = psycopg2.connect(database='geodjango', user='megacell')
    cur = conn.cursor()
    cur.execute(TRAJECTORIES_SQL, (COMMUTE_DIRECTION, ))
    linkcounts = defaultdict(int)
    for (link_ids, ) in cur:
        for id in link_ids:
            linkcounts[id] += 1
    return linkcounts

@cache(LINKS_FILE)
def get_links():
    conn = psycopg2.connect(database='geodjango', user='megacell')
    cur = conn.cursor()
    cur.execute(LINKS_SQL)

    links = {}
    for (link_id, geom) in cur:
        links[link_id] = json.loads(geom)
    return links
