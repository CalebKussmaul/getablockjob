from django.db import models

import json
import random


class Block(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    cooldown = models.IntegerField(default=5*60)
    health = models.FloatField(default=1)

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

    def is_powered(self, board):

        ncoord = (self.x, self.y + 1)
        if ncoord in board and board[ncoord].typestr == "nots" and board[ncoord].powered:
            return True
        ncoord = (self.x, self.y - 1)
        if ncoord in board and board[ncoord].typestr == "notn" and board[ncoord].powered:
            return True
        ncoord = (self.x + 1, self.y)
        if ncoord in board and board[ncoord].typestr == "notw" and board[ncoord].powered:
            return True
        ncoord = (self.x - 1, self.y)
        if ncoord in board and board[ncoord].typestr == "note" and board[ncoord].powered:
            return True

        return False

    def get_connected_wires(self, board, s=set()):

        s.add(self)
        for n in [x for x in self.get_neighbors(board) if x.typestr == "wireon" or x.typestr == "wireoff"]:
            if n not in s:
                s.add(n)
                s = s.intersection(n.get_connected_wires(board, s))
        return s


class BacteriaBlock(Block):

    typestr = models.CharField(max_length=10, default="bacteria")

    def on_tick(self, board):
        if random.randint(0, 100) == 1:
            d = random.randint(0, 3)
            coord = (self.x, self.y)
            if d == 0:
                coord = (self.x, self.y + 1)
            elif d == 1:
                coord = (self.x, self.y - 1)
            if d == 2:
                coord = (self.x + 1, self.y)
            elif d == 3:
                coord = (self.x - 1, self.y)
            if coord in board:
                board[coord].health -= 1
                if board[coord].health < 0:
                    board[coord].delete()
                board[coord] = BacteriaBlock.objects.create(x=coord[0], y=coord[1])


class ColorBlock(Block):
    color = models.CharField(max_length=10)
    typestr = models.CharField(max_length=10, default="basic")

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})
        return out


class GolBlock(Block):
    gol_cooldown = models.IntegerField()
    add_next_tick = dict()
    remove_next_tick = False
    typestr = models.CharField(max_length=10, default="gol")

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
                neighbor_count = neighbor_count + 1
            if (coords[0], coords[1] - 1) not in board:
                neighbor_count = neighbor_count + 1
            if (coords[0] + 1, coords[1]) not in board:
                neighbor_count = neighbor_count + 1
            if (coords[0] - 1, coords[1]) not in board:
                neighbor_count = neighbor_count + 1
            if neighbor_count == 3:
                self.add_next_tick[coords] = GolBlock.objects.create(x=coords[0], y=coords[1])

        for key in add.keys():
            if key not in board:
                board[key] = add[key]
            else:
                add[key].delete()

        if remove:
            del board[(self.x, self.y)]
            self.delete()


class MbsBlock(Block):
    mbs_cooldown = models.IntegerField(default=5 * 60)
    typestr = models.CharField(max_length=10, default="mbs")

    def on_tick(self, board):
        print("fuck")
        return


class NotEastBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = models.CharField(max_length=10, default="note")

    def on_tick(self, board):
        coord = (self.x, self.y + 1)
        if coord in board and ((board[coord].typestr == "nots" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x, self.y - 1)
        if coord in board and ((board[coord].typestr == "notn" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x - 1, self.y)
        if coord in board and ((board[coord].typestr == "note" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        return False


class NotNorthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = models.CharField(max_length=10, default="notn")

    def on_tick(self, board):
        coord = (self.x, self.y - 1)
        if coord in board and ((board[coord].typestr == "notn" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x + 1, self.y)
        if coord in board and ((board[coord].typestr == "notw" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x - 1, self.y)
        if coord in board and ((board[coord].typestr == "note" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        return False


class NotSouthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = models.CharField(max_length=10, default="nots")

    def on_tick(self, board):
        coord = (self.x, self.y + 1)
        if coord in board and ((board[coord].typestr == "nots" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x + 1, self.y)
        if coord in board and ((board[coord].typestr == "notw" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x - 1, self.y)
        if coord in board and ((board[coord].typestr == "note" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        return False


class NotWestBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = models.CharField(max_length=10, default="notw")

    def on_tick(self, board):
        coord = (self.x, self.y + 1)
        if coord in board and ((board[coord].typestr == "nots" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x, self.y - 1)
        if coord in board and ((board[coord].typestr == "notn" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        coord = (self.x + 1, self.y)
        if coord in board and ((board[coord].typestr == "notw" and board[coord].powered)
                               or board[coord].typestr == "wireon"):
            return True
        return False


class WireBlock(Block):
    ticked = False
    typestr = models.CharField(max_length=10, default="wireoff")

    def on_tick(self, board):
        if self.ticked:
            self.ticked = False
            return
        wires = self.get_connected_wires(board)
        is_powered = False
        for wire in wires:
            wire.ticked = True
            if wire.is_powered(board):
                is_powered = True
                break
        for wire in wires:
            wire.typestr = "wireon" if is_powered else "wireoff"


class OthelloWhiteBlock(Block):
    typestr = models.CharField(max_length=10, default="othw")

    def on_place(self, board):

        for x in range(self.x, self.x - 20):
            if (x, self.y) in board and board[(x, self.y)].typestr == "othw":
                for xi in range(x, self.x):
                    if (xi, self.y) in board:
                        b = board[(xi, self.y)]
                        del board[(xi, self.y)]
                        b.delete()
                    board[(xi, self.y)] = OthelloWhiteBlock.objects.create(x=xi, y=self.y)
                break
        for x in range(self.x, self.x + 20):
            if (x, self.y) in board and board[(x, self.y)].typestr == "othw":
                for xi in range(x, self.x):
                    if (xi, self.y) in board:
                        b = board[(xi, self.y)]
                        del board[(xi, self.y)]
                        b.delete()
                    board[(xi, self.y)] = OthelloWhiteBlock.objects.create(x=xi, y=self.y)
                break
        for y in range(self.y, self.y - 20):
            if (self.x, y) in board and board[(self.x, y)].typestr == "othw":
                for yi in range(y, self.y):
                    if (self.x, yi) in board:
                        b = board[(self.x, yi)]
                        del board[(self.x, yi)]
                        b.delete()
                    board[(self.x, yi)] = OthelloWhiteBlock.objects.create(x=self.x, y=yi)
                break
        for y in range(self.y, self.y + 20):
            if (self.x, y) in board and board[(self.x, y)].typestr == "othw":
                for yi in range(y, self.y):
                    if (self.x, yi) in board:
                        b = board[(self.x, yi)]
                        del board[(self.x, yi)]
                        b.delete()
                    board[(self.x, yi)] = OthelloWhiteBlock.objects.create(x=self.x, y=yi)
                break


class OthelloBlackBlock(Block):
    typestr = models.CharField(max_length=10, default="othb")

    def on_place(self, board):

        for x in range(self.x, self.x - 20):
            if (x, self.y) in board and board[(x, self.y)].typestr == "othb":
                for xi in range(x, self.x):
                    if (xi, self.y) in board:
                        b = board[(xi, self.y)]
                        del board[(xi, self.y)]
                        b.delete()
                    board[(xi, self.y)] = OthelloBlackBlock.objects.create(x=xi, y=self.y)
                break
        for x in range(self.x, self.x + 20):
            if (x, self.y) in board and board[(x, self.y)].typestr == "othb":
                for xi in range(x, self.x):
                    if (xi, self.y) in board:
                        b = board[(xi, self.y)]
                        del board[(xi, self.y)]
                        b.delete()
                    board[(xi, self.y)] = OthelloBlackBlock.objects.create(x=xi, y=self.y)
                break
        for y in range(self.y, self.y - 20):
            if (self.x, y) in board and board[(self.x, y)].typestr == "othb":
                for yi in range(y, self.y):
                    if (self.x, yi) in board:
                        b = board[(self.x, yi)]
                        del board[(self.x, yi)]
                        b.delete()
                    board[(self.x, yi)] = OthelloWhiteBlock.objects.create(x=self.x, y=yi)
                break
        for y in range(self.y, self.y + 20):
            if (self.x, y) in board and board[(self.x, y)].typestr == "othb":
                for yi in range(y, self.y):
                    if (self.x, yi) in board:
                        b = board[(self.x, yi)]
                        del board[(self.x, yi)]
                        b.delete()
                    board[(self.x, yi)] = OthelloBlackBlock.objects.create(x=self.x, y=yi)
                break


class TNTBlock(Block):
    typestr = models.CharField(max_length=10, default="tnt")

