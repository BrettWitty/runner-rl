from src.globals import *

from src.object.object import Object
from src.object.item import Key
from src.gui import Gui


class Vent(Object):
    def __init__(self, cell=None):
        Object.__init__(self, cell, char='#', color=(100, 100, 100))

        self.block = [False, True, False]

    def interact(self, actor=None, dir=None, type=None):
        if type is 'ATTACK':
            self.destroy()
            return 5

        self.cell.object.remove(self)
        return 10

    def describe(self):
        return "Vent"


class Door(Object):
    def __init__(self, cell=None, tier=0):
        Object.__init__(self, cell, char=178, color=COLOR['GRAY'])

        self.tier = tier
        self.closed = True
        self.block = [True, True, True]

    def open(self, actor):
        if self.authorize(actor):
#            actor.main.sound['DOOR'].play()
            self.closed = False
            self.block = [False, False, False]
            self.char = 177

    def close(self, actor):
        if self.authorize(actor):
#            actor.main.sound['DOOR'].play()
            self.closed = True
            self.block = [True, True, True]
            self.char = 178

    def interact(self, actor=None, dir=None, type=None):
        if type is 'ATTACK':
            self.destroy()
            return 5
        if self.closed:
            self.open(actor)
        else:
            self.close(actor)
        return 3

    def authorize(self, actor):
        return True

    def describe(self):
        return "Door ({:})".format(self.tier)


class SecDoor(Door):
    def __init__(self, cell=None, tier=0):
        Door.__init__(self, cell, tier)

    def authorize(self, actor):
        for item in actor.inventory:
            if isinstance(item, Key) and item.tier == self.tier:
                Gui.pushMessage("Access granted")
                return True
        Gui.pushMessage("Access denied", COLOR['RED'])
        return False

    def describe(self):
        return "SecDoor ({:})".format(self.tier)


class AutoDoor(Door):
    def __init__(self, cell=None, tier=0):
        Door.__init__(self, cell, tier=tier)

    def physics(self, map):
        obj = 0
        for cell in map.getNeighborhood(self.cell.pos) + [self.cell]:
            obj += len(cell.object)
        if obj > 1:
            self.open()
        else:
            self.close()

    def interact(self, actor=None, dir=None, type=None):
        return 0

    def describe(self):
        return "Autodoor ({:})".format(self.tier)
