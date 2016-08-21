from utils import *
from django.contrib.gis.geos import Point, Polygon
from pdb import set_trace as T
from collections import namedtuple
import shapefile

from extract_links import get_links

CELLPATHS_FILE = '../data/cells/cells_voronoi.shp'
OUTFILE = 'web/data/cellpaths{}.geojson'
COMPARE_FILE = '../../megacell/set_lsh/compare.json'
IN_SRID = 32611
OUT_SRID = 4326
Cell = namedtuple('Cell', ['id', 'center', 'voronoi'])

def import_paths(filename):
    reader = shapefile.Reader(filename)
    records = reader.iterRecords()
    shapes = reader.iterShapes()

    cells = {}
    for record, shape in zip(records, shapes):
        id, x, y = record
        point = Point(x, y, srid=IN_SRID)
        point.transform(OUT_SRID)
        poly = Polygon(map(tuple, shape.points), srid=IN_SRID)
        poly.transform(OUT_SRID)
        cells[id] = Cell(id, point, poly)
    return cells

def cells_to_fc(cells):
    fc = FeatureCollection()
    for cell in cells.values():
        fc.add(cell.center.json, {'id': cell.id})
        fc.add(cell.voronoi.json, {'id': cell.id})
    return fc

if __name__ == '__main__':
    cells = import_paths(CELLPATHS_FILE)
    link_geom = get_links()
    fc = cells_to_fc(cells)
    compare = json.load(open(COMPARE_FILE))[:40]
    for i, datum in enumerate(compare):
        newfc = fc.deepcopy()
        for c in datum['sstem_path']:
            newfc.add(cells[c].voronoi.json, {'color': 'rgba(255, 0, 0, 0.5)'})
        for c in datum['lsh']:
            newfc.add(cells[c].voronoi.json, {'color': 'rgba(0, 255, 0, 0.5)'})
        for l_id in datum['trajectory']:
            newfc.add(link_geom[l_id], {})
        newfc.dump(OUTFILE.format(str(i)))
