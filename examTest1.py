#coding: utf-8
import sys
from scene import *

class Game(scene):
    def setup(self):
        self.background_color = '#004f82'
        ground = Node(parent=self)
        x=0

        while x <= self.size.w + 64:
            tile = SpriteNode('pfl:Ground_PlanetHalf_mid', position=(x,0))
            ground.add_child(tile)
            x += 64

            self.player = SpriteNode('plf:AlienGreen_front')
            self.player.anchor_point = (0.5,0)
            self.player.position = (self.size.w/2, 32)
            self.add_child(self.player)

if _name_== '_main_':
    run(Game(),LANDSCAPE,show_fps=Ture)
