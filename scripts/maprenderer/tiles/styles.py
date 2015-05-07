# -*- coding: utf-8 -*-

class StyleObject(object):
    """
    Represents geometry features with assigned style
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
        

class StyleObjectLine(StyleObject):
    """
    Specification of the StyleObject class for line features
    """

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
        
    def get_line_style(self):
        """
        Returns line style parameters
        """
        
        return [
            self.brush,
            self.brush_size,
            self.color,
            self.opacity_brush,
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
    
class StyleObjectPolygon(StyleObjectLine):
    """
    Specification of the StyleObject class for line features
    """
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
        try:
            out += (
                "Image: " + self.image + " (" + str(self.opacity_image) + ")\n"
            )        
        except TypeError:
            out = "No image or image type error"
        return out
    
    def get_image_data(self):
        return [self.image, self.opacity_image]