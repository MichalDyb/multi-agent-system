# Klasa Coordinate przechowująca współrzędne obiektu
class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    # Settery
    def setX(self, x: float) -> None:
        self.x = x

    def setY(self, y: float) -> None:
        self.y = y

    def setZ(self, z: float) -> None:
        self.z = z

    # Gettery
    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def getZ(self) -> float:
        return self.z

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False
