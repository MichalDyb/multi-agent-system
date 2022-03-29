from osbrain.agent import Agent, run_agent
from classes.Ball import *
from classes.Field import *
from classes.Util import *
from classes.Movement import *
import random
from math import sqrt, pow

class Player(Agent, Movement):

    def on_init(self):
        random.seed()
        self.coordinate = Coordinate()
        self.size = Size()
        self.startX = 0
        self.startY = 0
        self.speed = random.randint(1, 5)
        self.skill = random.randint(1, 5)
        self.xDir = 0
        self.yDir = 0
        self.xGoal = 0
        self.yGoal = 0
        self.mvDistance = 0

    def getStartX(self) -> float:
        return self.startX

    def getStartY(self) -> float:
        return self.startY

    def getCoordinate(self) -> Coordinate:
        return self.coordinate

    def getSize(self) -> Size:
        return self.size

    def getSpeed(self) -> int:
        return self.speed

    def getSkill(self) -> int:
        return self.skill

    def getMvDistance(self) -> float:
        return self.mvDistance

    def getName(self) -> str:
        return self.name

    def setMvDistance(self, fieldDistance: float) -> None:
        self.mvDistance = fieldDistance

    def setCoordinate(self, newCoordinate: Coordinate) -> None:
        self.coordinate = newCoordinate
        return None

    def setSize(self, newSize: Size) -> None:
        self.size = newSize
        return None

    def setSpeed(self, newSpeed: int) -> None:
        self.speed = newSpeed
        return None

    def setSkill(self, newSkill: int) -> None:
        self.skill = newSkill
        return None

    def setX(self, x: float) -> None:
        self.coordinate.setX(x)

    def setStartX(self, startX: float) -> None:
        self.startX = startX

    def setY(self, y: float) -> None:
        self.coordinate.setY(y)

    def setStartY(self, startY: float) -> None:
        self.startY = startY

    def setZ(self, z: float) -> None:
        self.coordinate.setZ(z)

    def getX(self) -> float:
        return self.coordinate.getX()

    def getY(self) -> float:
        return self.coordinate.getY()

    def getZ(self) -> float:
        return self.coordinate.getZ()

    def setWidth(self, width: float) -> None:
        self.size.setWidth(width)

    def setHeight(self, height: float) -> None:
        self.size.setHeight(height)

    def getWidth(self) -> float:
        return self.size.getWidth()

    def getHeight(self) -> float:
        return self.size.getHeight()

    def getName(self) -> str:
        return self.name

    # Sprawdza czy obiekty klasy Player są takie same
    def __eq__(self, other):
        if self.coordinate == other.coordinate and self.size == other.size and self.skill == other.skill and self.speed == other.speed:
            return True
        else:
            return False

    # Skaluje rozmiar gracza
    def scalePlayer(self, width: float) -> None:
        self.setWidth(width * 0.0125)
        self.setHeight(width / 10)

    # Sprawdza czy gracz jest w zasiegu pilki, (może wykonać jakąś akcję)
    def ballRange(self, ball: Ball) -> bool:
        if ball.getZ() - ball.getWidth() <= self.getHeight() + self.getHeight() * 0.8:
            if self.getX() + self.getWidth() >= ball.getX() - ball.getWidth() and self.getX() - self.getWidth() <= ball.getX() + ball.getWidth():
                if self.getY() + self.getWidth() >= ball.getY() - ball.getWidth() and self.getY() - self.getWidth() <= ball.getY() + ball.getWidth():
                    return True
        return False

    # Zwraca czy akcja gracza zakonczyla sie pomyslnie np. odbicie na podstawie prawdopodobienstwa z uwzględnieniem umiejętności gracza
    def getActionState(self) -> bool:
        rand = random.randint(1, 100)
        if rand > 92 + self.getSkill():
            return False
        return True

    # Oblicza zmienne kierunkowe dla podanych współrzędnych docelowych
    def calculateDirection(self, xGoal: float, yGoal: float) -> None:

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

    # Porusza gracza na podstawie kierunku określonego w Movement
    def move(self) -> None:

        if self.getXDir() == 0 and self.getYDir() == 0:
            return

        if sqrt(pow(self.getX() - self.getXGoal(), 2) + pow(self.getY() - self.getYGoal(), 2)) < self.getMvDistance():
            self.setX(self.getXGoal())
            self.setY(self.getYGoal())
            self.setXDir(0)
            self.setYDir(0)

        if self.getXDir() != 0:
            self.setX(self.getX() + self.getMvDistance() * self.getXDir())

        if self.getYDir() != 0:
            self.setY(self.getY() + self.getMvDistance() * self.getYDir())

    # Zwraca do jakiej drużyny należy gracz
    def getTeam(self) -> bool:
        if "Red" in self.name:
            return False
        else:
            return True

# Tworzy i uruchamia agentów tworzących daną drużyne
def createTeam(teamName: str) -> list:
    team = []
    i = 0
    while i < 5:
        team.append(run_agent(teamName + str(i), base=Player))
        i += 1
    if len(team) < 1:
        return []
    else:
        return team

# Skaluje rozmiar druzyny i ustawia pozycje początkowe
def scaleTeam(teamRed: list, teamBlue, field: Field) -> None:
    for i in teamRed:
        i.scalePlayer(field.getWidth())
        i.setMvDistance(field.getDistance() * (1 - i.getSpeed() / 100))
    for i in teamBlue:
        i.scalePlayer(field.getWidth())
        i.setMvDistance(field.getDistance() * (1 - i.getSpeed() / 100))

    teamRed[0].setStartY(field.getY() + field.getHeight() * 0.125 - teamRed[0].getWidth())
    teamRed[0].setStartX(field.getX() + field.getWidth() * 0.425 - teamRed[0].getWidth())
    teamRed[1].setStartY(field.getY() + field.getHeight() * 0.875 - teamRed[1].getWidth())
    teamRed[1].setStartX(field.getX() + field.getWidth() * 0.425 - teamRed[1].getWidth())
    teamRed[2].setStartY(field.getY() + field.getHeight() * 0.125 - teamRed[2].getWidth())
    teamRed[2].setStartX(field.getX() + field.getWidth() * 0.125 - teamRed[2].getWidth())
    teamRed[3].setStartY(field.getY() + field.getHeight() * 0.875 - teamRed[3].getWidth())
    teamRed[3].setStartX(field.getX() + field.getWidth() * 0.125 - teamRed[3].getWidth())
    teamRed[4].setStartY(field.getY() + field.getHeight() * 0.5 - teamRed[4].getWidth())
    teamRed[4].setStartX(field.getX() + field.getWidth() * 0.25 - teamRed[4].getWidth())

    teamBlue[0].setStartY(field.getY() + field.getHeight() * 0.125 - teamBlue[0].getWidth())
    teamBlue[0].setStartX(field.getX() + field.getWidth() * 0.6 - teamBlue[0].getWidth())
    teamBlue[1].setStartY(field.getY() + field.getHeight() * 0.875 - teamBlue[1].getWidth())
    teamBlue[1].setStartX(field.getX() + field.getWidth() * 0.6 - teamBlue[1].getWidth())
    teamBlue[2].setStartY(field.getY() + field.getHeight() * 0.125 - teamBlue[2].getWidth())
    teamBlue[2].setStartX(field.getX() + field.getWidth() * 0.875 - teamBlue[2].getWidth())
    teamBlue[3].setStartY(field.getY() + field.getHeight() * 0.875 - teamBlue[3].getWidth())
    teamBlue[3].setStartX(field.getX() + field.getWidth() * 0.875 - teamBlue[3].getWidth())
    teamBlue[4].setStartY(field.getY() + field.getHeight() * 0.5 - teamBlue[4].getWidth())
    teamBlue[4].setStartX(field.getX() + field.getWidth() * 0.75 - teamBlue[4].getWidth())

# Ustawia początkowo pozycje graczy do serowania
def startPosition(teamRed: list, teamBlue: list,  field: Field, set: bool) -> None:

    for i in teamRed:
        i.setX(i.getStartX())
        i.setY(i.getStartY())
    for i in teamBlue:
        i.setX(i.getStartX())
        i.setY(i.getStartY())

    if set == False:
        teamRed[3].setX(field.getX())
    else:
        teamBlue[2].setX(field.getX() + field.getWidth())

# Ustawia nowe umiejętności i prędkość dla graczy
def newSkills(teamLeft: list, teamRight: list) -> None:
    for i in teamLeft:
        i.setSkill(random.randint(1, 5))
        i.setSpeed(random.randint(1, 5))

    for i in teamRight:
        i.setSkill(random.randint(1, 5))
        i.setSpeed(random.randint(1, 5))
