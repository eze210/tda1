from sys import argv
from math import inf as Infinite

def loadGame(fileName):
    playerA = ShipPlayer()
    with open(fileName, "r") as file:
        for line in file:
            playerA.addShip(line)
    ships = playerA.getShips()
    playerB = Grido3MissilePlayer(ships, numberOfGuns=2)
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
        currentDamage = self.getDamageForCurrentTurn(currentTurn)
        self.health -= currentDamage
        if self.health < 0:
            self.health = 0

    """ 
    Devuelve la cantidad de tiros consecutivos que se necesitan para matar al
    barco comenzando por el turno actual
    """     
    def getNumberOfConsecutiveShotsToDie(self, currentTurn):
        if self.health <= 0:
            return Infinite
        appliedDamage = 0
        number = 0
        while appliedDamage < self.health:
            appliedDamage += self.getDamageForCurrentTurn(currentTurn + number)
            number += 1
        return number

    """
    Devuelve la cantidad de danio que se le haria al barco si se le disparara
    en el turno actual
    """    
    def getDamageForCurrentTurn(self, currentTurn):
        currentIndex = currentTurn % len(self.damageList)
        return self.damageList[currentIndex]

    """
    Devuelve el porcentaje de danio que se le haria al barco si se le disparara
    en el turno actual
    """    
    def getDamagePercentageForCurrentTurn(self, currentTurn):
        currentIndex = currentTurn % len(self.damageList)
        return self.damageList[currentIndex] / self.health


"""
Representa al jugador A
"""
class ShipPlayer:
    def __init__(self):
        self.currentTurn = 0
        self.shipList = []
        self.points = 0

    def getStatus(self):
        for i, ship in enumerate(self.shipList):
            print("Barco {0}: {1} hp".format(i, ship.health))
        print("Cantidad de puntos: {}".format(self.points))

    def addShip(self, strShip):
        ship = Ship.parseShip(strShip)
        self.shipList.append(ship)

    def receiveMissile(self, rowNum):
        self.shipList[rowNum].applyDamage(self.currentTurn)

    def step(self):
        self.currentTurn += 1
        self.points += self.countActiveShips()

    def getTurn(self):
        return self.currentTurn

    def countActiveShips(self):
        return sum(1 for s in self.shipList if s.health > 0)
        
    def getShips(self):
        return self.shipList


"""
Representa al jugador B
"""
class MissilePlayer:
    def __init__(self, shipList, numberOfGuns):
        self.shipList = shipList
        self.numberOfGuns = numberOfGuns

    def playTurn(self, currentTurn):
        return self.chooseRow(currentTurn)

    def chooseRow(self, currentTurn):
        return 0


class Grido1MissilePlayer(MissilePlayer):
    def chooseRow(self, currentTurn):
        minimumNumberOfShots = Infinite
        selectedRow = 0
        for row, ship in enumerate(self.shipList):
            if not ship.health > 0:
                continue

            numberOfShots = ship.getNumberOfConsecutiveShotsToDie(currentTurn)
            if numberOfShots < minimumNumberOfShots:
                selectedRow = row
                minimumNumberOfShots = numberOfShots
        
        return selectedRow


class Grido2MissilePlayer(MissilePlayer):
    def chooseRow(self, currentTurn):
        maximumDamage = 0
        selectedRow = 0
        for row, ship in enumerate(self.shipList):
            if not ship.health > 0:
                continue

            damage = ship.getDamageForCurrentTurn(currentTurn)
            if damage > maximumDamage:
                selectedRow = row
                maximumDamage = damage
        
        return selectedRow


class Grido3MissilePlayer(MissilePlayer):
    def chooseRow(self, currentTurn):
        maximumDamagePercentage = 0
        selectedRow = 0
        for row, ship in enumerate(self.shipList):
            if not ship.health > 0:
                continue

            damagePercentage = ship.getDamagePercentageForCurrentTurn(currentTurn)
            if damagePercentage > maximumDamagePercentage:
                selectedRow = row
                maximumDamagePercentage = damagePercentage
        
        return selectedRow


"""
Representa un juego
"""
class Game:
    def __init__(self, shipPlayer, missilePlayer):
        self.shipPlayer = shipPlayer
        self.missilePlayer = missilePlayer

    def play(self):
        while self.shipPlayer.countActiveShips() > 0:
            for _ in range(self.missilePlayer.numberOfGuns):
                selectedRow = self.missilePlayer.playTurn(self.shipPlayer.getTurn())
                print("Selected ship: {}".format(selectedRow))
                self.shipPlayer.receiveMissile(selectedRow)
                if self.shipPlayer.countActiveShips() == 0:
                    break

            self.shipPlayer.step()
            self.shipPlayer.getStatus()

if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python shipPlayer.py <shipfile>")
        exit(1)
    fileName = argv[1]
    print("Cargando {0}".format(fileName))
    game = loadGame(fileName)
    game.play()
