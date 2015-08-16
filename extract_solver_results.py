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

config = { 'num_routes': 30
         , 'density': 1
         , 'outmat': 'solver_output/1/output_waypoints30.mat'
         , 'err_file': 'web/data/results_error.geojson'
         , 'linkcounts_file': 'web/data/results_links.geojson'
         , 'control_links' : 'web/data/control_links.pkl'
         , 'results_links' : 'web/data/results_links.pkl'
         }

# SQL needed to load individual routes
route_loader_sql = """
SELECT r.links, r.flow_count
FROM experiment2_routes r
JOIN experiment2_waypoint_od_bins w
ON r.od_route_index = w.od_route_index AND r.orig_taz = w.origin AND r.dest_taz = w.destination
WHERE r.od_route_index < %(num_routes)s AND w.density_id = %(density)s
ORDER BY w.waypoints, r.orig_taz, r.dest_taz, r.od_route_index;
"""

# Load sensors
SENSORS_SQL = '''
select ST_AsGeoJSON(location) from orm_sensor s;
'''

def get_sensors_json():
    cur = get_conn().cursor()
    cur.execute(SENSORS_SQL)
    return [json.loads(l[0]) for l in cur]

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
    control_links = pickle.load(open(config['control_links']))
    results_links = pickle.load(open(config['results_links']))

    fc = FeatureCollection()
    links = get_links()

    for link_id, geom in links.items():
        control, result = control_links[link_id], results_links[link_id]
        if control != 0:
            difference = abs(float(control - result)) / control * 6
            params = {'weight': difference, 'link_id': link_id}
        else:
            params = {}
        fc.add(geom, params)

    fc.dump(config['err_file'])

    lc = FeatureCollection()
    max_link = max(control_links.values())

    for link_id, geom in links.items():
        lc.add(geom, {'weight': control_links[link_id] * 1.0 / max_link,
                      'link_id': link_id})

    for sensor_geom in get_sensors_json():
        lc.add(sensor_geom, {'sensor': True})

    lc.dump(config['linkcounts_file'])

if __name__ == '__main__':
    main()
