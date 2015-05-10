'''
Created on May 5, 2015

@author: mucx
'''

import shapely.geometry

polygon = shapely.geometry.Polygon([
                   [4.0, 20.0], 
                   [7.0, 17.0],
                   [8.0, 18.0],
                   [12.0, 15.0],
                   [14.0, 17.0], 
                   [13.0, 19.0], 
                   [10.0, 20.0], 
                   [7.0, 23.0], 
                   [4.0, 20.0]
                ])

line = shapely.geometry.LineString([[13, 15], [-0.8564064605510153, 23]])

print polygon.intersection(line)