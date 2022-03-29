# Import wymaganych bibliotek
from classes.Window import *
from classes.Player import *
from classes.Ball import *
from osbrain import run_agent
from osbrain import run_nameserver
from classes.Util import *
from time import sleep

def log_message_players(self, message: str):
    header = decodeJSON(message)
    data = header["DATA"]

    if self.name == header["FOR"] or "All" == header["FOR"] or "Players" == header["FOR"]:

        if header["MSG_TYPE"] == "ALL_MV":
            self.move()

        if header["MSG_TYPE"] == "PL_SERVE":
            if self.getActionState():
                self.log_info("Gracz zaserwował piłkę w kierunku x = " + str(data["X"]) + ", y = " + str(data["Y"]))
                self.calculateDirection(self.getStartX(), self.getStartY())

                self.send('server', encodeJSON(buildDict("BL_SERVE", "Ball", {
                    "X": data["X"],
                    "Y": data["Y"],
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

            else:
                x = self.getX() + random.randint(-3, 3) * self.getWidth()
                y = self.getY() + random.randint(-3, 3) * self.getWidth()
                self.log_info("Gracz popełnił pomyłkę i zaserwował piłkę w kierunku x = " + str(x) + ", y = " + str(y))
                self.calculateDirection(self.getStartX(), self.getStartY())

                self.send('server', encodeJSON(buildDict("BL_SERVE", "Ball", {
                    "X": x,
                    "Y": y,
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

        if header["MSG_TYPE"] == "PL_DIR":
            self.log_info("Gracz przemieszcza się w kierunku  x = " + str(data["X"]) + ", y = " + str(data["Y"]))
            self.calculateDirection(data["X"], data["Y"])

        if header["MSG_TYPE"] == "PL_PS":
            if self.getActionState():
                self.log_info("Gracz podał piłkę do gracza (" + str(data["P"]) + ") w kierunku x = " + str(data["X"]) + ", y = " + str(data["Y"]))
                self.send('server', encodeJSON(buildDict("BL_PS", "Ball", {
                    "X": data["X"],
                    "Y": data["Y"],
                    "H": self.getHeight(),
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

            else:
                x = data["X"] + self.getWidth() * random.randint(-3, 3)
                y = data["Y"] + self.getWidth() * random.randint(-3, 3)
                self.log_info("Gracz popełnił pomyłkę i podał piłkę do gracza (" + str(data["P"]) + ") w kierunku x = " + str(x) + ", y = " + str(y))
                self.send('server', encodeJSON(buildDict("BL_PS", "Ball", {
                    "X": x,
                    "Y": y,
                    "H": self.getHeight(),
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

                self.send('server', encodeJSON(buildDict("PL_DIR", "Player", {
                    "X": x,
                    "Y": y,
                    "P": data["P"]
                })), handler=log_message_players_reply)
            self.calculateDirection(self.getStartX(), self.getStartY())

        if header["MSG_TYPE"] == "PL_AT":
            if self.getActionState():
                self.log_info("Gracz zaatakował piłką w kierunku x = " + str(data["X"]) + ", y = " + str(data["Y"]))
                self.calculateDirection(self.getStartX(), self.getStartY())

                self.send('server', encodeJSON(buildDict("BL_AT", "Ball", {
                    "X": data["X"],
                    "Y": data["Y"],
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

            else:
                x = self.getX() + random.randint(-2, 2) * self.getWidth()
                y = self.getY() + random.randint(-2, 2) * self.getWidth()
                self.log_info("Gracz popełnił pomyłkę i zaatakował piłkę w kierunku x = " + str(x) + ", y = " + str(y))
                self.calculateDirection(self.getStartX(), self.getStartY())

                self.send('server', encodeJSON(buildDict("BL_AT", "Ball", {
                    "X": x,
                    "Y": y,
                    "T": self.getTeam()
                })), handler=log_message_players_reply)

def log_message_server(self, message: str):
    header = decodeJSON(message)
    data = header["DATA"]

    if header["FOR"] == "Player":
        self.send('server', encodeJSON(buildDict("PL_DIR", data["P"], {
            "X": data["X"],
            "Y": data["Y"]
        })))

    if header["FOR"] == "Ball":
        if header["MSG_TYPE"] == "BL_SERVE":
            self.send('server', encodeJSON(buildDict("BL_SERVE", "Ball", {
                "X": data["X"],
                "Y": data["Y"],
                "T": data["T"]
            })))
            self.log_info("Serwer, przekazał nowy kierunek dla piłki od gracza.")
            return ""

        if header["MSG_TYPE"] == "BL_AT":
            self.send('server', encodeJSON(buildDict("BL_AT", "Ball", {
                "X": data["X"],
                "Y": data["Y"],
                "T": data["T"]
            })))
            self.log_info("Serwer, przekazał nowy kierunek dla piłki od gracza.")
            return ""

        if header["MSG_TYPE"] == "BL_PS":
            self.send('server', encodeJSON(buildDict("BL_PS", "Ball", {
                "X": data["X"],
                "Y": data["Y"],
                "H": data["H"],
                "T": data["T"]
            })))
            self.log_info("Serwer, przekazał nowy kierunek dla piłki od gracza.")
            return ""

def log_message_ball(self, message: str):
    header = decodeJSON(message)
    data = header["DATA"]

    if self.name == header["FOR"] or "All" == header["FOR"]:
        if header["MSG_TYPE"] == "BL_SERVE":
            self.log_info("Piłka otrzymała kierunek od gracza x = " + str(data["X"]) + ", y = " + str(data["Y"]))
            self.calculateDirection(data["X"], data["Y"], False)
            if abs(self.getXDir()) >= 0.35 and abs(self.getXDir()) >= 0.35:
                self.setSteps(self.getSteps() * 1.05)
            elif abs(self.getYDir()) <= 0.15:
                self.setSteps(self.getSteps() * 0.86)
            self.setLastTouch(data["T"])
            self.maxCount()

        if header["MSG_TYPE"] == "BL_AT":
            self.log_info("Piłka otrzymała kierunek od gracza x = " + str(data["X"]) + ", y = " + str(data["Y"]))
            self.calculateDirection(data["X"], data["Y"], False)
            if abs(self.getXDir()) >= 0.35 and abs(self.getXDir()) >= 0.35:
                self.setSteps(self.getSteps() * 1.05)
            elif abs(self.getYDir()) <= 0.15:
                self.setSteps(self.getSteps() * 0.86)
            self.setLastTouch(data["T"])
            self.maxCount()

        if header["MSG_TYPE"] == "BL_PS":
            self.log_info("Piłka otrzymała kierunek od gracza x = " + str(data["X"]) + ", y = " + str(data["Y"]))
            self.setZ(data["H"] * 1.6)
            self.calculateDirection(data["X"], data["Y"], True)
            self.setLastTouch(data["T"])

            if self.counterState():
                self.setRecievedCounter(1)
            else:
                self.incCounter()

        elif header["MSG_TYPE"] == "ALL_MV":
            self.move()

def log_message_players_reply (self, message: str):
    pass


if __name__ == '__main__': #*************************************************************************************************

    # Utworzenie obiektu klasy Window
    window = Window()
    # Utworzenie obiektu klasy Field
    field = Field()
    # Utworzenie obiektu klasy Net
    net = Net()
    #Utworzenie obiektu klasy Score
    score = Score()

    player = None
    team = None

    # Uruchomienie lokalnego serwera i połączenie
    ns = run_nameserver()
    mast = run_agent('Master')
    addr = mast.bind('SYNC_PUB', alias='server', handler=log_message_server)
    ball = run_agent("Ball", base=Ball)
    ball.connect(addr, alias='server', handler=log_message_ball)
    rpTable = createTeam("Red")
    bpTable = createTeam("Blue")
    for rp in rpTable:
        rp.connect(addr, alias='server', handler=log_message_players)
    for bp in bpTable:
        bp.connect(addr, alias='server', handler=log_message_players)

    # Utworzenie okna
    window.createScreen()

    #Skalowanie rozmiaru obiektów
    field.scaleField(window.getWidth(), window.getHeight())
    net.scaleNet(window.getWidth(), window.getHeight())
    ball.scaleWidth(field.getWidth(), field.getDistance(), net.getDistance())
    scaleTeam(rpTable, bpTable, field)

    while True: #*********************************************************************************************

        # Odwołanie się do kolejki zdarzeń i incjuje ponownie pygame
        pygame.event.pump()
        # Czy są jakieś eventy w kolejce do obsłużenia?
        if(pygame.event.peek()):
            # Oczekuje na zdarzenie, jesli oczekiwanie sie zakonczy przypisuje zdarzenie do zmiennej
            event = pygame.event.wait()
            # W przypadku nacisniecia przycisku wylaczenia okna, konczy dzialanie programu
            if event.type == pygame.QUIT:
                window.closeScreen()
                ns.shutdown()
                exit(0)
            # W przypadku nacisniecia klawisza Escape, konczy dzialanie programu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window.closeScreen()
                    ns.shutdown()
                    exit(0)
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    score.setGameState(1)
            # W przypadku zmiany szerokosci okna skaluje boisko i graczy
            elif event.type == pygame.VIDEORESIZE:
                window.scaleScreen()
                field.scaleField(window.getWidth(), window.getHeight())
                net.scaleNet(window.getWidth(), window.getHeight())
                ball.scaleWidth(field.getWidth(), field.getDistance(), net.getDistance())
                scaleTeam(rpTable, bpTable, field)

        # Naprawa błędu związanego z wybiórczym skalowaniem minimalnej szerokości ekranu
        if(window.checkScreen()):
            window.scaleScreen()
            field.scaleField(window.getWidth(), window.getHeight())
            net.scaleNet(window.getWidth(), window.getHeight())
            ball.scaleWidth(field.getWidth(), field.getDistance(), net.getDistance())
            scaleTeam(rpTable, bpTable, field)

        # Rozgrywka***********************************************************************************************

        # Rozgrywka nie została uruchomiona ----------------------------------------------------------------------
        if score.getGameState() == 0:
            window.drawBackground(25, 125, 25)
            window.renderMenuMessage()
            pygame.display.flip()

        # Nowa rozgrywka jest tworzona ----------------------------------------------------------------------
        if score.getGameState() == 1:
            score.newGame()
            newSkills(rpTable, bpTable)
            startPosition(rpTable, bpTable, field, score.getWho())
            ball.startPosition(rpTable[0].getWidth(), field, score.getWho())
            ball.setLastTouch(score.getWho())
            score.setGameState(2)

        # W trakcie rozgrywki - serwowanie ----------------------------------------------------------------------
        if score.getGameState() == 2:
            # Ustawiamy piłkę na wysokości gracza
            startPosition(rpTable, bpTable, field, score.getWho())
            ball.startPosition(rpTable[0].getWidth(), field, score.getWho())
            ball.setZ(rpTable[0].getHeight() * 1.6)

            if not score.getWho():
                player = rpTable[3]
                team = bpTable
            else:
                player = bpTable[2]
                team = rpTable
            dir = []
            for a in team:
                for b in team:
                    dir.append([ (a.getX() + b.getX()) / 2, (a.getY() + b.getY()) / 2])

            index = random.randint(0, len(dir) - 1)
            mast.send('server', encodeJSON(buildDict("PL_SERVE", player.getName(), {
                "X": dir[index][0] + random.randint(-2, 2) * player.getWidth(),
                "Y": dir[index][1] + random.randint(-2, 2) * player.getWidth(),
            })))

            window.drawBackground(25, 125, 25)
            window.drawField(field.getX(), field.getY(), field.getWidth(), field.getHeight())
            window.drawNet(net.getX(), net.getY(), net.getWidth(), net.getHeight())
            window.renderPlayers(rpTable, 255, 0, 0)
            window.renderPlayers(bpTable, 0, 0, 255)
            window.renderBall(ball, net)
            window.renderScore(score)
            pygame.display.flip()
            sleep(1)
            score.setGameState(3)

        # W trakcie rozgrywki -
        if score.getGameState() == 3:  # ---------------------------------------------------------------------------

            recievedCounter = ball.getRecievedCounter()

            # Odbiór piłki przez drużynę przeciwną
            if recievedCounter == 3:
                dit = {
                    "player": None,
                    "distance": 50000
                }
                team = None
                player = None
                if ball.getLastTouch():
                    team = rpTable
                else:
                    team = bpTable

                goalX = ball.getXGoal()
                goalY = ball.getYGoal()

                for i in team:
                    dist = sqrt(pow(i.getX() - goalX, 2) + pow(i.getY() - goalY, 2))
                    if dist <= dit["distance"]:
                        dit["distance"] = dist
                        dit["player"] = i.getName()

                if dit["player"] is not None:
                    mast.send('server', encodeJSON(buildDict("PL_DIR", dit["player"], {
                        "X": goalX,
                        "Y": goalY
                    })))

                for i in team:
                    if i.ballRange(ball):
                        player = i
                        break

                if player is not None:
                    x = team[random.randint(0, 4)]
                    while x.getName() == player.getName():
                        x = team[random.randint(0, 4)]

                    mast.send('server', encodeJSON(buildDict("PL_PS", player.getName(), {
                        "X": x.getX(),
                        "Y": x.getY(),
                        "P": x.getName(),
                        "R": recievedCounter
                    })))

            # Akcja gracza dla odbioru pilki lub ataku
            if recievedCounter > 0 and recievedCounter < 3:

                choice = random.randint(1, 2)
                if recievedCounter == 2:
                    choice = 2

                team = None
                if not ball.getLastTouch():
                    team = rpTable
                else:
                    team = bpTable

                player = None

                for i in team:
                    if i.ballRange(ball):
                        player = i
                        break

                if choice == 1:

                    if player is not None:
                        x = team[random.randint(0, 4)]
                        while x.getName() == player.getName():
                            x = team[random.randint(0, 4)]

                        mast.send('server', encodeJSON(buildDict("PL_PS", player.getName(), {
                            "X": x.getX(),
                            "Y": x.getY(),
                            "P": x.getName(),
                            "R": recievedCounter
                        })))

                else:

                    if player is not None:
                        x = team[random.randint(0, 4)]
                        while x.getName() == player.getName():
                            x = team[random.randint(0, 4)]

                        if ball.getLastTouch():
                            team = rpTable
                        else:
                            team = bpTable

                        dir = []
                        for a in team:
                            for b in team:
                                dir.append([(a.getX() + b.getX()) / 2, (a.getY() + b.getY()) / 2])

                        index = random.randint(0, len(dir) - 1)
                        mast.send('server', encodeJSON(buildDict("PL_AT", player.getName(), {
                            "X": dir[index][0],
                            "Y": dir[index][1]
                        })))

            # Master informuje wszystkich o poruszeniu się, jeśli jest taka możliwość
            mast.send('server', encodeJSON(buildDict("ALL_MV", "All", {
                "N": net.getX()
                })))

            score.setGameState(4)

        # Sprawdzenie czy, któraś drużyna zdobyła punkt, albo rozgrywka się zakończyła -----------------------------
        if score.getGameState() == 4:
            #Jeśli nikt nie zdobył punktu to rozgrywka trwa nadal
            score.setGameState(3)

            if ball.touchOut(field.getWidth() + 100, field.getHeight() + 100) or (not ball.touchField(field) and ball.touchGround()) \
            or ball.touchNet(net) or ball.getRecievedCounter() > 3:
                score.addPoint(not ball.getLastTouch())
                score.setWho(not ball.getLastTouch())
                score.setGameState(2)
            elif ball.touchGround() and ball.touchField(field):
                if ball.getLastTouch() == ball.touchHalf(net):
                    score.addPoint(not ball.getLastTouch())
                    score.setWho(not ball.getLastTouch())
                    score.setGameState(2)
                else:
                    score.addPoint(ball.getLastTouch())
                    score.setWho(ball.getLastTouch())
                    score.setGameState(2)

            if not score.winGame():
                if score.winSet() == 0:
                    score.setWinSetsRed(score.getWinSetsRed() + 1)
                    score.resetScore()
                    score.setWho(True)
                    score.setGameState(2)
                elif score.winSet() == 1:
                    score.setWinSetsBlue(score.getWinSetsBlue() + 1)
                    score.resetScore()
                    score.setWho(False)
                    score.setGameState(2)

            # Wyświetlenie boiska, graczy, piłki i tablicy wyników --------------------------------------------------
            window.drawBackground(25, 125, 25)
            window.drawField(field.getX(), field.getY(), field.getWidth(), field.getHeight())
            window.drawNet(net.getX(), net.getY(), net.getWidth(), net.getHeight())
            window.renderPlayers(rpTable, 255, 0, 0)
            window.renderPlayers(bpTable, 0, 0, 255)
            window.renderBall(ball, net)
            window.renderScore(score)
            pygame.display.flip()

        # Rozgrywka się zakończyła ----------------------------------------------------------------------
        if score.getGameState() == 5:
            window.drawBackground(25, 125, 25)
            window.renderEndMessage(score)
            pygame.display.flip()
