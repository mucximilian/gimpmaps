'''
Created on May 18, 2015

@author: mucx
'''

import psycopg2
import json

map_style_id = 1
json_data = {"name": "Chalk map","type": "Hachure map"}

zoom_levels = {}

for i in range(0,21):
    
    zoom_level = {}
    features_dict = {}
    features = []    

    conn_zoom_style = psycopg2.connect(
        'dbname=gimp_osm_styles '
        'user=gis '
        'password=gis '
        'host=localhost '
        'port=5432'
    )
    
    curs_zoom = conn_zoom_style.cursor()
    
    ############################################################################
    # LINES
    lines = []
    lines_dict = {}
    
    sql = "SELECT * FROM get_line_tags_and_style(%s, %s)"                            
    curs_zoom.execute(sql, (map_style_id, i))
    
    # Store feature data in an array       
    for row in curs_zoom.fetchall():
        
        line_data = {
            "brush": row[2],
            "brush_size": row[3],
        }        
        feature = {
            "osm_tags": row[1],
            "stroke_line":line_data
        }        
        lines.append(feature)
    lines_dict["lines"] = lines
    features.append(lines_dict)
        
    ############################################################################
    # POLYGONS
    polygons = []
    polygons_dict = {}
    sql = "SELECT * FROM get_polygon_hachure_tags_and_style(%s, %s)"                            
    curs_zoom.execute(sql, (map_style_id, i))
    
    # Store feature data in an array       
    for row in curs_zoom.fetchall():
        
        polygon_data = {
            "brush": row[2],
            "brush_size": row[3],
        }
        
        feature = {
            "osm_tags": row[1],
            "stroke_line":line_data
        }
        
        polygons.append(feature)    
    polygons_dict["polygons"] = polygons
    features.append(polygons_dict)
    
    zoom_level["features"] = features
        
    zoom_levels[i] = zoom_level 
        
    curs_zoom.close()
    
json_data["zoom_levels"] = zoom_levels

out_file = open("test.json","w")
json.dump(json_data, out_file, indent=4)

print "Done"