# Import potrzebnych klas
import pygame
from classes.Ball import *
from classes.Net import *
from classes.Score import *
from os import path

# Klasa przechowująca okno i informacje o oknie rozgrywki
class Window(Size):

    def __init__(self):
        self.screen = 0
        self.description = "Volleyball Multi-Agent 007"
        self.graphicsPath = path.join(path.split(path.dirname(__file__))[0], "graphics")
        self.iconPath = path.join(self.graphicsPath, "logo.png")
        self.WHITE = (255,255,255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

    # Tworzy i wyswietla okno
    def createScreen(self) -> None:
        # Inicjalizuje wszystkie moduły pygame
        pygame.init()
        # Zmiana opisu okna
        pygame.display.set_caption(self.description)
        # Zmiana ikony okna
        pygame.display.set_icon(pygame.image.load(self.iconPath))
        # Pobiera rozdzielczosc monitora i zapisuje do pamieci obiektu
        resolution = pygame.display.Info()
        self.setWidth(resolution.current_w)
        self.setHeight(resolution.current_h)
        # Tworzy i wyświetla nowe okno
        self.screen = pygame.display.set_mode((self.getWidth() - 100, self.getHeight() - 100), pygame.RESIZABLE)
        self.scaleScreen()

    # Skaluje okno
    def scaleScreen(self) -> None:
        # Pobiera rozdzielczosc monitora i zapisuje do pamieci obiektu
        resolution = pygame.display.Info()
        if resolution.current_w < 800:
            self.setWidth(800)
            self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        else:
            self.setWidth(resolution.current_w)
        if resolution.current_h < 600:
            self.setHeight(600)
            self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        else:
            self.setHeight(resolution.current_h)

    # Check screen
    def checkScreen(self) -> bool:
        resolution = pygame.display.Info()
        if resolution.current_w < 800:
            return True
        if resolution.current_h < 600:
            return True
        return False

    # Wylacza okno
    def closeScreen(self) -> None:
        pygame.display.quit()

    # Rysuje tło
    def drawBackground(self, red: int, green: int, blue: int) -> None:
        if red < 0 or red > 255:
            red = 125
        if green < 0 or green > 255:
            green = 125
        if blue < 0 or blue > 255:
            blue = 125
        background_color = (red, green, blue)
        self.screen.fill(background_color)

    # Rysuje prostokąt wypełniony na ekranie na podanej pozycji oraz o podanej wielkości
    def drawRect(self, x: float, y: float, w: float, h: float, color: tuple) -> None:
        pygame.draw.rect(self.screen, color, (x,y,w,h))

    # Rysuje prostokąt pusty na ekranie na podanej pozycji oraz o podanej wielkości
    def drawField(self, x: float, y: float, w: float, h: float) -> None:
        pygame.draw.line(self.screen, self.WHITE, (x,y), (x + w, y), width = 5)
        pygame.draw.line(self.screen, self.WHITE, (x, y + h), (x + w, y + h), width=5)
        pygame.draw.line(self.screen, self.WHITE, (x, y), (x, y + h), width=5)
        pygame.draw.line(self.screen, self.WHITE, (x + w, y), (x + w, y + h), width=5)
        pygame.draw.line(self.screen, self.WHITE, (x + w / 2 - w / 6, y), (x + w / 2 - w / 6, y + h), width=3)
        pygame.draw.line(self.screen, self.WHITE, (x + w / 2 + w / 6, y), (x + w / 2 + w / 6, y + h), width=3)
        self.drawEmptyCircle(x + w / 2, y + h / 2, h * 0.15)

    def drawNet(self, x: float, y: float, w: float, h: float) -> None:
        pygame.draw.line(self.screen, self.BLACK, (x, y), (x, y + h), width=2)

    # Rysuje koło na ekranie na podanej pozycji oraz o podanym promieniu
    def drawCircle(self, x: float, y: float, r: float, R: int, G: int, B: int) -> None:
        pygame.draw.circle(self.screen, (R, G, B), (x, y), r)

    # Rysuje okrąg na ekranie na podanej pozycji oraz o podanym promieniu
    def drawEmptyCircle(self, x: float, y: float, r: float, width = 5) -> None:
        pygame.draw.circle(self.screen, self.WHITE, (x, y), r, width)

    # Renderuje zadany tekst na ekranie w zadanej pozycji
    def printText(self, text, x: float, y: float, fontSize: int, fontName: str, color: tuple) -> None:
        pygame.font.init()
        font = pygame.font.SysFont(fontName, fontSize)
        rtext = font.render(text, False, color)
        self.screen.blit(rtext, (x, y))
        return None

    # Renderuje graczy na ekranie
    def renderPlayers(self, team: list, R :int, G: int, B: int) -> None:
        for i in team:
            self.drawCircle(i.getX(), i.getY(), i.getWidth(), R, G, B)

    # Renderuje piłkę na ekranie
    def renderBall(self, ball: Ball, net: Net) -> None:
        if ball.getZ() > net.getZ():
            self.drawCircle(ball.getX(), ball.getY(), ball.getWidth(), 75, 75, 255)
        elif ball.getZ() < net.getZ() and ball.getZ() > (0 + ball.getWidth()):
            self.drawCircle(ball.getX(), ball.getY(), ball.getWidth(), 75, 255, 75)
        else:
            self.drawCircle(ball.getX(), ball.getY(), ball.getWidth(), 255, 75, 75)
        self.drawEmptyCircle(ball.getX(), ball.getY(), ball.getWidth(), 2)

    # Renderuje tablicę wyników
    def renderScore(self, score: Score) -> None:
        center = self.getWidth()/2
        self.drawRect(center - 75, 10, 150, 30, self.WHITE)
        self.printText(str(score.getScoreRed()), center - 60, 10, 28, 'Liberation Serif', self.RED)
        self.printText(str(score.getWinSetsRed()), center - 25, 10, 22, 'Liberation Serif', self.RED)
        self.printText(str(score.getWinSetsBlue()), center + 10, 10, 22, 'Liberation Serif', self.BLUE)
        self.printText(str(score.getScoreBlue()), center + 40, 10, 28, 'Liberation Serif', self.BLUE)

    #Wyswietlajaca wiadomosc i wysrodkowujaca ja w elemencie
    def drawMessage(self, color, elementX, elementWidth, elementY, elementHeight, message, fontSize, offsetX = 0, offsetY = 0, font = "arial") -> None:
        #Ustala format czcionki
        font = pygame.font.SysFont(font, int(elementHeight * 0.09 * fontSize))
        #Renderuje wiadomosc
        message = font.render(message, True, color)
        #Pobiera wymiary wiadomosci
        message_field = message.get_rect()
        #Ustala srodek wiadomosci
        message_field.center = (elementX + int(elementWidth / 2) + int(elementWidth / 2 * offsetX * 0.1), elementY + int(elementHeight / 2) + int(elementHeight / 2 * offsetY * 0.1))
        #Wyswietla wiadomosc, w odpowiadajacym jej miejscu
        self.screen.blit(message, message_field)

    # Renderuje wiadomosc powitalną
    def renderMenuMessage(self) -> None:
        self.drawMessage(self.BLACK, 0, self.getWidth(), 0, self.getHeight(), "Naciśnij ESC: wyłącz aplikację.", 0.9, 0, -1)
        self.drawMessage(self.BLACK, 0, self.getWidth(), 0, self.getHeight(), "Naciśnij ENTER: rozpocznij nową gre.", 0.9, 0, 1)

    # Renderuje wiadomosc z zakończonej rozgrywki
    def renderEndMessage(self, score: Score) -> None:
        self.renderScore(score)

        if(score.getWinSetsRed() == 3):
            self.drawMessage(self.RED, 0, self.getWidth(), 0, self.getHeight(), "Wygrała drużyna czerwona.",0.9, 0, -3)
        elif (score.getWinSetsBlue() == 3):
            self.drawMessage(self.BLUE, 0, self.getWidth(), 0, self.getHeight(), "Wygrała drużyna niebieska.", 0.9, 0, -3)
        else:
            self.drawMessage(self.BLACK, 0, self.getWidth(), 0, self.getHeight(), "Rozgrywka zakończyła się nieprawidłowo.", 0.8, 0, -3)

        self.drawMessage(self.BLACK, 0, self.getWidth(), 0, self.getHeight(), "Naciśnij ESC: wyłącz aplikację.", 0.9, 0, -1)
        self.drawMessage(self.BLACK, 0, self.getWidth(), 0, self.getHeight(), "Naciśnij ENTER: rozpocznij nową gre.", 0.9, 0,  1)