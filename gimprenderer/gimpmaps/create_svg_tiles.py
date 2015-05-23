# -*- coding: utf-8 -*-

from gimpmaps import tilerenderer

tile_renderer = tilerenderer.TileRendererSvg("config_test.json")
tile_renderer.render()