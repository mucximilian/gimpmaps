'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division

import math
import random

from geometry import LineSimple

'''
This module is a customized and simplified copy of the HandyRenderer.java 
class which contains the geometry processing logic of the Handy Processing 
library developed by Jo Wood.

http://www.gicentre.net/software/#/handy/
'''

seed = 1 
bowing = 1.0
roughness = 1.0

def line(line, max_offset):
    """
    Clone of the function:
    
    void line(float x1, float y1, float x2, float y2, float maxOffset)
    """
    
    line = LineSimple(line)
    
    x1 = line.coords[0][0]
    y1 = line.coords[0][1]
    x2 = line.coords[1][0]
    y2 = line.coords[1][1]

    # Ensure random perturbation is no more than 10% of line length.
    lenSq = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
    offset = max_offset

    if (max_offset * max_offset * 100 > lenSq):
        offset = math.sqrt(lenSq)/10.0

    half_offset = offset/2
    
    random.seed(line.length() * seed)
    
    divergePoint = 0.2 + random.random() * 0.2

    # This is the midpoint displacement value to give slightly bowed lines.
    midDispX = bowing * max_offset * (y2-y1) / 200.0
    midDispY = bowing * max_offset * (x1-x2) / 200.0

    midDispX = get_offset(-midDispX, midDispX)
    midDispY = get_offset(-midDispY, midDispY)

    # Calculating line 1           
    line1 = get_displaced_linepoints(x1, y1, x2, y2, 
                                          midDispX, midDispY, 
                                          divergePoint, offset)
    
    # Calculating line 2
    line2 = get_displaced_linepoints(x1, y1, x2, y2, 
                                          midDispX, midDispY, 
                                          divergePoint, half_offset)
                
    return [line1, line2]
    
def get_offset(minVal, maxVal):
    """
    Clone of the function:
    
    float getOffset(float minVal, float maxVal)
    
    Should be called only from the 'line' function for secure random seed.
    """
         
    offset = roughness * (random.random() * (maxVal - minVal) + minVal)
         
    return offset

def get_displaced_linepoints(x_a, y_a, x_b, y_b, 
                 midDispX, midDispY, divergePoint, offset):
    """
    This is part of the line function in the original Java code and was put
    separately for readability reasons.
    """
    
    x0 = x_a + get_offset(-offset, offset)
    y0 = y_a + get_offset(-offset, offset)
    p0 = [x0, y0]
    
    x1 = midDispX + x_a + (x_b-x_a) * divergePoint + get_offset(-offset, offset)
    y1 = midDispY + y_a + (y_b-y_a) * divergePoint + get_offset(-offset, offset)
    p1 = [x1, y1]
    
    x2 = midDispX + x_a + 2 * (x_b-x_a) * divergePoint + get_offset(-offset, offset)
    y2 = midDispY + y_a + 2 * (y_b-y_a) * divergePoint + get_offset(-offset, offset)
    p2 = [x2, y2] 
    
    x3 = + x_b + get_offset(-offset, offset)
    y3 = + y_b + get_offset(-offset, offset)
    p3 = [x3, y3]
    
    # Note:
    # get_offset(...) cannot be substituted to a variable as the
    # random function inside it needs to be called each time
    
    line = [p0, p1, p2, p3]
    
    return line 