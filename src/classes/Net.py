# Import potrzebnych klas
from classes.Coordinate import *
from classes.Size import *


# Klasa Net, której obiekt odwzorowuje siatkę na boisku
class Net(Coordinate, Size):

    def __init__(self):
        self.distance = 0

    # Gettery
    def getDistance(self) -> float:
        return self.distance

    # Settery
    def setDisctance(self, distance: float):
        self.distance = distance

    #Skaluje rozmiary siatki
    def scaleNet(self, screenWidth: float, screenHeight: float) -> None:
        self.setX((screenWidth - 100) / 2 + 50 - 2.5)
        self.setY(50 + 5)
        self.setWidth(5)
        self.setHeight((screenHeight - 100) - 5 - 2.5)
        self.setZ(screenHeight / 3.7)
        self.distance = self.getZ() * 0.05