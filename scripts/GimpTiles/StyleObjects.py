# -*- coding: utf-8 -*-

class StyleObject(object):
    def __init__(self, geom_type, tags, z_order):
        self.geom_type = geom_type
        self.tags = tags
        self.z_order = z_order
    
    ############################################################################
    # Returns selection tags as a string suitable for a SQL 'WHERE' condition
    def get_selection_tags(self):
        selection_string = ""
        count = 0
        for tag in self.tags:
            if count > 0:
                selection_string += " OR "
            selection_string += tag
            count += 1
            
        return selection_string
        
class StyleObjectLine(StyleObject):
    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, opacity, dynamics):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.opacity = opacity
        self.dynamics = dynamics
        
    ############################################################################
    # Returns selection tags as a string suitable for a SQL 'WHERE' condition
    def get_rgba(self):            
        return [
            self.color[0],
            self.color[1],
            self.color[2],
            self.opacity
        ]
        
    def print_style(self):
        print (
            "geometry type: " + self.geom_type + "\n" +
            "OSM tags: " + str(self.tags) + "\n"
        )
    
