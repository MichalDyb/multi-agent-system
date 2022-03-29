# Import potrzebnych klas
from classes.Coordinate import *
from classes.Size import *

# Klasa Field, której obiekt wyznacza wymiary boiska do gry
class Field(Coordinate, Size):

    def __init__(self):
        self.distance = 0

    # Gettery
    def getDistance(self) -> float:
        return self.distance

    # Settery
    def setDisctance(self, distance: float):
        self.distance = distance

    # Skaluje pole do gry
    def scaleField(self, screenWidth: float, screenHeight: float) -> None:
        self.setWidth(screenWidth - 100)
        self.setHeight(screenHeight - 100)
        self.setX(50)
        self.setY(50)
        self.distance = self.getWidth() * 0.02

