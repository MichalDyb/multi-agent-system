#Import potrzebnych klas
from osbrain.agent import Agent
from classes.Window import *
from classes.Net import *
from classes.Field import *
from classes.Movement import *
from math import sqrt, pow

#Klasa Ball, której obiekt odwzorowuje piłkę na boisku
class Ball(Agent, Coordinate, Size, Movement):

    def on_init(self):
        self.setX(0)
        self.setY(0)
        self.setZ(0)
        self.setHeight(0)
        self.setWidth(0)
        self.xDir = 0
        self.yDir = 0
        self.xGoal = 0
        self.yGoal = 0
        # Ile razy piłka była dotknięta przez graczy na ich połowie
        self.recievedCounter = 0
        # Która drużyna ostatnia dotknęła piłki
        self.lastTouch = False
        # Liczba kroków, w których piłka wygrywa z grawitacją i porusza się do góry
        self.steps = 0

        self.mvDistance = 0
        self.hgDistance = 0


    # Settery
    def setLastTouch(self, lastTouch: bool) -> None:
        self.lastTouch = lastTouch

    def setSteps(self, steps: int) -> None:
        self.steps = steps

    def setMvDistance(self, fieldDistance: float) -> None:
        self.mvDistance = fieldDistance

    def setHgDistance(self, netDistance: float) -> None:
        self.hgDistance = netDistance

    def setRecievedCounter(self, recievedCounter: int) -> None:
        self.recievedCounter = recievedCounter

    # Gettery
    def getLastTouch(self) -> bool:
        return self.lastTouch

    def getSteps(self) -> int:
        return self.steps

    def getRecievedCounter(self) -> int:
        return self.recievedCounter

    def getMvDistance(self) -> float:
        return self.mvDistance

    def getHgDistance(self) -> float:
        return self.hgDistance

    # Skaluje rozmiar piłki
    def scaleWidth(self, width: float, fieldDistance: float, netDistance: float) -> None:
        self.setWidth(width * 0.009)
        self.setMvDistance(fieldDistance)
        self.setHgDistance(netDistance)

    # Ustawia początkowom pozycje piłki
    def startPosition(self, playerwidth: float, field: Field, set: bool) -> None:

        if set == False:
            self.setX(field.getX())
            self.setY(field.getY() + field.getHeight() * 0.875 - playerwidth)
        else:
            self.setX(field.getX() + field.getWidth())
            self.setY(field.getY() + field.getHeight() * 0.125 - playerwidth)

     # Metody dotyczące licznika ile razy piłka była dotknięta przez graczy na ich połowie
    def maxCount(self):
        self.recievedCounter = 3

    def resetCount(self) -> None:
        self.recievedCounter = 0

    def incCounter(self) -> None:
        self.recievedCounter = self.recievedCounter + 1

    def counterState(self) -> bool:
        if self.recievedCounter > 2:
            return True
        else:
            return False

    # Sprawdza czy piłka, wyleciała poza boisko
    def touchOut(self, screenWidth: float, screenHeight: float) -> bool:
        if self.getX() < 0 or self.getX() > screenWidth:
            return True
        if self.getY() < 0 or self.getY() > screenHeight:
            return True
        return False

    # Sprawdza czy piłka wylądowałą na boisku
    def touchField(self, field: Field) -> bool:
        if self.getX() - self.getWidth() >= 50 and self.getX() + self.getWidth() <= 50 + field.getWidth():
            if self.getY() - self.getWidth() >= 50 and self.getY() + self.getWidth() <= 50 + field.getHeight():
                return True
        return False

    # Sprawdza, po której stronie siatki jest piłka
    def touchHalf(self, net: Net) -> bool:
        if self.getX() <= net.getX():
            return False
        else:
            return True

    # Sprawdza czy piłka dotkneła ziemi
    def touchGround(self) -> bool:
        if self.getZ() - self.getWidth() > 0:
            return False
        else:
            return True

    # Sprawdza czy piłka dotknęła siatki
    def touchNet(self, net: Net) -> bool:
        if self.getZ() - self.getWidth() <= net.getZ():
            if net.getX() + self.getWidth() >= self.getX() >= net.getX() - self.getWidth():
                if self.getY() + self.getWidth() >= net.getY() and self.getY() - self.getWidth() <= net.getY() + net.getHeight():
                    return True
        return False

    # Oblicza zmienne kierunkowe dla podanych współrzędnych docelowych i ze względu, czy zagrywka ma być podaniem, czy atakiem
    def calculateDirection(self, xGoal: float, yGoal: float, high: bool) -> None:

        if self.getX() == xGoal and self.getY() == yGoal:
            return

        self.setXGoal(xGoal)
        self.setYGoal(yGoal)

        xDistance = abs(self.getX() - self.getXGoal())
        yDistance = abs(self.getY() - self.getYGoal())
        distance = xDistance + yDistance

        if self.getX() < self.getXGoal():
            self.setXDir(xDistance / distance)
        else:
            self.setXDir(xDistance / distance * (-1))

        if self.getY() < self.getYGoal():
            self.setYDir(yDistance / distance)
        else:
            self.setYDir(yDistance / distance * (-1))

    # Obliczenie czasu wznoszenia piłki
        dist = sqrt(pow(self.getX() - xGoal, 2) + pow(self.getY() - yGoal, 2))
        steps = dist / self.getMvDistance()
        stepsH = self.getZ() / self.getHgDistance()

        if high:
            self.setSteps(int(stepsH / 2 + (steps - stepsH) / 2))
        else:
            if steps >= 2.2 * stepsH:
                self.setSteps(int(stepsH / 2 + (steps - stepsH) / 2 * 0.1))
            elif steps >= 2 * stepsH:
                self.setSteps(int(stepsH / 2 + (steps - stepsH) / 2 * 0.25))
            elif steps >= 1.8 * stepsH:
                self.setSteps(int(stepsH / 2 + (steps - stepsH) / 2 * 0.45))
            else:
                self.setSteps(int(stepsH / 2 + (steps - stepsH) / 2 * 0.65))

    # Grawitacja działająca na piłkę, zmniejszająca jej wysokość przy każdym wywołaniu.
    def gravity(self) -> None:

        if self.getSteps() > 0:
            self.setSteps(self.getSteps() - 1)
            self.setZ(self.getZ() + self.getHgDistance())
            return

        if self.getZ() - self.getWidth() <= 0:
            self.setZ(0 + self.getWidth())
        elif self.getZ() - self.getWidth() < self.getHgDistance():
            self.setZ(0 + self.getWidth())
        else:
            self.setZ(self.getZ() - self.getHgDistance())

    # Porusza piłkę na podstawie kierunku określonego w Movement
    def move(self) -> None:

        self.gravity()

        if self.getXDir() == 0 and self.getYDir() == 0:
            return

        distance = self.getMvDistance() * 1.3

        if self.getXDir() != 0:
            self.setX(self.getX() + distance * self.getXDir())

        if self.getYDir() != 0:
            self.setY(self.getY() + distance * self.getYDir())