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
        
class ZoomSelectionPolygons(object):
    def __init__(self):
        self.polygons = ""
        
    # print the trackpoints info
    def printPt(self):
        print self.polygons