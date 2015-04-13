# -*- coding: utf-8 -*-

import psycopg2
from TileRenderer import TileRenderer

zoom = 14

conn = psycopg2.connect('dbname=gimp_osm_styles '
    	'user=gis '
    	'password=gis '
    	'host=localhost '
    	'port=5432')    
cur = conn.cursor()

# Get OSM tags and styles for zoom level
sql = """
    SELECT * FROM get_line_tags_and_style(%s);
"""                        

# cur.execute(sql, [zoom])
cur.execute(sql, (zoom,))

for row in cur.fetchall():
    sql_selection = row[1]
    line_style = [
        row[3],
        row[4],
        row[5],
        row[6],
        row[7]
    ]
    
    tile_renderer = TileRenderer(0,0,0,0)
    selection = tile_renderer.get_selection_tags(sql_selection)
    print selection
    