from sys import argv


def loadGame(fileName):
    playerA = ShipPlayer()
    with open(fileName, "r") as file:
        for line in file:
            playerA.addShip(line)
    ships = playerA.getShips()
    playerB = GridoMissilePlayer(ships)
    return Game(playerA, playerB)


"""
Representa un barco con sus puntos de vida y vector de dano
"""
class Ship:
    def __init__(self, health, damageList):
        self.health = health
        self.damageList = damageList

    """
    Crea un barco a partir de su representacion en string
    """
    @staticmethod
    def parseShip(strShip):
        shipParamsStr = strShip.split(" ")
        shipParams = [int(x) for x in shipParamsStr]
        return Ship(shipParams[0], shipParams[1:])

    """ 
    Aplica el dano segun el turno actual y el vector de danios
    """ 
    def applyDamage(self, currentTurn):
        currentIndex = currentTurn % len(self.damageList)
        currentDamage = self.damageList[currentIndex]
        self.health -= currentDamage

"""
Representa al jugador A
"""
class ShipPlayer:
    def __init__(self):
        self.currentTurn = 0
        self.shipList = []

    def getStatus(self):
        for i, ship in enumerate(self.shipList):
            print("Barco {0}: {1} hp".format(i, ship.health))

    def addShip(self, strShip):
        ship = Ship.parseShip(strShip)
        self.shipList.append(ship)

    def receiveMissile(self, rowNum):
        self.shipList[rowNum].applyDamage(self.currentTurn)
        
    def step(self):
        self.currentTurn += 1

    def countActiveShips(self):
        return sum(1 for s in self.shipList if s.health > 0)
        
    def getShips(self):
        return self.shipList

"""
Representa al jugador B
"""
class MissilePlayer:
    def __init__(self, shipList):
        print("MissileInit")
        self.shipList = shipList

    def playTurn(self):
        return self.chooseRow()

    def chooseRow(self):
        return 0


class GridoMissilePlayer(MissilePlayer):
    def chooseRow(self):
        print ("Shiplist size {}".format(len(self.shipList)))
        return 0

"""
Representa un juego
"""
class Game:
    def __init__(self, shipPlayer, missilePlayer):
        self.shipPlayer = shipPlayer
        self.missilePlayer = missilePlayer

    def play(self):
        while (self.shipPlayer.countActiveShips() > 0):
            selectedRow = self.missilePlayer.playTurn()
            self.shipPlayer.receiveMissile(selectedRow)
            self.shipPlayer.step()
            self.shipPlayer.getStatus()

if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python ship.py <shipfile>")
        exit(1)
    fileName = argv[1]
    print("Cargando {0}".format(fileName))
    game = loadGame(fileName)
    game.play()