'''
Created on Jun 9, 2015

@author: mucx
'''

import svgwrite
import datetime
import math

class Drawing(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename
        
        self.circles = []
        self.circle_groups = []
        self.paths = []
        self.path_groups = []
        self.paths_bezier = []
        self.path_bezier_groups = []
        
    ############################################################################
    # Drawing handling functions
        
    def create(self, format_type):
        
        file_out = self.get_file_out()
        
        bounds = self.get_bounds()
        
        print bounds
        
        img_buffer = 10.0
        
        # Image dimensions are the bounding box of all geometries plus a buffer.
        if format_type == "fit":
            
            width = math.fabs(bounds[2] - bounds[0])
            height = math.fabs(bounds[3] - bounds[1])            
            width += 2*img_buffer
            height += 2*img_buffer
            
            x_viewbox = bounds[0] - img_buffer
            y_viewbox = bounds[1] - img_buffer
            
            width_viewbox = width
            height_viewbox = height
        
        # Image dimensions are twice the size of the maximum absolute distance
        # from the origin (symmetrical to x and y axis). The viewbox is always
        # in the ++ Quadrant. A buffer is added.
        elif format_type == "full":
            
            x_max_abs = max(math.fabs(bounds[2]), math.fabs(bounds[0]))
            y_max_abs = max(math.fabs(bounds[3]), math.fabs(bounds[1]))
            
            width = 2 * x_max_abs
            height = 2 * y_max_abs
            width += 2 * img_buffer
            height += 2 * img_buffer
            
            x_viewbox = 0
            y_viewbox = 0
            
            width_viewbox = x_max_abs + img_buffer
            height_viewbox = y_max_abs + img_buffer
            
        viewbox = str(x_viewbox) + " " + str(y_viewbox) + " "
        viewbox += str(width_viewbox) + " " + str(height_viewbox)        
        print viewbox
        
        # Creating the image with a 10px buffer on each side
        self.drawing = svgwrite.Drawing(                                        
            file_out,
            width = width,
            height = height,
            viewBox=viewbox
        )
        
        for path in self.paths_bezier:
            
            self.draw_path_bezier(path)
        
        for group in self.path_bezier_groups:
            
            self.draw_group(group, "path_bezier")
        
    def get_file_out(self):
        
        return self.filename + "_" + self.get_formatted_time() + ".svg"
        
    def save(self):
        
        self.drawing.save()
        
    def get_formatted_time(self):

        t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        
        return t_form
    
    ############################################################################
    # Feature adding functions
    
    def add_circles(self, circle):
        
        self.circles.append(circle)
        
    def add_circle_group(self, circle_group):
        
        self.circle_groups.append(circle_group)
    
    def add_path(self, path):
        """
        Adding an array of paths to the image
        """
        
        self.paths.append(path)
        
    def add_path_group(self, path_group):
        """
        Adding arrays of arrays of paths to the image
        """
        
        self.path_groups.append(path_group)
        
    def add_path_bezier(self, path, style):
        
        self.paths_bezier.append([path, style])
        
    def add_path_bezier_group(self, path_group, style):
        
        self.path_bezier_groups.append([path_group, style])
    
    ############################################################################
    # Feature drawing functions
    
    def draw_circle(self, center, r, parent):
        
        parent.add(self.drawing.circle(center = (center[0], center[1], r)))
    
    def draw_path(self, svg, parent = None, style = None):
        
        if parent is None:
            parent = self.drawing
            
        if style is None:
            parent.add(self.drawing.path(d=svg))  
        else:      
            parent.add(self.drawing.path(
                d=svg,
                stroke_width = style.stroke_width,
                stroke = style.stroke_color,
                fill = style.fill
            ))
            
    def draw_path_bezier(self, path):
                
        svg = self.curve_to_svg_bezier(path[0])
        
        self.draw_path(svg, style = path[1])
            
    def draw_group(self, group, group_type):
        
        paths = group[0]
        style = group[1]
        
        grp = self.drawing.g(
            stroke_width = style.stroke_width,
            stroke = style.stroke_color,
            fill = style.fill
        )        
        
        for path in paths:
        
            if group_type == "path" :     
                
                svg = self.linepoints_to_svg_path(path)
                self.draw_path(svg, grp)
                
            elif group_type == "path_bezier" :
                
                svg = self.curve_to_svg_bezier(path)
                self.draw_path(svg, grp)
                
            elif group_type == "circle":
                
                self.draw_circle(path, grp)
            
        self.drawing.add(grp)
        
    def get_bounds(self):
        
        bbox = self.get_feature_bbox()
        
        x_min = bbox[0][0]
        y_min = bbox[0][1]
        x_max = bbox[1][0]
        y_max = bbox[1][1]
        
        return [x_min, y_min, x_max, y_max]
        
    def get_feature_bbox(self):
        
        # Circle points
        def get_points_circles(circles):
            
            points = []
            
            if len(circles) > 0:
                for circle in circles:
                    points.append(circle)
                    
            return points
        
        def get_points_circle_groups():
            
            points = []
            
            for group in self.circle_groups:
                points += get_points_circles(group)
                
            return points
        
        # Path points
        def get_points_paths(paths):
            
            points = []
            
            if len(paths) > 0:
                for path in paths:
                    for point in path:
                        points.append(point)
                        
            return points
                        
        def get_points_path_groups():
            
            points = []
            
            for group in self.path_groups:
                points += get_points_paths(group)
                
            return points
        
        # Bezier path points
        def get_points_paths_bezier():
            
            points = []
            
            for path in self.paths_bezier:                               
                for i in range(0, len(path[0]), 3):
                    
                    points.append(path[0][i])
                
            return points
                        
        def get_points_path_bezier_groups():
            
            points = []
            
            for group in self.path_bezier_groups:
                
                paths = group[0]                
                if len(paths) > 0:
                    
                    for path in paths:                        
                        for i in range(0, len(path), 3):
                            
                            points.append(path[i])
                
            print points
            
            return points
        
        ########################################################################
        def get_all_points():
            
            points = []
            
            points += get_points_circles(self.circles)
            
            points += get_points_circle_groups()
            
            points += get_points_paths(self.paths)
            
            points += get_points_path_groups()
            
            points += get_points_paths_bezier()
            
            points += get_points_path_bezier_groups()
            
            return points
        
        ########################################################################    
        def get_xys():
            
            xs = []
            ys = []
            
            points = get_all_points()
            
            print points
            
            for point in points:
                xs.append(point[0])
                ys.append(point[1])
                
            return [xs, ys]
        
        ########################################################################
        
        xys = get_xys()
        xs = xys[0]
        ys = xys[1]
            
        x_min = min(xs)
        y_min = min(ys)
        x_max = max(xs)
        y_max = max(ys)  
        
        bbox = [[x_min, y_min], [x_max, y_max]]
        
        # Round coordinates? (+ 10 px) ? (avoid points on egdes)
        
        return bbox
    
    ############################################################################
    # Point arrays to SVG path string conversion methods
    
    def curve_to_svg_bezier(self, curve):
        """
        Returns a SVG path representation of an array of points that describe
        a Bezier curve.
        """
        
        m = curve.pop(0)
        
        svg = "M " + self.coord_string(m) + " C"
        
        for p in curve:
            svg += " " + self.coord_string(p)
            
        return svg
    
    def linepoints_to_svg_path(self, curve):
        """
        Returns a SVG path representation of an array of points that form a 
        path.
        """
        
        m = curve.pop(0)
        
        svg = "M " + self.coord_string(m) + " L"
        
        for p in curve:
            svg += " " + self.coord_string(p)
            
        return svg
    
    def coord_string(self, point):
        """
        Returns the coordinates of a point in the format of a SVG path string.
        """
        
        return str(point[0]) + " " + str(point[1])

class Style(object):
    
    def __init__(self, stroke_width, stroke_color, fill):
        
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill = fill

class StyleLine(Style):
    
    def __init__(self, stroke_width, stroke_color, fill):
        
        super(StyleLine, self).__init__(stroke_width, stroke_color, fill)
        
class StyleCircle(Style):
    
    def __init__(self, stroke_width, stroke_color, fill, radius):
        
        super(StyleCircle, self).__init__(stroke_width, stroke_color, fill)

        self.radius = radius