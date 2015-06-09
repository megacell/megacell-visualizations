'''
This script extracts the solver results and calculates the link flow errors
'''

import json
import pickle
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

config = { 'num_routes': 30
         , 'density': 1
         , 'outmat': 'solver_output/1/output_waypoints30.mat'
         , 'outfile': 'web/data/results_error.geojson'
         }

def get_link_dict():
    ''' Return a dictionary mapping all link ids to 0
    '''
    return {link: 0 for link in get_links().keys()}

def get_all_flows(output_mat):
    ''' Returns CONTROL, a dictionary mapping each link id to route flow through
    that link based on CONFIG as defined at beginning of this file, as well as
    RESULTS, a dictionary mapping each link id to the link flows computed by the 
    solver.
    '''
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(route_loader_sql, config)
    
    out_mat = sio.loadmat(output_mat)
    x = np.squeeze(out_mat['orig_x'])

    control = get_link_dict()
    results = get_link_dict()
    
    x_index = 0
    for link_seq, flow in cur:
        for link_id in link_seq:
            control[link_id] += flow
            results[link_id] += flow * x[x_index]
        x_index += 1

    assert len(x) == x_index, "Solver output num routes: {}, Matrix num routes: {}".format(len(x), x_index)

    return control, results

def main():
    control_links, results_links = pickle.load(open('control_links.pkl')), pickle.load(open('results_links.pkl')) #get_all_flows(config['outmat'])

    fc = FeatureCollection()
    links = get_links()

    for link_id, geom in links.items():
        control, result = control_links[link_id], results_links[link_id]
        difference = abs(float(control - result)) / control if control != 0 else 0
        fc.add(geom, {'weight': difference})

    fc.dump(open(config['outfile'], 'w'))
        
if __name__ == '__main__':
    main()
    
