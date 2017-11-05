from django.db import models
from django.db.models.signals import post_save

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
        if Block.objects.filter(x=self.x + 1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x + 1, y=self.y))
        if Block.objects.filter(x=self.x - 1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x - 1, y=self.y))
        return neighbors

    def get_empty_neighbors(self):
        neighbors = list()
        if not Block.objects.filter(x=self.x, y=self.y + 1).exists():
            neighbors.append((self.x, self.y + 1))
        if not Block.objects.filter(x=self.x, y=self.y - 1).exists():
            neighbors.append((self.x, self.y - 1))
        if not Block.objects.filter(x=self.x + 1, y=self.y).exists():
            neighbors.append((self.x + 1, self.y))
        if not Block.objects.filter(x=self.x - 1, y=self.y).exists():
            neighbors.append((self.x - 1, self.y))
        return neighbors

    def get_more_empty_neighbors(self):
        neighbors = list()
        if not Block.objects.filter(x=self.x, y=self.y + 1).exists():
            neighbors.append((self.x, self.y + 1))
        if not Block.objects.filter(x=self.x, y=self.y - 1).exists():
            neighbors.append((self.x, self.y - 1))
        if not Block.objects.filter(x=self.x + 1, y=self.y).exists():
            neighbors.append((self.x + 1, self.y))
        if not Block.objects.filter(x=self.x - 1, y=self.y).exists():
            neighbors.append((self.x - 1, self.y))

        if not Block.objects.filter(x=self.x + 1, y=self.y + 1).exists():
            neighbors.append((self.x + 1, self.y + 1))
        if not Block.objects.filter(x=self.x + 1, y=self.y - 1).exists():
            neighbors.append((self.x + 1, self.y - 1))
        if not Block.objects.filter(x=self.x - 1, y=self.y + 1).exists():
            neighbors.append((self.x - 1, self.y))
        if not Block.objects.filter(x=self.x - 1, y=self.y - 1).exists():
            neighbors.append((self.x - 1, self.y - 1))
        return neighbors

    def get_more_neighbors(self):
        neighbors = list()
        if Block.objects.filter(x=self.x, y=self.y + 1).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y + 1))
        if Block.objects.filter(x=self.x, y=self.y - 1).exists():
            neighbors.append(Block.objects.get(x=self.x, y=self.y - 1))
        if Block.objects.filter(x=self.x + 1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x + 1, y=self.y))
        if Block.objects.filter(x=self.x - 1, y=self.y).exists():
            neighbors.append(Block.objects.get(x=self.x - 1, y=self.y))

        if Block.objects.filter(x=self.x + 1, y=self.y + 1).exists():
            neighbors.append(Block.objects.get(x=self.x + 1, y=self.y + 1))
        if Block.objects.filter(x=self.x + 1, y=self.y - 1).exists():
            neighbors.append(Block.objects.get(x=self.x + 1, y=self.y - 1))
        if Block.objects.filter(x=self.x - 1, y=self.y + 1).exists():
            neighbors.append(Block.objects.get(x=self.x - 1, y=self.y + 1))
        if Block.objects.filter(x=self.x - 1, y=self.y - 1).exists():
            neighbors.append(Block.objects.get(x=self.x - 1, y=self.y - 1))
        return neighbors

    def is_powered_by_not(self):
        s = NotNorthBlock.objects.filter(x=self.x, y=self.y + 1)
        if s.exists() and not s.first().powered:
            return True
        n = NotSouthBlock.objects.filter(x=self.x, y=self.y - 1)
        if n.exists() and not n.first().powered:
            return True
        e = NotWestBlock.objects.filter(x=self.x + 1, y=self.y)
        if e.exists() and not e.first().powered:
            return True
        w = NotEastBlock.objects.filter(x=self.x - 1, y=self.y)
        if w.exists() and not w.first().powered:
            return True

        return False

    def get_connected_wires2(self, checked=set()):

        checked.add(self)
        unchecked = list()

        if WireBlock.objects.filter(x=self.x, y=self.y + 1).exists():
            o = WireBlock.objects.get(x=self.x, y=self.y + 1)
            if o not in checked:
                unchecked.append(o)
        if WireBlock.objects.filter(x=self.x, y=self.y - 1).exists():
            o = WireBlock.objects.get(x=self.x, y=self.y - 1)
            if o not in checked:
                unchecked.append(o)
        if WireBlock.objects.filter(x=self.x + 1, y=self.y).exists():
            o = WireBlock.objects.get(x=self.x + 1, y=self.y)
            if o not in checked:
                unchecked.append(o)
        if WireBlock.objects.filter(x=self.x - 1, y=self.y).exists():
            o = WireBlock.objects.get(x=self.x - 1, y=self.y)
            if o not in checked:
                unchecked.append(o)

        if len(unchecked) == 0:
            return {self}

        rest = {self}
        for blocks in unchecked:
            rest = rest.union(blocks.get_connected_wires2(checked))
        return rest


class BacteriaBlock(Block):

    typestr = "bacteria"

    def on_tick(self):
        if len(self.get_empty_neighbors()) == 0:
            return
        if random.randint(0, 50) == 1:
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
            else:
                BacteriaBlock.objects.create(x=coord[0], y=coord[1])


class ColorBlock(Block):
    color = models.CharField(max_length=10)
    typestr = "basic"

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})
        return out


class GolBlock(Block):
    gol_cooldown = models.IntegerField(default=5)
    add_next_tick = dict()
    remove_next_tick = False
    typestr = "gol"

    def on_tiick(self):

        if self.gol_cooldown > 0:
            self.gol_cooldown -= 1
            self.save()

        neighbors = [x for x in self.get_more_neighbors() if x.typestr == "gol"]

        remove = self.remove_next_tick
        add = self.add_next_tick.copy()
        self.add_next_tick = dict()

        if len(neighbors) < 2 or len(neighbors) > 3:
            self.remove_next_tick = True

        for coords in self.get_more_empty_neighbors():

            neighbor_count = 0
            if GolBlock.objects.filter(x=coords[0], y=coords[1] + 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0], y=coords[1] - 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0] + 1, y=coords[1]).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0] - 1, y=coords[1]).exists():
                neighbor_count += 1

            if GolBlock.objects.filter(x=coords[0]+1, y=coords[1] + 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0]+1, y=coords[1] - 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0]-1, y=coords[1] + 1).exists():
                neighbor_count += 1
            if GolBlock.objects.filter(x=coords[0]-1, y=coords[1] - 1).exists():
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
        s = WireBlock.objects.filter(x=self.x, y=self.y + 1)
        if s.exists():
            self.powered = s.first().powered
        n = WireBlock.objects.filter(x=self.x, y=self.y - 1)
        if n.exists():
            self.powered = n.first().powered
        # e = WireBlock.objects.filter(x=self.x + 1, y=self.y)
        # if e.exists():
        #     self.powered = e.first().powered
        w = WireBlock.objects.filter(x=self.x - 1, y=self.y)
        if w.exists():
            self.powered = w.first().powered
        self.save()


class NotNorthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "notn"

    def on_tick(self):
        s = WireBlock.objects.filter(x=self.x, y=self.y + 1)
        if s.exists():
            self.powered = s.first().powered
        # n = WireBlock.objects.filter(x=self.x, y=self.y - 1)
        # if n.exists():
        #     self.powered = n.first().powered
        e = WireBlock.objects.filter(x=self.x + 1, y=self.y)
        if e.exists():
            self.powered = e.first().powered
        w = WireBlock.objects.filter(x=self.x - 1, y=self.y)
        if w.exists():
            self.powered = w.first().powered
        self.save()


class NotSouthBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "nots"

    def on_tick(self):
        s = WireBlock.objects.filter(x=self.x, y=self.y + 1)
        if s.exists():
            self.powered = s.first().powered
        # n = WireBlock.objects.filter(x=self.x, y=self.y - 1)
        # if n.exists():
        #     self.powered = n.first().powered
        e = WireBlock.objects.filter(x=self.x + 1, y=self.y)
        if e.exists():
            self.powered = e.first().powered
        w = WireBlock.objects.filter(x=self.x - 1, y=self.y)
        if w.exists():
            self.powered = w.first().powered
        self.save()


class NotWestBlock(Block):
    powered = models.BooleanField(default=False)
    typestr = "notw"

    def on_tick(self):
        s = WireBlock.objects.filter(x=self.x, y=self.y + 1)
        if s.exists():
            self.powered = s.first().powered
        n = WireBlock.objects.filter(x=self.x, y=self.y - 1)
        if n.exists():
            self.powered = n.first().powered
        e = WireBlock.objects.filter(x=self.x + 1, y=self.y)
        if e.exists():
            self.powered = e.first().powered
        # w = WireBlock.objects.filter(x=self.x - 1, y=self.y)
        # if w.exists():
        #     self.powered = w.first().powered
        # self.save()


class WireBlock(Block):

    ticked = models.BooleanField(default=False)
    powered = models.BooleanField(default=False)
    typestr = "wireoff"

    def as_json(self):
        out = super(WireBlock, self).as_json()
        out.update({"powered": self.powered})
        return out

    def on_tick(self):
        if self.ticked:
            self.ticked = False
            return
        wires = self.get_connected_wires2(set())
        is_powered = False
        for wire in wires:
            wire.ticked = True
            if wire.is_powered_by_not():
                is_powered = True
                break
        for wire in wires:
            wire.typestr = "wireon" if is_powered else "wireoff"
            wire.powered = is_powered
            wire.save()


class OthelloWhiteBlock(Block):
    typestr = "othw"

    ignorehorizontal = models.BooleanField(default=False)
    ignorevertical = models.BooleanField(default=False)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return

        if not instance.ignorehorizontal:
            for x in reversed(range(instance.x - 20, instance.x)):
                if Block.objects.filter(x=x, y=instance.y).exists():
                    if OthelloWhiteBlock.objects.filter(x=x, y=instance.y).exists():
                        for xi in range(x, instance.x):
                            if OthelloBlackBlock.objects.filter(x=xi, y=instance.y).exists():
                                OthelloBlackBlock.objects.get(x=xi, y=instance.y).delete()
                            if not Block.objects.filter(x=xi, y=instance.y).exists():
                                OthelloWhiteBlock.objects.create(x=xi, y=instance.y, ignorehorizontal=True)
                    break
            for x in range(instance.x, instance.x + 20):
                if Block.objects.filter(x=x, y=instance.y).exists():
                    if OthelloWhiteBlock.objects.filter(x=x, y=instance.y).exists():
                        for xi in range(x, instance.x):
                            if OthelloBlackBlock.objects.filter(x=xi, y=instance.y).exists():
                                OthelloBlackBlock.objects.get(x=xi, y=instance.y).delete()
                            if not Block.objects.filter(x=xi, y=instance.y).exists():
                                OthelloWhiteBlock.objects.create(x=xi, y=instance.y, ignorehorizontal=True)
                    break
        if not instance.ignorevertical:
            for y in reversed(range(instance.y - 20, instance.y)):
                if Block.objects.filter(x=instance.x, y=y).exists():
                    if OthelloWhiteBlock.objects.filter(x=instance.x, y=y).exists():
                        for yi in range(y, instance.y):
                            if OthelloBlackBlock.objects.filter(x=instance.x, y=yi).exists():
                                OthelloBlackBlock.objects.get(x=instance.x, y=yi).delete()
                            if not Block.objects.filter(x=instance.x, y=yi).exists():
                                OthelloWhiteBlock.objects.create(x=instance.x, y=yi, ignorevertical=True)
                    break
            for y in range(instance.y, instance.y + 20):
                if Block.objects.filter(x=instance.x, y=y).exists():
                    if OthelloWhiteBlock.objects.filter(x=instance.x, y=y).exists():
                        for yi in range(y, instance.y):
                            if OthelloBlackBlock.objects.filter(x=instance.x, y=yi).exists():
                                OthelloBlackBlock.objects.get(x=instance.x, y=yi).delete()
                            if not Block.objects.filter(x=instance.x, y=yi).exists():
                                OthelloWhiteBlock.objects.create(x=instance.x, y=yi, ignorevertical=True)
                    break


post_save.connect(OthelloWhiteBlock.post_create, sender=OthelloWhiteBlock)


class OthelloBlackBlock(Block):
    typestr = "othb"
    ignorehorizontal = models.BooleanField(default=False)
    ignorevertical = models.BooleanField(default=False)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        print("hello I live at "+str(instance.x)+str(instance.y))

        if not instance.ignorehorizontal:
            for x in reversed(range(instance.x - 20, instance.x-1)):
                if Block.objects.filter(x=x, y=instance.y).exists():
                    if OthelloBlackBlock.objects.filter(x=x, y=instance.y).exists():
                        print("abc: " + str(x) + " to " + str(instance.x))
                        for xi in range(x, instance.x):
                            if OthelloWhiteBlock.objects.filter(x=xi, y=instance.y).exists():
                                OthelloWhiteBlock.objects.get(x=xi, y=instance.y).delete()
                            if not Block.objects.filter(x=xi, y=instance.y).exists():
                                OthelloBlackBlock.objects.create(x=xi, y=instance.y, ignorehorizontal=True)
                    break
            for x in range(instance.x+1, instance.x + 20):
                if Block.objects.filter(x=x, y=instance.y).exists():
                    if OthelloBlackBlock.objects.filter(x=x, y=instance.y).exists():
                        print("abc: " + str(x) + " to " + str(instance.x))
                        for xi in range(x, instance.x):
                            if OthelloBlackBlock.objects.filter(x=xi, y=instance.y).exists():
                                OthelloWhiteBlock.objects.get(x=xi, y=instance.y).delete()
                            if not Block.objects.filter(x=xi, y=instance.y).exists():
                                OthelloBlackBlock.objects.create(x=xi, y=instance.y, ignorehorizontal=True)
                    break
        if not instance.ignorevertical:
            for y in reversed(range(instance.y - 20, instance.y-1)):
                if Block.objects.filter(x=instance.x, y=y).exists():
                    if OthelloBlackBlock.objects.filter(x=instance.x, y=y).exists():
                        print("abc: " + str(y) + " to " + str(instance.y))
                        for yi in range(y, instance.y):
                            if OthelloWhiteBlock.objects.filter(x=instance.x, y=yi).exists():
                                OthelloWhiteBlock.objects.get(x=instance.x, y=yi).delete()
                            if not Block.objects.filter(x=instance.x, y=yi).exists():
                                OthelloBlackBlock.objects.create(x=instance.x, y=yi, ignorevertical=True)
                    break
            for y in range(instance.y + 1, instance.y + 20):
                if Block.objects.filter(x=instance.x, y=y).exists():
                    if OthelloBlackBlock.objects.filter(x=instance.x, y=y).exists():
                        print("abc: " + str(y) + " to " + str(instance.y))
                        for yi in range(y, instance.y):
                            if OthelloWhiteBlock.objects.filter(x=instance.x, y=yi).exists():
                                OthelloWhiteBlock.objects.get(x=instance.x, y=yi).delete()
                            if not Block.objects.filter(x=instance.x, y=yi).exists():
                                OthelloBlackBlock.objects.create(x=instance.x, y=yi, ignorevertical=True)
                    break


post_save.connect(OthelloBlackBlock.post_create, sender=OthelloBlackBlock)


class TNTBlock(Block):
    typestr ="tnt"

