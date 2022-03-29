# Klasa Coordinate przechowująca współrzędne docelowe i zmienne kierunkowe
class Movement:

    def __init__(self):
        self.xDir = 0
        self.yDir = 0
        self.xGoal = 0
        self.yGoal = 0

    # Settery
    def setXDir(self, xDir: float) -> None:
        self.xDir = xDir

    def setYDir(self, yDir: float) -> None:
        self.yDir = yDir

    def setXGoal(self, xGoal: float) -> None:
        self.xGoal = xGoal

    def setYGoal(self, yGoal: float) -> None:
        self.yGoal = yGoal

    # Gettery
    def getXDir(self) -> float:
        return self.xDir

    def getYDir(self) -> float:
        return  self.yDir

    def getXGoal(self) -> float:
        return self.xGoal

    def getYGoal(self) -> float:
        return self.yGoal

    def __eq__(self, other):
        if self.xDir == other.xDir and self.yDir == other.yDir and self.xGoal == other.xGoal and self.yGoal == other.yGoal:
            return True
        else:
            return False
