# -*- coding: utf-8 -*-

class ZoomSelectionLines(object):    
    def __init__(self):
        
        self.roads = {
        5: """
            highway=motorway,
            highway=motorway_link
            """,
        6: """
            highway=motorway,
            highway=motorway_link
            """,
        7: """
            highway=motorway,
            highway=motorway_link
            """,
        8: """
            highway=motorway,
            highway=motorway_link
            """,
        9: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            """,
        10: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            """,
        11: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            """,
        12: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary'
            """,
        13: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary'
            """,
        14: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary'
            """,
        15: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary' OR 
            highway = 'tertiary' OR 
            highway = 'residential'
            """,
        16: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary' OR 
            highway = 'tertiary' OR 
            highway = 'residential' OR 
            highway = 'service'
            """,
        17: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary' OR 
            highway = 'tertiary' OR 
            highway = 'residential' OR 
            highway = 'service'
            """,
        18: """
            highway = 'motorway' OR
            highway = 'motorway_link' OR
            highway = 'primary' OR 
            route = 'road' OR 
            highway = 'secondary' OR 
            highway = 'tertiary' OR 
            highway = 'residential' OR 
            highway = 'service'
            """,
        }   
        
    # print the trackpoints info
    def printPt(self):
        print self.roads
        
class ZoomSelection(object):    
    def __init__(self):
        
        self.lines = {
            5: [
                {
                    "tags": [
                        "highway=motorway"
                    ],
                    "style": {
                        "brush": "GIMP Brush #7",
                        "brush_size": 12,
                        "color": [
                            128,
                            128,
                            128
                        ],
                        "dynamics": "Det3",
                        "opacity": 255            
                    },
                    "z_order": 1
                },
                {
                    "tags": [
                        "highway=motorway_link"
                    ],
                    "style": {
                        "brush": "GIMP Brush #7",
                        "brush_size": 12,
                        "color": [
                            128,
                            128,
                            128
                        ],
                        "dynamics": "Det3",
                        "opacity": 255            
                    },
                    "z_order": 1
                }
            ],
            6: """
                highway=motorway,
                highway=motorway_link
                """,
            7: """
                highway=motorway,
                highway=motorway_link
                """,
            8: """
                highway=motorway,
                highway=motorway_link
                """,
            9: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                """,
            10: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                """,
            11: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                """,
            12: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary'
                """,
            13: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary'
                """,
            14: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary'
                """,
            15: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary' OR 
                highway = 'tertiary' OR 
                highway = 'residential'
                """,
            16: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary' OR 
                highway = 'tertiary' OR 
                highway = 'residential' OR 
                highway = 'service'
                """,
            17: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary' OR 
                highway = 'tertiary' OR 
                highway = 'residential' OR 
                highway = 'service'
                """,
            18: """
                highway = 'motorway' OR
                highway = 'motorway_link' OR
                highway = 'primary' OR 
                route = 'road' OR 
                highway = 'secondary' OR 
                highway = 'tertiary' OR 
                highway = 'residential' OR 
                highway = 'service'
                """,
        }   
        
    # print the trackpoints info
    def printPt(self):
        print self.roads
        
class ZoomSelectionLinesType(object):    
    def __init__(self):
        
        self.roads = {
        5: """
            line_type=motorway,
            line_type=motorway_link
            """,
        6: """
            line_type=motorway,
            line_type=motorway_link
            """,
        7: """
            line_type=motorway,
            line_type=motorway_link
            """,
        8: """
            line_type=motorway,
            line_type=motorway_link
            """,
        9: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            """,
        10: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            """,
        11: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            """,
        12: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary'
            """,
        13: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary'
            """,
        14: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary'
            """,
        15: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary' OR 
            line_type = 'tertiary' OR 
            line_type = 'residential'
            """,
        16: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary' OR 
            line_type = 'tertiary' OR 
            line_type = 'residential' OR 
            line_type = 'service'
            """,
        17: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary' OR 
            line_type = 'tertiary' OR 
            line_type = 'residential' OR 
            line_type = 'service'
            """,
        18: """
            line_type = 'motorway' OR
            line_type = 'motorway_link' OR
            line_type = 'primary' OR 
            line_type = 'road' OR 
            line_type = 'secondary' OR 
            line_type = 'tertiary' OR 
            line_type = 'residential' OR 
            line_type = 'service'
            """
        }   
        
    # print the trackpoints info
    def printPt(self):
        print self.roads
        
class ZoomSelectionPolygons(object):
    def __init__(self):
        self.polygons = ""
        
    # print the trackpoints info
    def printPt(self):
        print self.polygons