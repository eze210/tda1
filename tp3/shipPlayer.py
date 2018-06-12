from sys import argv

try:
    from math import inf as Infinite
except Exception as e:
    Infinite = float('inf')

from dynamic import *

def loadGame(fileName, numberOfGuns):
    playerA = ShipPlayer()
    with open(fileName, "r") as file:
        for line in file:
            playerA.addShip(line)
    ships = playerA.getShips()
    playerB = DinamicoMissilePlayer(ships, numberOfGuns)
    return Game(playerA, playerB)


"""
Representa un barco con sus puntos de vida y vector de dano
"""
class Ship:
    def __init__(self, identifier, health, damageList):
        self.identifier = identifier
        self.health = health
        self.damageList = damageList

    """
    Crea un barco a partir de su representacion en string
    """
    @staticmethod
    def parseShip(identifier, strShip):
        shipParamsStr = strShip.split(" ")
        shipParams = [int(x) for x in shipParamsStr]
        return Ship(identifier, shipParams[0], shipParams[1:])

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
        ship = Ship.parseShip(len(self.shipList), strShip)
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

    def playTurn(self, currentTurn, numberOfGuns):
        return self.chooseRow(currentTurn, numberOfGuns)

    def chooseRow(self, currentTurn, numberOfGuns):
        return 0


class Grido1MissilePlayer(MissilePlayer):
    def chooseRow(self, currentTurn, numberOfGuns):
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
    def chooseRow(self, currentTurn, numberOfGuns):
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
    def chooseRow(self, currentTurn, numberOfGuns):
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


class DinamicoMissilePlayer(MissilePlayer):
    def __init__(self, shipList, numberOfGuns):
        super(DinamicoMissilePlayer, self).__init__(shipList, numberOfGuns)
        dmgGrid = [x.damageList for x in shipList]
        hitpoints = [x.health for x in shipList]
        self.solution = solve_game(dmgGrid, hitpoints, numberOfGuns)
        self.solution = [item for sublist in self.solution[1] for item in sublist]
        print(self.solution)

    def chooseRow(self, currentTurn, numberOfGuns):
        return self.solution[currentTurn * self.numberOfGuns + numberOfGuns]


"""
Representa un juego
"""
class Game:
    def __init__(self, shipPlayer, missilePlayer):
        self.shipPlayer = shipPlayer
        self.missilePlayer = missilePlayer
        self.gunsUsedInTheCurrentTurn = 0

    def play(self):
        while self.shipPlayer.countActiveShips() > 0:
            selectedRow = self.missilePlayer.playTurn(self.shipPlayer.getTurn(), self.gunsUsedInTheCurrentTurn)
            self.selectRow(selectedRow)

    def selectRow(self, selectedRow):
        print("Selected ship: {}".format(selectedRow))
        self.shipPlayer.receiveMissile(selectedRow)
        self.shipPlayer.getStatus()

        self.gunsUsedInTheCurrentTurn += 1
        if self.gunsUsedInTheCurrentTurn == self.missilePlayer.numberOfGuns:
            self.shipPlayer.step()
            self.gunsUsedInTheCurrentTurn = 0

    def getCurrentTurn(self):
        return self.shipPlayer.currentTurn


if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python shipPlayer.py <shipfile>")
        exit(1)
    fileName = argv[1]
    print("Cargando {0}".format(fileName))
    game = loadGame(fileName, numberOfGuns=4)
    game.play()
