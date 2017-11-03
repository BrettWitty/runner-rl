from src.globals import *
from PIL import Image
import numpy as np
import copy as cp
import tdl
import tcod
import time as t


class Render:  # a rectangle on the map. used to characterize a room.
    GRAPHICSPATH = './graphics/'
    TILESET = 'tileset16x16.png'

    MAPINSET = np.array([1, 1])

    def __init__(self, main):
        self.main = main

        tdl.set_font(Render.GRAPHICSPATH + Render.TILESET,
                     greyscale=True)
        tdl.setFPS(LIMIT_FPS)

        self.console = tdl.init(
            SCREEN[WIDTH], SCREEN[HEIGHT], title="RunnerRL", fullscreen=False)
        self.console.clear(bg=[50, 50, 50])

        self.back = tdl.Window(self.console, 0, 0, None, None)
        self.back.clear(bg=[50, 50, 50])

        self.mapPanel = tdl.Window(
            self.console, Render.MAPINSET[X], Render.MAPINSET[Y], SEPARATOR[WIDTH] - 2, SEPARATOR[HEIGHT] - 2)
        self.infoPanel = tdl.Window(
            self.console, SEPARATOR[WIDTH], 1, SCREEN[WIDTH] - SEPARATOR[WIDTH] - 1, SCREEN[HEIGHT] - 2)
        self.messagePanel = tdl.Window(
            self.console, Render.MAPINSET[X], SEPARATOR[HEIGHT], SEPARATOR[WIDTH] - 2, SCREEN[HEIGHT] - SEPARATOR[HEIGHT] - 1)



        self.raymap = Render.rayMap(24, 32)
        self.lightmap = Render.rayMap(8, 32)

    def renderStart(self):
        self.mapPanel.clear(bg=BLACK)
        self.infoPanel.clear(bg=BLACK)
        self.messagePanel.clear(bg=BLACK)

        self.mapPanel.draw_str(2, 2, "Generating Level")

        self.console.blit(self.mapPanel, 1, 1)
        self.console.blit(self.infoPanel, SEPARATOR[WIDTH], 1)

        tdl.flush()

    def renderAll(self, map, gui):
        self.renderMap(map, gui.mapOffset)
        gui.renderInfo(self.infoPanel)
        gui.renderMessage(self.messagePanel)

        self.console.blit(self.mapPanel, 1, 1)
        self.console.blit(self.infoPanel, SEPARATOR[WIDTH], 1)
        tdl.flush()

    def renderMap(self, map, mapOffset):
        self.mapPanel.clear(bg=BLACK)

        for cell in self.main.gui.mapCells:
            cell.draw(self.mapPanel, cell.pos - mapOffset)

#        cell = map.getTile(self.main.gui.cursorPos)
#        cell.drawHighlight(self.mapPanel, cell.pos - mapOffset)

        cell = map.getTile(self.main.player.cell.pos + self.main.gui.cursorDir)
        cell.drawHighlight(self.mapPanel, cell.pos - mapOffset)





    @staticmethod
    def inMap(terminalPos):
        if terminalPos[X] < Render.MAPINSET[X] or terminalPos[Y] < Render.MAPINSET[Y]:
            return False
        elif terminalPos[X] >= SEPARATOR[X] - 1 or terminalPos[Y] >= SEPARATOR[Y] - 1:
            return False
        else:
            return True

    @staticmethod
    def rayCast(start, end):
        delta = end - start
        direction = delta / np.linalg.norm(delta)
        line = []

        ray = 0.25 * direction
        while np.linalg.norm(ray) <= np.linalg.norm(delta):
            if len(line) == 0 or np.linalg.norm(line[-1] - ray.round().astype('int')) != 0:
                line.append(ray.round().astype('int'))
            ray += 0.25 * direction
        return np.array(line)

    @staticmethod
    def rayMap(r, num):
        lines = []
        start = np.array([0., 0.])
        phi0 =  2*np.pi* np.random.random()
        for phi in np.linspace(phi0, phi0+ 2. * np.pi, num):
            end = r * np.array([np.cos(phi), np.sin(phi)])
            lines.append(Render.rayCast(start, end)[1:int(r)])
        return lines

    @staticmethod
    def printImage(map, fileName):
        img = Image.new('RGB', MAP, "black")  # create a new black image
        pixels = img.load()  # create the pixel map
        for x in range(MAP[WIDTH]):    # for every pixel:
            for y in range(MAP[HEIGHT]):
                if map.tile[x][y].wall is False:
                    # set the colour accordingly
                    pixels[x, y] = (40 * map.tile[x][y].tier,
                                    255 - 40 * map.tile[x][y].tier, 255)
                elif map.tile[x][y].wall is True:
                    pixels[x, y] = (25, 25, 25)  # set the colour accordingly
                elif map.tile[x][y].wall is None:
                    pixels[x, y] = (0, 0, 0)  # set the colour accordingly

                if map.tile[x][y].tier == -2:
                    pixels[x, y] = (55, 55, 55)  # set the colour accordingly

        for room in map.tier[-1]:
            if room.function is not None:
                for pos in room.rectangle.border():
                    if map.getTile(pos).wall:
                        if room.function is "start":
                            pixels[pos[X], pos[Y]] = (50, 250, 50)
                        elif room.function is "extraction":
                            pixels[pos[X], pos[Y]] = (250, 50, 50)
        img.save(fileName)
