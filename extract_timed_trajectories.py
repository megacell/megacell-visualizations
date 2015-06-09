'''
Extracts a small number of trajectories and simulates them as timeslices
'''

import json
from pdb import set_trace as T
from django.contrib.gis.geos import LineString
from math import log

from utils import *
from extract_links import get_flows, get_links

# This is the value used for ISTTT experients, see route_loader in experiment 2
COMMUTE_DIRECTION = 0
NUM_AGENTS = 5000
SPEED = 15 # Meters per second
DT    = 10 # Seconds

trajectories_sql = '''
SELECT link_ids
FROM experiment2_trajectories
WHERE commute_direction=%s
LIMIT %s;
'''

class Agent:
    def __init__(self, links):
        self.links = links
        self.link_counter = 0

    def step(self, time):
        cur_link = self.links[self.link_counter]
        if self.link_counter == len(self.links) - 1 and \
           cur_link.cur_dist == cur_link.total_dist:
           return None
        remaining = cur_link.move(time)
        while remaining > 0 and self.link_counter < len(self.links) - 1:
            self.link_counter += 1
            remaining = self.links[self.link_counter].move(remaining)
        return self.links[self.link_counter].get_position()

class Link:
    def __init__(self, geom, speed):
        self.line = LineString(geom['coordinates'], srid=4326)
        self.line.transform(32611)
        self.speed = speed
        self.cur_dist = 0
        self.total_dist = self.line.length

    def move(self, dt):
        distance = self.speed * dt
        overshot = distance + self.cur_dist - self.total_dist
        if overshot > 0:
            self.cur_dist = self.total_dist
            return float(overshot) / self.speed
        else:
            self.cur_dist += distance
            return 0

    def get_position(self):
        pt = self.line.interpolate(self.cur_dist)
        pt.transform(3857)
        return list(pt)

def execute(conn, outfile, routes=True):
    cur = conn.cursor()
    link_geoms = get_links()
    link_flows = get_flows()

    def link_speed(link_id):
        flow = link_flows[link_id]
        return SPEED - log(flow) / 2

    cur.execute(trajectories_sql, (COMMUTE_DIRECTION, NUM_AGENTS))
    agent_steps = []
    for (links, ) in cur:
        a = Agent([Link(link_geoms[l], link_speed(l)) for l in links])

        steps = []
        pos = a.step(DT)
        while pos:
            steps.append(pos)
            pos = a.step(DT)
        agent_steps.append(steps)

    json.dump(agent_steps, open(outfile, 'w'))

if __name__ == '__main__':
    execute(get_conn(), 'web/data/timed_trajectories.json', routes=True)
