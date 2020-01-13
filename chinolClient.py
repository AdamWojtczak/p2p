import socket

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from time import sleep
import threading

sock = ''

class TotalCommander(QMainWindow):
    def __init__(self, address, kolor):
        super(TotalCommander, self).__init__()
        self.interface(kolor)

    def sendMsg(self, sock, msg):
        sock.send(bytes(msg, 'utf-8'))


    def updatePeers(self, peerData):
        peers = str(peerData, "utf-8").split(",")[:-1]


    def interface(self, kolor):
        self.setWindowTitle('Total Commander in python')
        self.run = False
        Widget = QWidget()
        self.setCentralWidget(Widget)
        self.grid = QGridLayout()  # grid na przyciski

        self.biale = []
        self.startR = []
        self.startB = []
        self.startG = []
        self.startY = []
        self.koniecR = []
        self.koniecB = []
        self.koniecG = []
        self.koniecY = []
        self.kostki = []

        self.drawBoard()

        self.kostka = QPushButton()  # przycisk z kostką
        self.kostka.setIcon(QIcon('./d0.png'))
        self.kostka.clicked.connect(self.rzucKostka)
        self.grid.addWidget(self.kostka, 8, 8)

        Widget.setLayout(self.grid)
        self.iluGra = 2  # ilu graczy jest podłączonych ->do zmiany po dodaniu sieci
        self.setMouseTracking(True)
        self.kolorGracza = kolor  # kolor tego gracza #wstawic literke koloru w wywolaniu konstruktora na samym dole

        self.wybor = False  # gracz ma wybór pionka do ruchu
        self.ruch = False  # gracz ruszył pionkiem
        self.rzuc = False  # gracz chce rzucić kostką
        self.wynikRzutu = -1  # wynik ostatniego rzutu kostką

        self.inicjacjaGraczy()
        zacznijGre = QAction('&Start', self)
        zacznijGre.setStatusTip('Zacznij gre')

        watek = threading.Thread(target=self.start)

        zacznijGre.triggered.connect(lambda: watek.start())
        menubar = self.menuBar()
        opcje = menubar.addMenu('&Opcje')
        opcje.addAction(zacznijGre)
        self.show()

    def rzucKostka(self):  # event przycisku z kostką -> gracz chce rzucić
        self.rzuc = True

    def nowy(self):  # event przycisków startowych jeśli może taki wybrać uruchamiane zostaje przeniesienie na planszę
        if self.wybor == True and self.sender() in self.startR and 0 not in self.tab[4]:
            self.pionNaStart(self.tab[0])
            self.ruch = True
            self.wybor = False

    def guzik(self):  # event przycisków planszy -> gracz wybiera pionek do przesunięcia
        if self.wybor == True and self.biale.index(self.sender()) in self.tab[4]:
            # print("x "+"{}".format(self.sender().x())+ " y "+"{}".format(self.sender().y()))
            self.przesunPionek(self.sender(), self.wynikRzutu)
            self.ruch = True
            self.wybor = False

    def changeColor(self, button, color):  # funkcja do zmiany koloru przycisku "button" na podany "color"
        if color == 'R':
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 red);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
        elif color == 'W':
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 white);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
        elif color == 'Y':
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 yellow);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
        elif color == 'B':
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 blue);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
        elif color == 'G':
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 green);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
        elif color == 'L':
            button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 black);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
        elif color == 'SB':
            button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 DogerBlue);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
        elif color == 'SR':
            button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 FireBrick);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
        elif color == 'SY':
            button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 Khaki);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
        elif color == 'SG':
            button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 lime);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')

    def mousePressEvent(self, event):  # event kliknięcia myszą, drukuje współrzędne -> zbędny
        print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))

    def pionNaStart(self, color):  # ustawienie piona z pola startowego na planszy dla gracza z danym parametrem "color"
        if color == 'R':
            self.changeColor(self.startR[self.red[3]], 'L')
            self.changeColor(self.biale[0], color)
            self.red[4][self.red[3]] = 0
            self.red[3] = self.red[3] + 1
        elif color == 'Y':
            self.changeColor(self.startY[self.yellow[3]], 'L')
            self.yellow[3] = self.yellow[3] + 1
            self.changeColor(self.biale[20], color)
            self.yellow[4][0] = 20
        elif color == 'G':
            self.changeColor(self.startG[self.green[3]], 'L')
            self.green[3] = self.green[3] + 1
            self.changeColor(self.biale[10], color)
            self.green[4][0] = 10
        else:
            self.changeColor(self.startB[self.blue[3]], 'L')
            self.blue[3] = self.blue[3] + 1
            self.changeColor(self.biale[30], color)
            self.blue[4][0] = 30

    def rozczytanieKomunikatu(self, komunikat):  # rozczytanie ruchu innego gracza
        # pola komunikatu
        # litera koloru gracza, który wykonał ruch ->
        # pole z którego przesunięto pionek -> -1 to z pozycji startowej
        # pole na które przesunięto pionek -> -1 nie wykonano przesunięcia? 40,41,42,43 pola końcowe
        # numer gracza który wykonuje następny ruch ->jeśli F to koniec
        gracz, poleZ, poleDo, ktoNastepny = komunikat.split()

        if poleDo != -1:
            if poleZ == -1:
                self.pionNaStart(gracz)
            else:
                self.przesunPionek(gracz, self.biale[poleZ], poleDo)

        if self.tab[1] == ktoNastepny:
            mojaTura()
        self.czyKoniec()

    def przesunPionekSiec(self, kto, pionek, ile):  # wersja sieciowa
        if kto == "R":
            tab = self.red
        elif kto == 'B':
            tab = self.blue
        elif kto == 'Y':
            tab = self.yellow
        elif kto == 'G':
            tab = self.green

        if pionek in self.biale:
            x = self.biale.index(pionek)
            if x in tab[4]:
                self.komunikat += ' ' + str(x)  #
                if ile < 40:
                    ile -= 40
                    tab[4][tab[4].index(x)] = -2
                    tab[8][ile] = 1
                    tab[5] += 1
                    self.changeColor(self.biale[x], 'W')
                    if kto == "R":
                        self.changeColor(self.koniecR[ile], 'R')
                    elif kto == 'B':
                        self.changeColor(self.koniecB[ile], 'B')
                    elif kto == 'Y':
                        self.changeColor(self.koniecY[ile], 'Y')
                    elif kto == 'G':
                        self.changeColor(self.koniecG[ile], 'G')
                    self.komunikat += ' ' + str(40 + ile)  #
                else:
                    if x + ile > 39 - tab[7]:
                        A = x + ile - 40 - tab[7]
                        if A < 4:
                            if tab[8][A] == 0:
                                tab[4][tab[4].index(x)] = -2
                                tab[8][A] = 1
                                tab[5] += 1
                                self.changeColor(self.biale[x], 'W')
                                if kto == "R":
                                    self.changeColor(self.koniecR[A], 'R')
                                elif kto == 'B':
                                    self.changeColor(self.koniecB[A], 'B')
                                elif kto == 'Y':
                                    self.changeColor(self.koniecY[A], 'Y')
                                elif kto == 'G':
                                    self.changeColor(self.koniecG[A], 'G')
                                self.komunikat += ' ' + str(40 + A)  #

                    else:
                        for gracz in self.gracze:
                            if not (kto in gracz):
                                if x in gracz[4]:
                                    print(5)
                                    temp = gracz[4]
                                    y = temp.index(x)
                                    temp[y] = -1
                                    self.changeColor((gracz[6])[gracz[3]], 'S' + gracz[0])
                                    gracz[3] = gracz[3] - 1
                                    break
                        self.changeColor(self.biale[x], 'W')
                        self.changeColor(self.biale[x + ile], tab[0])
                        z = (tab[4]).index(x)
                        tab[4][z] = x + ile
                        self.komunikat += ' ' + str(x + ile)

    def start(self):  # główna funkcja gry -> po dodaniu sieci tura gracza? -> do usunięcia?
        self.run = True
        while (self.run):  # jeśli nikt nie wygral działa
            ####################################tutaj petla czytajaca komunikaty i odpalajaca rozczytanieKomunikatu
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                if data[0:1] == b'\x11':
                    print("got peers")
                    okno.updatePeers(data[1:])
                else:
                    # argumenty = str(data, 'utf-8').split(' ')
                    # okno.przesunPionekSiec(argumenty[1],argumenty[2],argumenty[3])
                    print(str(data, 'utf-8'))

            for i in self.gracze:
                ile6 = 0
                if i[2]:  # jeśli jest kolej gracza
                    while self.rzuc == False:
                        sleep(1)
                    self.rzuc = False
                    wynik = self.DieRoll()
                    # print(2)
                    ile6 = 0
                    while wynik == 6:
                        if ile6 < 3:
                            if i[3] == 0:
                                self.pionNaStart(i[0])
                            else:
                                self.wybor = True
                                while self.ruch == False:
                                    sleep(0.1)
                                self.czyKoniec()
                                if self.run == False:
                                    break;
                        else:
                            break;
                        ile6 = ile6 + 1
                    else:
                        if i[3] > 0:
                            self.wybor = True
                            while self.ruch == False:
                                sleep(0.1)
                            self.czyKoniec()
                            if self.run == False:
                                break;
            self.czyKoniec()
            # i[2]=False
            # self.gracze[i[1]+1][2]=True

    def przesunPionek(self, pionek,
                      ile):  # funkcja przesuwania pionka po planszy, włącznie z końcem trasy-> Do zmiany na sieci
        if pionek in self.biale:
            x = self.biale.index(pionek)
            if x in self.tab[4]:
                if x + ile > 39 - self.tab[7]:
                    A = x + ile - 40 - self.tab[7]
                    if A < 4:
                        if self.tab[8][A] == 0:
                            self.tab[4][self.tab[4].index(x)] = -2
                            self.tab[8][A] = 1
                            self.tab[5] += 1
                            self.changeColor(self.biale[x], 'W')
                            self.changeColor(self.koniecR[A], 'R')  ##############

                else:
                    for gracz in self.gracze:
                        if not (self.kolorGracza in gracz):
                            if x in gracz[4]:
                                print(5)
                                temp = gracz[4]
                                y = temp.index(x)
                                temp[y] = -1
                                self.changeColor((gracz[6])[gracz[3]], 'S' + gracz[0])
                                gracz[3] = gracz[3] - 1
                                break
                    self.changeColor(self.biale[x], 'W')
                    self.changeColor(self.biale[x + ile], self.tab[0])
                    z = (self.tab[4]).index(x)
                    self.tab[4][z] = x + ile

            # sprawdzić czy gracz ma pionek na tym polu
            # sprawdz kolizje --> sprawdź czy ktoś ma piona na tym polu, jeśli tak to przemalować i zmienić tablicę
            # pomalować pionek na biało
            # pomalować self.biale[x+self.ile] na kolor gracza
            # zmienić tablicę gracza

    def czyKoniec(self):  # sprawdza czy gra powinna się skończyć
        if self.tab[5] == 4:
            self.run = False

    def inicjacjaGraczy(self):  # stworzenie tablic dla graczy

        self.red = ['R', 1, True, 0, [-1, -1, -1, -1], 0, self.startR, 0, [0, 0, 0, 0]]
        #               pola tablcy -> gracza przykład powyżej, opis poniżej
        # nazwa koloru
        # numer w kolejności
        # czyJegoKolej
        # ile pionków ma już na planszy
        # numery pól z pionkami gracza -> -1 na pozycji startowej
        # ile Pionków Skończyło
        # tabela z przyciskami startowymi
        # nr pola z którego gracz zaczyna
        # oznaczenie pól końcowych ->0 wolne, 1 zajęte
        self.blue = ['B', 2, False, 0, [-1, -1, -1, -1], 0, self.startB, 30, [0, 0, 0, 0]]
        self.green = ['G', 3, False, 0, [-1, -1, -1, -1], 0, self.startG, 10, [0, 0, 0, 0]]
        self.yellow = ['Y', 4, False, 0, [-1, -1, -1, -1], 0, self.startY, 20, [0, 0, 0, 0]]
        if self.iluGra == 4:
            self.gracze = [self.red, self.blue, self.green, self.yellow]
        elif self.iluGra == 3:
            self.gracze = [self.red, self.green, self.yellow]
        elif self.iluGra == 2:
            self.gracze = [self.red, self.green]
        elif self.iluGra == 1:
            self.gracze = [self.red]

        if self.kolorGracza == 'R':
            self.tab = self.red
        elif self.kolorGracza == 'B':
            self.tab = self.blue
        elif self.kolorGracza == 'Y':
            self.tab = self.yellow
        else:
            self.tab = self.green

    def DieRoll(self):  # rzut kostką oraz zmiana ikony przycisku
        import random
        roll = random.randint(1, 6)
        self.wynikRzutu = roll
        self.kostka.setIcon(QIcon('./d' + str(roll) + '.png'))
        return roll

    def mojaTura(self):  # tura gracza właściciela
        # warunek na start
        start = 1
        end = 2
        if self.run == True:
            ile6 = 0
            while self.rzuc == False:
                sleep(1)
            self.rzuc = False
            self.komunikat = self.tab[0]
            wynik = self.DieRoll()

            if wynik == 6:
                while wynik == 6:

                    if ile6 < 3:
                        if self.tab[3] == 0:
                            self.pionNaStart(i[0])
                            start = -1
                            end = self.tab[7]
                            self.komunikat += ()
                        else:
                            self.wybor = True
                            while self.ruch == False:
                                sleep(0.1)
                            self.czyKoniec()
                            if self.run == False:
                                break
                    while self.rzuc == False:
                        sleep(0.1)
                    self.rzuc = False
                    wynik = self.DieRoll()
                    if wynik == 6 and (ile6 + 1) == 3:
                        self.komunikat += ' ' + self.tab[1] + 1
                    else:
                        self.komunikat += ' ' + self.tab[1]
                        break
                    # wyślij
                    self.sendMsg(sock,self.komunikat)
                    ile6 = ile6 + 1



            else:
                if self.tab[3] > 0:
                    self.wybor = True
                    while self.ruch == False:
                        sleep(0.1)
                    self.czyKoniec()
                    self.komunikat += ' ' + str(self.tab[1] + 1)
            self.czyKoniec()
            self.sendMsg(sock, self.komunikat)
            # wyślij komunikat

    def drawBoard(self):  # rysowanie planszy i dodanie pól do odpowiednich tablic
        tabI = [4, 4, 4, 4, 4, 3, 2, 1, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4, 4, 5, 6, 6, 6, 6, 6, 7, 8, 9, 10, 10, 10, 9, 8, 7,
                6, 6, 6, 6, 6, 5]
        tabJ = [0, 1, 2, 3, 4, 4, 4, 4, 4, 5, 6, 6, 6, 6, 6, 7, 8, 9, 10, 10, 10, 9, 8, 7, 6, 6, 6, 6, 6, 5, 4, 4, 4, 4,
                4, 3, 2, 1, 0, 0]

        for k in range(40):
            button = QToolButton()
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 white);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
            self.biale.append(button)
            self.grid.addWidget(button, tabI[k], tabJ[k])
            button.clicked.connect(self.guzik)

        for i in range(1, 5):
            button = QToolButton()
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 FireBrick);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
            self.koniecR.append(button)
            self.grid.addWidget(button, 5, i)
            button.clicked.connect(self.guzik)

        for i in range(6, 10):
            button = QToolButton()
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 Khaki);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
            self.koniecY.append(button)
            self.grid.addWidget(button, 5, i)
            button.clicked.connect(self.guzik)

        for i in range(1, 5):
            button = QToolButton()
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 lime);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
            self.koniecG.append(button)
            self.grid.addWidget(button, i, 5)
            button.clicked.connect(self.guzik)

        for i in range(6, 10):
            button = QToolButton()
            button.setStyleSheet(''' 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 DodgerBlue);
                border-style: solid;
                border-color: black;
                border-width: 5px;
                border-radius: 14px;''')
            self.koniecB.append(button)
            self.grid.addWidget(button, i, 5)
            button.clicked.connect(self.guzik)

        for i in range(2):
            for j in range(2):
                button = QToolButton()
                button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 FireBrick);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
                self.grid.addWidget(button, i, j)
                button.clicked.connect(self.nowy)
                self.startR.append(button)

        for i in range(2):
            for j in range(9, 11):
                button = QToolButton()
                button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 lime);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
                self.grid.addWidget(button, i, j)
                button.clicked.connect(self.nowy)
                self.startG.append(button)
        for i in range(9, 11):
            for j in range(2):
                button = QToolButton()
                button.setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 DodgerBlue);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
                self.grid.addWidget(button, i, j)
                button.clicked.connect(self.nowy)
                self.startB.append(button)

        for i in range(9, 11):
            for j in range(9, 11):
                self.startY.append(QToolButton())
                button = QToolButton()
                self.startY[-1].setStyleSheet(''' 
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 black, stop: 1 Khaki);
                        border-style: solid;
                        border-color: black;
                        border-width: 5px;
                        border-radius: 50px;''')
                self.grid.addWidget(self.startY[-1], i, j)
                self.startY[-1].clicked.connect(self.nowy)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    okno = TotalCommander("127.0.0.1", 'R') #tutaj wsatwic literke koloru
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 10000))

    # iThread = threading.Thread(target=self.sendMsg, args=(sock,))
    # iThread.daemon = True
    # iThread.start()



    sys.exit(app.exec_())