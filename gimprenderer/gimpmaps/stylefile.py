'''
Created on May 18, 2015

@author: mucx
'''

import psycopg2
import json

def get_map_style_name(map_style_id):
    
    conn = psycopg2.connect(
        'dbname=gimp_osm_styles '
        'user=gis '
        'password=gis '
        'host=localhost '
        'port=5432'
    )
    
    sql = "SELECT name FROM map_style WHERE id = %s"
    
    curs = conn.cursor()
    curs.execute(sql, (map_style_id,))

    
    name = curs.fetchone()[0]
    conn.close()

    return name

def create_stylefile(map_style_id):
    
    print "Start"

    map_style_name = get_map_style_name(1)

    json_data = {"name": map_style_name}
    
    zoom_levels = {}
    
    for i in range(0,21):
        
        zoom_level = {}    
    
        conn_zoom_style = psycopg2.connect(
            'dbname=gimp_osm_styles '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
        
        curs_zoom = conn_zoom_style.cursor()
        
        ########################################################################
        # FEATURES
        
        features_dict = {}
        
        # LINES
        lines = []
        
        sql = "SELECT * FROM get_line_tags_and_style(%s, %s)"                            
        curs_zoom.execute(sql, (map_style_id, i))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():
            
            style_stroke = {
                "brush": row[2],
                "brush_size": row[3],
                "color": row[4],
                "dynamics": row[5]
            }        
            feature = {
                "osm_tags": row[1],
                "stroke_line":style_stroke,
                "z_order": row[6]
            }   
            lines.append(feature)
                    
        features_dict["lines"] = lines
            
        # POLYGONS
        polygons = []
        
        sql = "SELECT * FROM get_polygon_tags_and_style(%s, %s)"                            
        curs_zoom.execute(sql, (map_style_id, i))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():
            
            style_stroke = {
                "brush": row[2],
                "brush_size": row[3],
                "color": row[4],
                "dynamics": row[5]
            }
            style_hachure = {
                "brush": row[6],
                "brush_size": row[7],
                "color": row[8],
                "dynamics": row[9],
                "spacing": row[10],
                "angle": row[11]
            }   
            
            feature = {
                "osm_tags": row[1],
                "stroke_line": style_stroke,
                "stroke_hachure": style_hachure,
                "image": row[12],
                "fill_color": row[13],
                "z_order": row[14]
            }
            
            polygons.append(feature)
            
        features_dict["polygons"] = polygons
        
        zoom_level["features"] = features_dict   
        
        ############################################################################
        # TEXT
        text_dict = {}           
        
        # TEXT POLYGONS
        text_polygons = []    
        sql = "SELECT * FROM get_text_polygon_tags_and_style(%s, %s)"                            
        curs_zoom.execute(sql, (map_style_id, i))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():
            
            style_stroke = {
                "brush": row[2],
                "brush_size": row[3],
                "color": row[4],
                "dynamics": row[5]
            }
            
            feature = {
                "osm_tags": row[1],
                "stroke_line":style_stroke,
                "font": row[6],
                "font_size": row[7],
                "color": row[8],
                "z_order": row[9]
            }
            
            text_polygons.append(feature)
            
        text_dict["polygons"] = text_polygons
        
        zoom_level["text"] = text_dict   
        
        ############################################################################
        # BACKGROUND IMAGE
        sql = "SELECT * FROM get_background_image(%s, %s)"                            
        curs_zoom.execute(sql, (map_style_id, i))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():        
            image = row[1]
            
        zoom_level["background"] = image    
        
        # TO DO:
        # Defining zoom levels in database for background image
        # --> Restructuring of zoom_level definition in tables (not in features)
        
        ############################################################################
        # FINALIZE     
        zoom_levels[i] = zoom_level 
            
        curs_zoom.close()
        
    json_data["zoom_levels"] = zoom_levels
    
    file_name = "styles/style_" + map_style_name.lower().replace(" ", "_") + ".json"
    
    print file_name
    
    out_file = open(file_name,"w")
    json.dump(json_data, out_file, indent=4)
    
    print "Done"
    
def create_stylefile_new(map_style_id):
    
    print "Start"

    map_style_name = get_map_style_name(map_style_id)
    json_data = {"name": map_style_name}

    
    conn_zoom_style = psycopg2.connect(
        'dbname=gimp_osm_styles '
        'user=gis '
        'password=gis '
        'host=localhost '
        'port=5432'
    )
    
    curs_zoom = conn_zoom_style.cursor()
    
    ########################################################################
    # FEATURES
    
    features_dict = {}
    
    # LINES
    lines = []
    
    sql = "SELECT * FROM get_line_tags_and_style(%s)"                            
    curs_zoom.execute(sql, (map_style_id,))
    
    # Store feature data in an array       
    for row in curs_zoom.fetchall():
        
        style_stroke = {
            "brush": row[2],
            "brush_size": row[3],
            "color": row[4],
            "dynamics": row[5]
        }        
        feature = {
            "osm_tags": row[1],
            "stroke_line":style_stroke,
            "z_order": row[6],
            "zoom_min":row[7],
            "zoom_max":row[8]
        }   
        lines.append(feature)
                
    features_dict["lines"] = lines
        
    # POLYGONS
    polygons = []
    
    sql = "SELECT * FROM get_polygon_tags_and_style(%s)"                            
    curs_zoom.execute(sql, (map_style_id,))
    
    # Store feature data in an array       
    for row in curs_zoom.fetchall():
        
        style_stroke = {
            "brush": row[2],
            "brush_size": row[3],
            "color": row[4],
            "dynamics": row[5]
        }
        style_hachure = {
            "brush": row[6],
            "brush_size": row[7],
            "color": row[8],
            "dynamics": row[9],
            "spacing": row[10],
            "angle": row[11]
        }   
        
        feature = {
            "osm_tags": row[1],
            "stroke_line": style_stroke,
            "stroke_hachure": style_hachure,
            "image": row[12],
            "fill_color": row[13],
            "z_order": row[14],
            "zoom_min":row[15],
            "zoom_max":row[16]
        }
        
        polygons.append(feature)
            
        features_dict["polygons"] = polygons
        
        ############################################################################
        # TEXT
        text_dict = {}           
        
        # TEXT POLYGONS
        text_polygons = []    
        sql = "SELECT * FROM get_text_polygon_tags_and_style(%s)"                            
        curs_zoom.execute(sql, (map_style_id,))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():
            
            style_stroke = {
                "brush": row[2],
                "brush_size": row[3],
                "color": row[4],
                "dynamics": row[5]
            }
            
            effect = {
                "name":row[12],
                "buffer_size":row[13],
                "buffer_color":row[14]
            }
            
            feature = {
                "osm_tags": row[1],
                "stroke_line": style_stroke,
                "font": row[6],
                "font_size": row[7],
                "color": row[8],
                "effect": effect,
                "z_order": row[9],
                "zoom_min":row[10],
                "zoom_max":row[11]                
            }
            
            text_polygons.append(feature)
            
        text_dict["polygons"] = text_polygons
        
        json_data["text"] = text_dict   
        
        ############################################################################
        # BACKGROUND IMAGE
        bg_images = []
        sql = "SELECT * FROM get_background_image(%s)"                            
        curs_zoom.execute(sql, (map_style_id,))
        
        # Store feature data in an array       
        for row in curs_zoom.fetchall():        
            
            image = {
                "image":row[1],
                "zoom_min":row[2],
                "zoom_max":row[3]
            }
            bg_images.append(image)
            
        json_data["background"] = bg_images    

    curs_zoom.close()
        
    json_data["features"] = features_dict
    
    file_name = "styles/style_" + map_style_name.lower().replace(" ", "_") + ".json"
    
    print file_name
    
    out_file = open(file_name,"w")
    json.dump(json_data, out_file, indent=4)
    
    print "Done"
    
def read_stylefile(read_file):
    
    read_file = open(read_file,"r")
    json_data = json.load(read_file)
    
    features_lines = json_data["zoom_levels"]["12"]["features"]["lines"]
    
    for line in features_lines:
        print line["z_order"]
        print line["stroke_line"]["color"]
        print line["stroke_line"]["dynamics"]
        print line["stroke_line"]["brush"]
        print line["stroke_line"]["brush_size"]
        print line["osm_tags"]
        

create_stylefile_new(1)

# read_stylefile("styles/test.json")