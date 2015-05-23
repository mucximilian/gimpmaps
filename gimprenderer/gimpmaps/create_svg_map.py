'''
Created on May 11, 2015

@author: mucx
'''

from gimpmaps import renderermap
    
svg_renderer = renderermap.MapRendererSvg("config_test.json")
svg_renderer.render()