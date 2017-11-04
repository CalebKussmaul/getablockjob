from django.db import models

import json
# Create your models here.

class Block(models.Model):
    type = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    x = models.IntegerField()
    y = models.IntegerField()
    cooldown = models.IntegerField()

    class Meta:
        unique_together = ('x', 'y',)
    health = models.FloatField()

    def __str__(self):

        out = {'type': self.type, 'color': self.color,'health':self.health,'x': self.x,'y': self.y,'cooldown': self.cooldown,}
        return json.dumps(out)

    def __json__(self):
        return {'type': self.type, 'color': self.color,'x': self.x,'y': self.y,'cooldown': self.cooldown,}

    def as_json(self):
        out = {'type': self.type, 'color': self.color, 'health': self.health, 'x': self.x, 'y': self.y,
               'cooldown': self.cooldown, }
        return out


# class Block():
#     def getColor(self):
#         return self.color
#
#     def getCord(self):
#         return self.cord
#
#     def getHealth(self):
#         return self.health
#
#     def getType(self):
#         return self.type
#
#     def setHealth(self, health):
#         self.health = health
#
#     def __init__(self, type, color, x, y,cooldown, health):
#         self.type = type
#         self.color = color
#         self.cord = (x,y)
#         self.health = 1.0
#         self.cooldown = cooldown
#         self.c
