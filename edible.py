import pygame as pg

# Just a simple class for me to store variables, represents both food and poison
class Edible():
    
    def __init__(self, x, y, r):
        self.position = pg.Vector2(x, y)
        self.r = r