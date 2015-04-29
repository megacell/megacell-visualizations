import psycopg2

import extract_OD
import extract_routes

def main():
    conn = psycopg2.connect(database='geodjango', user='megacell')
    try:
        #extract_OD.execute(conn, 'web/data/od_route_polygons.geojson', routes=True)
        #extract_OD.execute(conn, 'data/od_trajectory_polygons.geojson', routes=False)
        extract_routes.execute(conn, 'web/data/routes_paths.geojson')
    finally:
        conn.close()

if __name__ == "__main__":
    main()
