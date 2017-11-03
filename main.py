#!/usr/bin/env python

from src.globals import *
from src.level import Level
from src.input import Input
from src.gui import Gui
from src.render import Render
from src.actor import Player

import sys
import time as t
import tdl


class Game:
    LIMIT_FPS = 24
    TIC_SEC = 8
    TIC_SIZE = 1. / TIC_SEC
    FRAME_LENGTH = 1. / LIMIT_FPS

    def __init__(self):
        self.player = None
        self.actor = []
        self.render = Render(self)
        self.input = Input(self)
        self.gui = Gui(self)
        self.map = Level(self)

        self.lastTic = t.time()
        self.tic = 0

    def initialize(self):
        tdl.setFPS(self.LIMIT_FPS)
        self.render.renderStart()

        stats = {'DEADENDS': -1, 'VENTS': - 1}
#        while stats['DEADENDS'] != 0 or stats['VENTS'] < 16:
        self.map = Level(self)
        stats = self.map.generate()
        print(stats)

        self.player = Player(self.map.tile[0][0], self)
        self.map.finalize(self.player)
        self.render.printImage(self.map, "levelgen.bmp")

        self.gui.moveOffset(self.player.cell.pos - (self.render.SEPARATOR / 2))
        self.gui.updateCursor()
        self.map.updatePhysics()
        self.map.updateRender()

    def run(self):
        while True:
            if tdl.event.isWindowClosed() or game.input.quit:
                sys.exit()
            if t.time() >= self.TIC_SIZE + self.lastTic:
                self.map.updatePhysics()
                for actor in self.actor:
                    actor.act(self.map)
                self.map.updateRender()

                self.tic += 1
                self.lastTic = t.time()
            if t.time() >= self.FRAME_LENGTH + self.lastTic:
                self.render.renderAll(self.map, self.gui)
                self.input.handleEvents()


game = Game()
game.initialize()
game.run()
