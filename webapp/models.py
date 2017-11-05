from django.db import models

import json
import random


class Block(models.Model):

    typestr = models.CharField(max_length=10)
    x = models.IntegerField()
    y = models.IntegerField()
    cooldown = models.IntegerField()
    health = models.FloatField()

    def __init__(self, x, y, cooldown, health):
        self.typestr = "basic"
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.health = health
        super(Block, self).__init__()

    class Meta:
        unique_together = ('x', 'y')

    def __str__(self):

        out = {'type': self.typestr, 'health': self.health, 'x': self.x, 'y': self.y, 'cooldown': self.cooldown}
        return json.dumps(out)

    def as_json(self):
        return {'type': self.typestr, 'health': self.health, 'x': self.x, 'y': self.y, 'cooldown': self.cooldown}

    def on_place(self, board):
        return

    def on_tick(self, board):
        return

    def get_neighbors(self, board):
        neighbors = list()
        if (self.x, self.y + 1) in board:
            neighbors.append(board[(self.x, self.y + 1)])
        if (self.x, self.y - 1) in board:
            neighbors.append(board[(self.x, self.y + 1)])
        if (self.x + 1, self.y) in board:
            neighbors.append(board[(self.x, self.y + 1)])
        if (self.x - 1, self.y) in board:
            neighbors.append(board[(self.x, self.y + 1)])
        return neighbors

    def get_empty_neighbors(self, board):
        neighbors = list()
        if (self.x, self.y + 1) not in board:
            neighbors.append((self.x, self.y + 1))
        if (self.x, self.y - 1) not in board:
            neighbors.append((self.x, self.y + 1))
        if (self.x + 1, self.y) not in board:
            neighbors.append((self.x, self.y + 1))
        if (self.x - 1, self.y) not in board:
            neighbors.append((self.x, self.y + 1))
        return neighbors


class ColorBlock(Block):

    color = models.CharField(max_length=10)

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "basic"
        super(ColorBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})


class GolBlock(Block):

    gol_cooldown = models.IntegerField()
    add_next_tick = dict()
    remove_next_tick = False

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "gol"
        self.gol_cooldown = 60
        super(GolBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)

    def on_tick(self, board):

        neighbors = [x for x in self.get_neighbors(board) if x.typestr == "gol"]

        remove = self.remove_next_tick
        add = self.add_next_tick.copy()
        self.add_next_tick = dict()

        if len(neighbors) < 2 or len(neighbors) > 3:
            self.remove_next_tick = True

        for coords in self.get_empty_neighbors(board):

            neighbor_count = 0
            if (coords[0], coords[1] + 1) not in board:
                neighbor_count = neighbor_count+1
            if (coords[0], coords[1] - 1) not in board:
                neighbor_count = neighbor_count + 1
            if (coords[0] + 1, coords[1]) not in board:
                neighbor_count = neighbor_count + 1
            if (coords[0] - 1, coords[1]) not in board:
                neighbor_count = neighbor_count + 1
            if neighbor_count == 3:
                self.add_next_tick[coords] = GolBlock(coords[0], coords[1])

        for key in add.keys():
            if key not in board:
                board[key] = add[key]
            else:
                add[key].delete()

        if remove:
            del board[(self.x, self.y)]
            self.delete()


class MbsBlock(Block):
    mbs_cooldown = models.IntegerField()

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "mbs"
        super(MbsBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class NotEastBlock(Block):
    powered = models.BooleanField()

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "note"
        super(NotEastBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class NotNorthBlock(Block):
    powered = models.BooleanField()

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "notn"
        super(NotNorthBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class NotSouthBlock(Block):
    powered = models.BooleanField()

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "nots"
        super(NotSouthBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class NotWestBlock(Block):
    powered = models.BooleanField()

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "notw"
        super(NotWestBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class WireBlock(Block):

    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "wireoff"
        super(WireBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)

    def on_tick(self, board):
        for wire in [x for x in self.get_neighbors(board) if x.typestr == "wireoff"]:
            board[(wire.x, wire.y)] = WireBlock(x=wire.x, y=wire.y, health=wire.health)
            wire.delete()


class OthelloWhiteBlock(Block):
    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "othw"
        super(OthelloWhiteBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class OthelloBlackBlock(Block):
    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "othw"
        super(OthelloBlackBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)


class TNTBlock(Block):
    def __init__(self, x, y, cooldown=5 * 60, health=1):
        self.typestr = "tnt"
        super(TNTBlock, self).__init__(x=x, y=y, cooldown=cooldown, health=health)
