from django.db import models

import json
import random


class Block(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    cooldown = models.IntegerField(default=5*60)
    health = models.FloatField(default=1)
    typestr = "basic"

    # class Meta:
    #     unique_together = ('x', 'y')

    def __str__(self):
        out = {'type': self.typestr, 'health': self.health, 'x': self.x, 'y': self.y, 'cooldown': self.cooldown}
        return json.dumps(out)

    def as_json(self):
        return {'type': self.typestr, 'health': self.health, 'x': self.x, 'y': self.y, 'cooldown': self.cooldown}

    def on_place(self):
        return

    def on_tick(self):
        return

    def get_neighbors(self):
        neighbors = list()
        if Block.objects.filter(x=self.x, y=self.y + 1).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y + 1))
        if Block.objects.filter(x=self.x, y=self.y - 1).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y - 1))
        if Block.objects.filter(x=self.x+1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y))
        if Block.objects.filter(x=self.x-1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y))
        return neighbors

    def get_empty_neighbors(self):
        neighbors = list()
        if not Block.objects.filter(x=self.x, y=self.y + 1).exists():
            neighbors.append((self.x, self.y + 1))
        if not Block.objects.filter(x=self.x, y=self.y - 1).exists():
            neighbors.append((self.x, self.y - 1))
        if not Block.objects.filter(x=self.x + 1, y=self.y).exists():
            neighbors.append((self.x, self.y))
        if not Block.objects.filter(x=self.x - 1, y=self.y).exists():
            neighbors.append((self.x, self.y))
        return neighbors

    def is_powered(self):

        n = Block.objects.filter(x=self.x, y=self.y + 1)
        if n.exists() and n.typestr == "notn" and n.powered:
            return True
        e = Block.objects.filter(x=self.x, y=self.y - 1)
        if e.exists() and e.typestr == "nots" and e.powered:
            return True
        s = Block.objects.filter(x=self.x + 1, y=self.y)
        if e.exists() and e.typestr == "note" and e.powered:
            return True
        w = Block.objects.filter(x=self.x - 1, y=self.y)
        if w.exists() and w.typestr == "notw" and w.powered:
            return True

        return False

    def get_connected_wires(self, s=set()):

        s.add(self)
        for n in [x for x in self.get_neighbors() if x.typestr == "wireon" or x.typestr == "wireoff"]:
            if n not in s:
                s.add(n)
                s = s.intersection(n.get_connected_wires(s))
        return s


class BacteriaBlock(Block):

    typestr = "bacteria"

    def on_tick(self):
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
            if Block.objects.filter(x=coord[0], y=coord[1]).exists():
                o = Block.objects.get(x=coord[0], y=coord[1])
                o.health -= 1
                if o.health < 0:
                    o.delete()
                BacteriaBlock.objects.create(x=coord[0], y=coord[1])


class ColorBlock(Block):
    color = models.CharField(max_length=10)
    typestr = "basic"

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})
        return out


class GolBlock(Block):
    gol_cooldown = models.IntegerField()
    add_next_tick = dict()
    remove_next_tick = False
    typestr = "gol"

    def on_tick(self):

        neighbors = [x for x in self.get_neighbors() if x.typestr == "gol"]

        remove = self.remove_next_tick
        add = self.add_next_tick.copy()
        self.add_next_tick = dict()

        if len(neighbors) < 2 or len(neighbors) > 3:
            self.remove_next_tick = True

        for coords in self.get_empty_neighbors():

            neighbor_count = 0
            if GolBlock.objects.filter(x=coords[0], y=coords[1] + 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0], y=coords[1] - 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0], y=coords[1] + 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0], y=coords[1] + 1).exists():
                neighbor_count += 1
            if neighbor_count == 3:
                self.add_next_tick[coords] = (coords[0], coords[1])

        for key in add.keys():
            if not Block.objects.filter(x=coords[0], y=coords[1]).exists():
                GolBlock.objects.create(x=coords[0], y=coords[1])
            else:
                add[key].delete()

        if remove:
            self.delete()


class MbsBlock(Block):
    mbs_cooldown = models.IntegerField(default=5 * 60)
    typestr = "mbs"

    def on_tick(self):
        print("fuck")
        return


class NotEastBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "note"

    def on_tick(self):
        ""


class NotNorthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "notn"

    def on_tick(self, board):
        ""


class NotSouthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "nots"

    def on_tick(self, board):
        ""


class NotWestBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "notw"

    def on_tick(self, board):
        ""


class WireBlock(Block):
    ticked = False

    powered = models.BooleanField(default=False)
    typestr = "wireoff"

    def on_tick(self):
        if self.ticked:
            self.ticked = False
            return
        wires = self.get_connected_wires()
        is_powered = False
        for wire in wires:
            wire.ticked = True
            if wire.is_powered():
                is_powered = True
                break
        for wire in wires:
            wire.typestr = "wireon" if is_powered else "wireoff"


class OthelloWhiteBlock(Block):
    typestr = "othw"

    def on_place(self):

        for x in range(self.x, self.x - 20):
            if OthelloWhiteBlock.objects.filter(x=x, y=self.y).exists():
                for xi in range(x, self.x):
                    o = Block.objects.filter(x=xi, y=self.y)
                    if o.exists():
                        o.delete()
                    OthelloWhiteBlock.objects.create(x=xi, y=self.y)
                break
        for x in range(self.x, self.x + 20):
            if OthelloWhiteBlock.objects.filter(x=x, y=self.y).exists():
                for xi in range(x, self.x):
                    o = Block.objects.filter(x=xi, y=self.y)
                    if o.exists():
                       o.delete()
                    OthelloWhiteBlock.objects.create(x=xi, y=self.y)
                break
        for y in range(self.y, self.y - 20):
            if OthelloWhiteBlock.objects.filter(x=self.x, y=y).exists():
                for yi in range(y, self.y):
                    o = Block.objects.filter(x=self.x, y=yi)
                    if o.exists():
                        o.delete()
                    OthelloWhiteBlock.objects.create(x=self.x, y=yi)
                break
        for y in range(self.y, self.y + 20):
            if OthelloWhiteBlock.objects.filter(x=self.x, y=y).exists():
                for yi in range(y, self.y):
                    o = Block.objects.filter(x=self.x, y=yi)
                    if o.exists():
                        o.delete()
                    OthelloWhiteBlock.objects.create(x=self.x, y=yi)
                break


class OthelloBlackBlock(Block):
    typestr = "othb"

    def on_place(self):

        for x in range(self.x, self.x - 20):
            if OthelloBlackBlock.objects.filter(x=x, y=self.y).exists():
                for xi in range(x, self.x):
                    o = Block.objects.filter(x=xi, y=self.y)
                    if o.exists():
                        o.delete()
                    OthelloBlackBlock.objects.create(x=xi, y=self.y)
                break
        for x in range(self.x, self.x + 20):
            if OthelloBlackBlock.objects.filter(x=x, y=self.y).exists():
                for xi in range(x, self.x):
                    o = Block.objects.filter(x=xi, y=self.y)
                    if o.exists():
                        o.delete()
                    OthelloBlackBlock.objects.create(x=xi, y=self.y)
                break
        for y in range(self.y, self.y - 20):
            if OthelloBlackBlock.objects.filter(x=self.x, y=y).exists():
                for yi in range(y, self.y):
                    o = Block.objects.filter(x=self.x, y=yi)
                    if o.exists():
                        o.delete()
                    OthelloBlackBlock.objects.create(x=self.x, y=yi)
                break
        for y in range(self.y, self.y + 20):
            if OthelloBlackBlock.objects.filter(x=self.x, y=y).exists():
                for yi in range(y, self.y):
                    o = Block.objects.filter(x=self.x, y=yi)
                    if o.exists():
                        o.delete()
                    OthelloBlackBlock.objects.create(x=self.x, y=yi)
                break


class TNTBlock(Block):
    typestr ="tnt"

