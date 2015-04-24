# -*- coding: utf-8 -*-

################################################################################
# 
# StyleObject
# Represents geometry features with assigned style
#
class StyleObject(object):
    def __init__(self, geom_type, tags, z_order):
        self.geom_type = geom_type
        self.tags = tags # A list of tags
        self.z_order = z_order
    
    ############################################################################
    # Returns concatenated selection tags suitable for a SQL 'WHERE' condition
    def get_selection_tags(self):
        selection_string = " AND ".join(self.tags)            
        return selection_string
        
################################################################################
# 
# StyleObjectLine
# Specification of the StyleObject class for line features
#
class StyleObjectLine(StyleObject):
    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, opacity_brush, dynamics):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.opacity_brush = opacity_brush
        self.dynamics = dynamics
        
    def get_z_order(self):
        return self.z_order
        
    ############################################################################
    # Returns line style parameters
    def get_line_style(self):
        return [
            self.brush,
            self.brush_size,
            self.color,
            self.opacity_brush,
            self.dynamics
        ]
        
    ############################################################################
    # Returns selection tags as a string suitable for a SQL 'WHERE' condition
    def get_rgba(self):            
        return [
            self.color[0],
            self.color[1],
            self.color[2],
            self.opacity_brush
        ]
     
    ############################################################################
    # Prints information about the style object
    def string_style(self):
        
        out = (
            "OSM feature(s): " + ", ".join(self.tags) + " (" + self.geom_type + ")\n" +
            "z-order: " + str(self.z_order) + "\n" +
            "Brush style: " + self.brush + "(" + str(self.brush_size) + ")\n" +
            "Brush color: " + self.string_color() + "\n" +
            "Brush dynamics: " + self.dynamics + "\n"
        )
        return out
        
    def string_color(self):
        out = (
               ",".join(str(x) for x in self.color) + "," +
               str(self.opacity_brush)
        )
        return out
    
################################################################################
# 
# StyleObjectLine
# Specification of the StyleObject class for line features
#
class StyleObjectPolygon(StyleObjectLine):
    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, opacity_brush, dynamics,
        image, opacity_image):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.opacity_brush = opacity_brush
        self.dynamics = dynamics
        self.image = image
        self.opacity_image = opacity_image
        
    def string_style(self):
        out = StyleObjectLine.string_style(self)
        out += (
            "Image: " + self.image + " (" + str(self.opacity_image) + ")\n"
        )
        return out