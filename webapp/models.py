from django.db import models

import json
import random


class Block(models.Model):

    typestr = models.CharField(max_length=10)
    x = models.IntegerField()
    y = models.IntegerField()
    cooldown = models.IntegerField()
    health = models.FloatField()

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


class ColorBlock(Block):

    color = models.CharField(max_length=10)

    def __init__(self):
        self.typestr = "basic"
        super(ColorBlock, self).__init__()

    def as_json(self):
        out = super(ColorBlock, self).as_json()
        out.update({"color": self.color})


class GolBlock(Block):

    gol_cooldown = models.IntegerField()

    def __init__(self):
        self.typestr = "gol"
        super(GolBlock, self).__init__()


class MbsBlock(Block):
    mbs_cooldown = models.IntegerField()

    def __init__(self):
        self.typestr = "mbs"
        super(MbsBlock, self).__init__()


class NotEastBlock(Block):

    def __init__(self):
        self.typestr = "note"
        super(NotEastBlock, self).__init__()


class NotNorthBlock(Block):

    def __init__(self):
        self.typestr = "notn"
        super(NotNorthBlock, self).__init__()


class NotSouthBlock(Block):

    def __init__(self):
        self.typestr = "nots"
        super(NotSouthBlock, self).__init__()


class NotWestBlock(Block):

    def __init__(self):
        self.typestr = "notw"
        super(NotWestBlock, self).__init__()


class WireOnBlock(Block):

    def __init__(self):
        self.typestr = "wireon"
        super(WireOnBlock, self).__init__()


class WireOffBlock(Block):
    def __init__(self):
        self.typestr = "wireoff"
        super(WireOffBlock, self).__init__()


class OthelloWhiteBlock(Block):
    def __init__(self):
        self.typestr = "othw"
        super(OthelloWhiteBlock, self).__init__()


class OthelloBlackBlock(Block):
    def __init__(self):
        self.typestr = "othb"
        super(OthelloBlackBlock, self).__init__()


class TNTBlock(Block):
    def __init__(self):
        self.typestr = "tnt"
        super(TNTBlock, self).__init__()
