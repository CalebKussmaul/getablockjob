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
        print (cooldown)
        self.typestr = "basic"
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.health = health
        # super(Block, self).__init__()

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

    def __init__(self, x, y):
        self.typestr = "basic"
        super(ColorBlock, self).__init__(x, y, 5*60, 1)

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})
        return out
        print("x",out)


class GolBlock(Block):

    gol_cooldown = models.IntegerField()
    add_next_tick = dict()
    remove_next_tick = False

    def __init__(self, x, y):
        self.typestr = "gol"
        self.gol_cooldown = 60
        super(GolBlock, self).__init__(x, y, 5 * 60, 1)

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
            board[key] = add[key]

        if remove:
            del board[(self.x, self.y)]
            self.delete()


class MbsBlock(Block):
    mbs_cooldown = models.IntegerField()

    def __init__(self, x, y):
        self.typestr = "mbs"
        super(MbsBlock, self).__init__(x, y, 5 * 60, 1)


class NotEastBlock(Block):

    def __init__(self, x, y):
        self.typestr = "note"
        super(NotEastBlock, self).__init__(x, y, 5 * 60, 1)


class NotNorthBlock(Block):

    def __init__(self, x, y):
        self.typestr = "notn"
        super(NotNorthBlock, self).__init__(x, y, 5 * 60, 1)


class NotSouthBlock(Block):

    def __init__(self, x, y):
        self.typestr = "nots"
        super(NotSouthBlock, self).__init__(x, y, 5 * 60, 1)


class NotWestBlock(Block):

    def __init__(self, x, y):
        self.typestr = "notw"
        super(NotWestBlock, self).__init__(x, y, 5 * 60, 1)


class WireOnBlock(Block):

    def __init__(self, x, y):
        self.typestr = "wireon"
        super(WireOnBlock, self).__init__(x, y, 5 * 60, 1)


class WireOffBlock(Block):
    def __init__(self, x, y):
        self.typestr = "wireoff"
        super(WireOffBlock, self).__init__(x, y, 5 * 60, 1)


class OthelloWhiteBlock(Block):
    def __init__(self, x, y):
        self.typestr = "othw"
        super(OthelloWhiteBlock, self).__init__(x, y, 5 * 60, 1)


class OthelloBlackBlock(Block):
    def __init__(self, x, y):
        self.typestr = "othw"
        super(OthelloBlackBlock, self).__init__(x, y, 5 * 60, 1)


class TNTBlock(Block):
    def __init__(self, x, y):
        self.typestr = "tnt"
        super(TNTBlock, self).__init__(x, y, 5 * 60, 1)
