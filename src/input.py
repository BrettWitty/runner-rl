from src.globals import *

import numpy as np
import tdl

from src.actor.ai import AI
from src.render import Render

class Input:

    MOVEMAP = {'w': np.array([0, -1]),
               'a': np.array([-1, 0]),
               's': np.array([0, 1]),
               'd': np.array([1, 0]),
               'q': np.array([-1, -1]),
               'e': np.array([1, -1]),
               'y': np.array([-1, 1]),
               'c': np.array([1, 1])}

    def __init__(self, main):
        self.main = main
        self.quit = False

    def handleEvents(self):
        try:
            while True:
                event = tdl.event.get().next()

                if event.type is 'KEYDOWN':
                    self.handleKey(event)
                elif event.type is 'MOUSEUP':
                    self.handleClick(event)
                elif event.type is 'MOUSEMOTION':
                    self.handleMouse(event)
                elif event.type is 'MOUSEDOWN':
                    self.handleScroll(event)
        except:
            pass

    def handleKey(self, event):
        if event.key == 'ESCAPE':
            self.quit = True
        elif event.key == 'UP':
            self.main.gui.moveOffset(np.array([0, -3]))
        elif event.key == 'DOWN':
            self.main.gui.moveOffset(np.array([0, 3]))
        elif event.key == 'LEFT':
            self.main.gui.moveOffset(np.array([-3, 0]))
        elif event.key == 'RIGHT':
            self.main.gui.moveOffset(np.array([3, 0]))

        elif event.key == 'SPACE' and len(self.main.player.actions) < 2:
            self.main.player.actions = []
            ray = self.main.gui.cursorPos - self.main.player.cell.pos
            dir = (ray / np.linalg.norm(ray)).round().astype('int')
            self.main.player.actions.append({'TYPE': 'ATTACK', 'DIR': dir})

        if event.key == 'CHAR':
            self.main.player.actions = []
            if event.char == 'r':
                self.main.gui.pushMessage("Waiting")
                self.main.player.cooldown += 2
            if event.char == 'm':
                self.main.gui.pushMessage("Switching Map")
                self.main.render.mapLayer = (self.main.render.mapLayer + 1) % 3
            if event.char in "wasdqeyc" and len(self.main.player.actions) < 2:
                self.main.player.actions.append({'TYPE': 'MOVE', 'DIR': Input.MOVEMAP[event.char]})

        if event.key == 'TEXT':
            if event.text in ['0','1','2','3','4','5']:
                index = int(event.text)
                if index < len(self.main.player.inventory):
                    self.main.player.actions.append({'TYPE': 'ITEM', 'INDEX': index})

    def handleMouse(self, event):
        self.main.gui.updateCursor(event.cell)

    def handleClick(self, event):
        self.main.player.actions = []

        if event.button is 'LEFT' and len(self.main.player.actions) < 2:
            self.main.player.actions = AI.findPath(self.main.map, self.main.player.cell.pos, self.main.gui.cursorPos)
        elif event.button is 'RIGHT' and len(self.main.player.actions) < 2:
            self.main.player.actions = AI.findPath(self.main.map, self.main.player.cell.pos, self.main.gui.cursorPos, True)

    def handleScroll(self, event):
        if event.button is 'SCROLLUP':
            if event.cell[X] <= Render.SEPARATOR[X]:
                self.main.gui.messageOffset += 1
            else:
                self.main.gui.inventoryOffset += 1
        elif event.button is 'SCROLLDOWN':
            if event.cell[X] <= Render.SEPARATOR[X]:
                self.main.gui.messageOffset -= 1
            else:
                self.main.gui.inventoryOffset -= 1

        self.main.gui.messageOffset = max(0, self.main.gui.messageOffset)
        self.main.gui.inventoryOffset = max(0, self.main.gui.inventoryOffset)
