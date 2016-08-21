"""
Extract true link flows
"""
import psycopg2
import json
import csv
from collections import defaultdict

from utils import *

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
    ''' Returns LINKCOUNTS, a dictionary mapping link ids to trajectory flows
    through each link.
    '''
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
    ''' Returns LINKS, a dictionary of all links mapping link ids to link
    geometry in geojson form.
    '''
    conn = psycopg2.connect(database='geodjango', user='megacell')
    cur = conn.cursor()
    cur.execute(LINKS_SQL)

    links = {}
    for (link_id, geom) in cur:
        links[link_id] = json.loads(geom)
    return links

def get_link_attrs():
    reader = csv.DictReader(open('links.csv'))
    return {int(line['ID']): line for line in reader}

def execute(outfile):
    fc = FeatureCollection()
    for link_id, geom in get_links().items():
        fc.add(geom, {'id': link_id})
    fc.dump(outfile)

if __name__ == '__main__':
    execute('web/data/links.geojson')
