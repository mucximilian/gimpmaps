'''
Created on Jun 9, 2015

@author: mucx

TO DO:
    - Adding classes for features instead of 2-dimensional arrays for features
    and styles
    - Adding layer/feature ordering
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
        """
        This is the main drawing function of the class. All features that have
        been added before are stored in an SVG image.
        
        :param format_type: Determines image dimensions
        """
        
        file_out = self.get_file_out()
        
        bounds = self.get_bounds()
        
        print bounds
        
        img_buffer = 10.0
        
        # Image dimensions are the bounding box of all geometries plus a buffer
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
        
        # TO DO: Adding missing functions
        # Ordering? 
        for path in self.paths:            
            self.draw_path_line(path)
        
        for group in self.path_groups:            
            self.draw_group(group, "path")
        
        for path in self.paths_bezier:            
            self.draw_path_bezier(path)
                    
        for group in self.path_bezier_groups:            
            self.draw_group(group, "path_bezier")
            
        for group in self.circle_groups:            
            self.draw_group(group, "circle")
        
    def get_file_out(self):
        
        return self.filename + "_" + self.get_formatted_time() + ".svg"
        
    def save(self):
        
        print "Saving image as '" + self.drawing.filename + "'"
        print "..."
        self.drawing.save()
        print "Done"
        
    def get_formatted_time(self):

        t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        
        return t_form
    
    ############################################################################
    # Feature adding functions
    
    def add_circles(self, circle, style):
        
        self.circles.append([circle, style])
        
    def add_circle_group(self, circle_group, style):
        
        self.circle_groups.append([circle_group, style])
    
    def add_path(self, path, style):
        """
        Adding an array of paths to the image
        """
        
        self.paths.append([path, style])
        
    def add_path_group(self, path_group, style):
        """
        Adding arrays of arrays of paths to the image
        """
        
        self.path_groups.append([path_group, style])
        
    def add_path_bezier(self, path, style):
        
        self.paths_bezier.append([path, style])
        
    def add_path_bezier_group(self, path_group, style):
        
        self.path_bezier_groups.append([path_group, style])
    
    ############################################################################
    # Feature drawing functions
    
    def draw_circle(self, center, r, parent = None, style = None):
        
        if parent is None:
            parent = self.drawing
            
        if style is None:
            parent.add(self.drawing.circle(
                center = (
                    center[0],
                    center[1]
                ),
                r = r
            ))
        else:
            parent.add(self.drawing.circle(
                center = (
                    center[0],
                    center[1],
                ),
                r = r
                # TO DO: Adding style for single circle
            ))
    
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
            
    def draw_path_line(self, path):
        
        svg = self.linepoints_to_svg_path(path[0])        
        self.draw_path(svg, style = path[1])
            
    def draw_path_bezier(self, path):
                
        svg = self.curve_to_svg_bezier(path[0])        
        self.draw_path(svg, style = path[1])
            
    def draw_group(self, group, group_type):
        
        features = group[0]
        style = group[1]
        
        grp = self.drawing.g(
            stroke_width = style.stroke_width,
            stroke = style.stroke_color,
            fill = style.fill
        )        
        
        for feature in features:
        
            if group_type == "path" :     
                
                svg = self.linepoints_to_svg_path(feature)
                self.draw_path(svg, grp)
                
            elif group_type == "path_bezier" :
                
                svg = self.curve_to_svg_bezier(feature)
                self.draw_path(svg, grp)
                
            elif group_type == "circle":
                
                self.draw_circle(feature, style.radius, grp)
            
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
                for point in group[0]:
                
                    points.append(point)
                
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
            
            for group in self.path_bezier_groups:
                
                paths = group[0]                
                if len(paths) > 0:
                    
                    for path in paths:                        
                        for point in path:
                            
                            points.append(point)
            
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
        
        :param curve: The curve with computed Bezier control points
        """
        
        m = curve.pop(0)
        
        svg = "M " + self.coord_string(m) + " C"
        
        for p in curve:
            svg += " " + self.coord_string(p)
            
        return svg
    
    def linepoints_to_svg_path(self, line):
        """
        Returns the SVG path notation for straight lines of an array of line 
        point coordinates.
        
        :param line: Array of line point coordinates
        """
        
        m = line.pop(0)      
          
        svg = "M " + self.coord_string(m) + " L"
        
        for p in line:
            svg += " " + self.coord_string(p)
            
        return svg
    
    def coord_string(self, point):
        """
        Returns the coordinates of a point in the format of a SVG path string.
        
        :param point: Point coordinates
        """
        
        return str(point[0]) + " " + str(point[1])
    
    def as_svg_path(self, d):
        """
        Returns a SVG path sequence as an SVG element with basi styling.
        
        :param d: SVG path commands
        """
                
        path = '<path d="'       
        path += d        
        path += '" style="fill:none;stroke:#000000;stroke-width:0.2;stroke-miterlimit:4;stroke-dasharray:none" />'
        
        return path

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