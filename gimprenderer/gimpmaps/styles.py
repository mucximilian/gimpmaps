'''
Created on May 03, 2015

@author: mucx
'''

class StyleObject(object):
    """
    Represents geometry features with assigned style.
    
    TO DO: should be abstract!
    """
    
    def __init__(self, geom_type, tags, z_order):
        self.geom_type = geom_type
        self.tags = tags # A list of tags
        self.z_order = z_order
    
    def get_selection_tags(self):
        """
        Returns concatenated selection tags suitable for a SQL 'WHERE' condition
        """
        
        selection_string = " AND ".join(self.tags)            
        return selection_string
    
    def get_geometry_type_name(self):
        """
        Returns the name of the geometry defined by geometry type integer
        """
        
        geometry_type_name = ""
        if self.geom_type == 2:
            geometry_type_name = "line"
        elif self.geom_type == 3:
            geometry_type_name = "polygon"

        return geometry_type_name
    
    def string_color(self, color):
        out = (
               ",".join(str(x) for x in color)
        )
        return out

class StyleObjectLine(StyleObject):
    """
    Specification of the StyleObject class for line features
    """

    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, dynamics):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.dynamics = dynamics
        
    def get_z_order(self):
        return self.z_order
        
    def get_line_style(self):
        """
        Returns line style parameters
        """
        
        return [
            self.brush,
            self.brush_size,
            self.color,
            self.dynamics
        ]
        
    def get_rgba(self):    
        """
        Returns selection tags as a string suitable for a SQL 'WHERE' condition
        """
                
        return [
            self.color[0],
            self.color[1],
            self.color[2],
            self.opacity_brush
        ]
     
    def string_style(self):
        """
        Prints information about the style object
        """
              
        out = (
            "OSM feature(s): " + ", ".join(self.tags) +
                " (" + str(self.geom_type) + ")\n" +
            "z-order: " + str(self.z_order) + "\n" +
            "Brush style: " + self.brush + "(" + str(self.brush_size) + ")\n" +
            "Brush color: " + self.string_color(self.color) + "\n" +
            "Brush dynamics: " + self.dynamics + "\n"
        )
        return out
    
class StyleObjectPolygon(StyleObjectLine):
    """
    Specification of the StyleObject class for line features
    """
    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, dynamics,
        brush_hachure, brush_hachure_size, color_hachure, dynamics_hachure,
        image):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.dynamics = dynamics
        self.brush_hachure = brush_hachure
        self.brush_hachure_size = brush_hachure_size
        self.color_hachure = color_hachure
        self.dynamics_hachure = dynamics_hachure
        self.image = image
        
    def string_style(self):
        """
        Prints information about the style object
        """
              
        out = (
            "OSM feature(s): " + ", ".join(self.tags) +
                " (" + str(self.geom_type) + ")\n" +
            "z-order: " + str(self.z_order) + "\n" +
            "Brush style: " + self.brush + "(" + str(self.brush_size) + ")\n" +
            "Brush color: " + self.string_color(self.color) + "\n" +
            "Brush dynamics: " + self.dynamics + "\n"
            "Hachure style: " + self.brush_hachure + "(" + str(self.brush_hachure_size) + ")\n" +
            "Hachure color: " + self.string_color(self.color_hachure) + "\n" +
            "Hachure dynamics: " + self.dynamics_hachure + "\n" +
            "Image: " + self.image + "\n"
        )
        return out

    def get_hachure_style(self):
        """
        Returns line style parameters
        """
        
        return [
            self.brush_hachure,
            self.brush_hachure_size,
            self.hachure_color,
            self.hachure_dynamics
        ]
    
    def get_image_data(self):
        return self.image
    
class StyleObjectText(StyleObjectLine):
    """
    Specification of the StyleObject class for line features
    """
    def __init__(
        self, 
        geom_type, tags, z_order,
        brush, brush_size, color, dynamics,
        font, font_size, font_color, effect, buffer_size, buffer_color):
            
        StyleObject.__init__(self, geom_type, tags, z_order)
        self.brush = brush
        self.brush_size = brush_size
        self.color = color
        self.dynamics = dynamics
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.effect = effect
        self.buffer_size = buffer_size
        self.buffer_color = buffer_color

    def string_style(self):
        """
        Prints information about the style object
        """
              
        out = (
            "OSM feature(s): " + ", ".join(self.tags) +
                " (" + str(self.geom_type) + ")\n" +
            "z-order: " + str(self.z_order) + "\n" +
            "Brush style: " + self.brush + "(" + str(self.brush_size) + ")\n" +
            "Brush color: " + self.string_color(self.color) + "\n" +
            "Brush dynamics: " + self.dynamics + "\n"
            "Font style: " + self.font + "(" + str(self.font_size) + ")\n" +
            "Font color: " + self.string_color(self.font_color) + "\n"
        )
        return out
    
    def get_text_style(self):
        
        return [
            self.font,
            self.font_size,
            self.font_color
        ]