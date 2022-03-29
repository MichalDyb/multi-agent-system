# Klasa Score, pełniąca funkcje tablicy wyników.
import random

class Score():
    def __init__(self):
        self.scoreBlue = 0
        self.scoreRed = 0
        self.winSetsBlue = 0
        self.winSetsRed = 0
        # Kto obecnie serwuje
        self.who = False
        # Czy gra jest włączona
        self.gameState = 0

    # Settery
    def setScoreBlue(self, scoreBlue: int) -> None:
        self.scoreBlue = scoreBlue

    def setScoreRed(self, scoreRed: int) -> None:
        self.scoreRed = scoreRed

    def setWinSetsBlue(self, winSetsBlue: int) -> None:
        self.winSetsBlue = winSetsBlue

    def setWinSetsRed(self, winSetsRed: int) -> None:
        self.winSetsRed = winSetsRed

    def setWho(self, who: bool) -> None:
        self.who = who

    def setGameState(self, game: int) -> None:
        self.gameState = game

    # Gettery
    def getScoreBlue(self) -> int:
        return self.scoreBlue

    def getScoreRed(self) -> int:
        return self.scoreRed

    def getWinSetsBlue(self) -> int:
        return self.winSetsBlue

    def getWinSetsRed(self) -> int:
        return self.winSetsRed

    def getWho(self) -> bool:
        return self.who

    def getGameState(self) -> int:
        return self.gameState

    # Dodaje punkty do drużyny określonej w warunku
    def addPoint(self, team: bool) -> None:
        if team:
            self.setScoreBlue(self.getScoreBlue() + 1)
        else:
            self.setScoreRed(self.getScoreRed() + 1)

    # Sprawdza czy, któraś z drużyn wygrała set, jeśli nie zwraca None
    def winSet(self) -> int:

        setPoints = 8
        if self.winSetsRed + self.winSetsBlue == 4:
            setPoints = 6

        if self.scoreRed >= setPoints and self.scoreBlue < self.scoreRed:
            return 0
        if self.scoreBlue >= setPoints and self.scoreRed < self.scoreBlue:
            return 1
        return -1

    # Sprawdza czy, któraś z drużyn wygrałą rozgrywke
    def winGame(self) -> bool:
        if self.winSetsRed == 3:
            self.setGameState(5)
            return True
        elif self.winSetsBlue == 3:
            self.setGameState(5)
            return True
        return False

    def __eq__(self, other):
        if self.scoreBlue == other.scoreBlue and self.scoreRed == other.scoreRed and self.winSetsBlue == other.winSetsBlue and self.winSetsRed == other.winSetsRed and self.who == other.who:
            return True
        else:
            return False

    # Resetuje wyniki dla nowego seta
    def resetScore(self) -> None:
        self.scoreRed = self.scoreBlue = 0

    # Resetuje wyniki i losuje, która drużyna będzie serwować
    def newGame(self) -> None:
        self.scoreRed = self.scoreBlue = 0
        self.winSetsRed = self.winSetsBlue = 0
        self.who = random.choice([True, False])