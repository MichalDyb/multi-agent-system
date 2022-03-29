# Klasa Size przechowująca rozmiary obiektu
class Size:
    def __init__(self):
        self.width = 0
        self.height = 0

    # Settery
    def setWidth(self, width: float) -> None:
        self.width = width

    def setHeight(self, height: float) -> None:
        self.height = height

    # Gettery
    def getWidth(self) -> float:
        return self.width

    def getHeight(self) -> float:
        return self.height

    def __eq__(self, other):
        if self.width == other.width and self.height == other.height:
            return True
        else:
            return False