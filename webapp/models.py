from django.db import models


# Create your models here.

class Block():
    def getColor(self):
        return self.color

    def getCord(self):
        return self.cord

    def getHealth(self):
        return self.health

    def setHealth(self, health):
        self.health = health

    def __init__(self, color, cord):
        self.color = color
        self.cord = cord
        self.health = 1.0
