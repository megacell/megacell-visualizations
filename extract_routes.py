'''
This script extracts route geometry
'''

import json
from pdb import set_trace as T

extract_sql = '''
select geom from experiment2_routes where orig_taz=22294000;
'''


def execute(cur, filename):
    cur = conn.cursor()
    cu


if __name__ == "__main__":
    main()
