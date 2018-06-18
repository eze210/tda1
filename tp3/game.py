from sys import argv
import players
from pretty_printer import run_simulation
try:
    from math import inf as Infinite
except Exception as e:
    Infinite = float('inf')


def loadGame(fileName, numberOfGuns, PlayerClass):
    Z = None
    playerA = ShipPlayer()
    with open(fileName, "r") as file:
        for line in file:
            ship = playerA.addShip(line)
            if ship.identifier == 0:
                Z = len(ship.damageList)
            if Z is not len(ship.damageList):
                raise RuntimeError('All rows must have the same length')
                
    ships = playerA.getShips()
    playerB = PlayerClass(ships, numberOfGuns)
    return Game(playerA, playerB)


"""
Representa un barco con sus puntos de vida y vector de dano
"""
class Ship:
    def __init__(self, identifier, health, damageList):
        self.identifier = identifier
        self.health = health
        self.damageList = damageList

        ok = False
        for d in self.damageList:
            if d > 0:
                ok = True
        if not ok:
            raise RuntimeError('Some value in damages list must be greater than zero')

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
        return ship

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
Representa un juego
"""
class Game:
    def __init__(self, shipPlayer, missilePlayer):
        self.shipPlayer = shipPlayer
        self.missilePlayer = missilePlayer
        self.gunsUsedInTheCurrentTurn = 0
        
        self.turnSequence = []
        self.completeSequence = []

    def play(self):
        while self.shipPlayer.countActiveShips() > 0:
            selectedRow = self.calculateNextShot()
            self.selectRow(selectedRow)
        return self.shipPlayer.points, tuple(self.completeSequence)

    def selectRow(self, selectedRow):
        self.shipPlayer.receiveMissile(selectedRow)

        self.gunsUsedInTheCurrentTurn += 1
        self.turnSequence.append(selectedRow)
        if self.gunsUsedInTheCurrentTurn == self.missilePlayer.numberOfGuns:
            print("Turno:", self.shipPlayer.getTurn())
            print("Cantidad de barcos disponibles:", self.shipPlayer.countActiveShips())
            print("Daños potenciales:", [s.getDamageForCurrentTurn(self.shipPlayer.getTurn()) for s in self.shipPlayer.shipList])
            print("Barcos elegidos:", self.turnSequence)
            self.shipPlayer.getStatus()
            print()
            self.shipPlayer.step()
            self.gunsUsedInTheCurrentTurn = 0
            self.completeSequence.append(tuple(self.turnSequence))
            self.turnSequence = []


    def getCurrentTurn(self):
        return self.shipPlayer.currentTurn
    
    def calculateNextShot(self):
        return self.missilePlayer.playTurn(self.shipPlayer.getTurn(), self.gunsUsedInTheCurrentTurn)


if __name__ == "__main__":
    if len(argv) < 4:
        print("Usage: python game.py <gridfile> <guns> <playerclass>")
        exit(1)
    fileName = argv[1]
    numberOfGuns = int(argv[2])
    PlayerClass = players.PlayerClasses[argv[3]]
    print("Loading {0}...".format(fileName))
    game = loadGame(fileName, numberOfGuns, PlayerClass)

    level = [s.damageList for s in game.shipPlayer.shipList]
    ships_health = [s.health for s in game.shipPlayer.shipList]

    solution = game.play()

    # runs and shows the game using the obtained solution
    run_simulation(level, ships_health, solution[1])
