'''
This script extracts the solver results and calculates the link flow errors
'''

import json
import numpy as np
import scipy.io as sio
from pdb import set_trace as T

from utils import *
from extract_links import get_links

# SQL needed to load individual routes
route_loader_sql = """
SELECT r.links, r.flow_count
FROM experiment2_routes r
JOIN experiment2_waypoint_od_bins w
ON r.od_route_index = w.od_route_index AND r.orig_taz = w.origin AND r.dest_taz = w.destination
WHERE r.od_route_index < %(num_routes)s AND w.density_id = %(density)s
ORDER BY w.waypoints, r.orig_taz, r.dest_taz, r.od_route_index;
"""

config = { 'num_routes': 10
         , 'density': 950
         , 'outmat': 'solver_output/950/output_waypoints10.mat'
         }

def get_link_dict():
    ''' Return a dictionary mapping all link ids to 0
    '''
    return {link: 0 for link in get_links().keys()}

def get_control_flows():
    ''' Returns LINKS, a dictionary mapping each link id to route flow through
    that link based on CONFIG as defined at beginning of this file. Also returns
    ROUTES, a list remembering the order of routes that are put into the
    experiment matrices.
    '''
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(route_loader_sql, config)

    links = get_link_dict()
    routes = cur.fetchall()

    for link_seq, flow in routes:
        for link_id in link_seq:
            links[link_id] += flow

    return links, routes

def get_experiment_link_flows(routes, output_mat, outfile):
    ''' Returns LINKS, a dictionary mapping each link id to the link flows
    computed by the solver.
    '''
    out_mat = sio.loadmat(output_mat)
    x = np.squeeze(out_mat['orig_x'])
    T()
    assert len(x) == len(routes), "Number of routes doesn't match!"

    links = get_link_dict()
    for scale, (link_seq, flow) in zip(x, routes):
        for link_id in link_seq:
            links[link_id] += flow * scale

if __name__ == '__main__':
    control_links, routes = get_control_flows()
    result_links = get_experiment_link_flows(
                     routes
                   , config['outmat']
                   , 'web/data/results_error.geojson')
    T()
