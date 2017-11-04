from django.db import models


# Create your models here.

class Block(models.Model):
    type = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    x = models.IntegerField()
    y = models.IntegerField()

    class Meta:
        unique_together = ('x', 'y',)
    health = models.FloatField()


class Block():
    def getColor(self):
        return self.color

    def getCord(self):
        return self.cord

    def getHealth(self):
        return self.health

    def getType(self):
        return self.type

    def setHealth(self, health):
        self.health = health

    def __init__(self, type, color, x, y ):
        self.type = type
        self.color = color
        self.cord = (x,y)
        self.health = 1.0
