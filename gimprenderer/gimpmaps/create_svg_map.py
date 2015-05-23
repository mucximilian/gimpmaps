'''
Created on May 11, 2015

@author: mucx
'''

from gimpmaps import maprenderer
    
svg_renderer = maprenderer.MapRendererSvg("config_test.json")
svg_renderer.render()