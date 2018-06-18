from sys import argv
from players import MissilePlayer
import time


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
            print(" ----  Barco {0}: {1} hp".format(i, ship.health))
        print(" ---- Cantidad de puntos: {}".format(self.points))

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



class DynamicShip():
    def __init__ (self, ship, numberOfGuns):
        self.ship = ship
        self.maxHealth = ship.health
        self.shotList = []
        self.totalDamage = 0
        currentTurn = 0
        self._shootUntilDeath(0)

    def removeShot(self, turn):
        if not turn < len(self.shotList):
            return False
        if self.shotList[turn] == 0:
            return False
        numShots = self.shotList[turn]
        self.totalDamage -= self.ship.getDamageForCurrentTurn(turn)
        self.shotList[turn] -= 1
        return True

    def addShot(self, turn):
        if len(self.shotList) < turn + 1:
            self.shotList.append(0)
        self.shotList[turn] += 1
        self.totalDamage += self.ship.getDamageForCurrentTurn(turn)
        #self._adjustDeath(turn + 1)


    def getPoints(self):
        return len(self.shotList) - 1

    def _adjustDeath(self, turn = 0):
        if turn > len(self.shotList):
            return
        self._removeExtraShots()
        self._shootUntilDeath(turn)
        
    def _removeExtraShots(self):
        while self.totalDamage > self.maxHealth:
            if self.shotList[-1] > 0:
                turn = len(self.shotList) - 1
                self.totalDamage -= self.ship.getDamageForCurrentTurn(turn)
                self.shotList[-1] -= 1
            else:
                self.shotList.pop()
        if self.shotList[-1] == 0 and self.totalDamage > 0:
            self.shotList.pop()

    """
    Dispara a partir del ultimo disparo recibido y devuelve el turno
    en el que morira si le disparo hasta matarlo
    """
    def _shootUntilDeath(self, turn):
        currentTurn = len(self.shotList)
        if currentTurn <= turn or not self.shotList:
            self.shotList.append(0)
        currentShot = self.shotList.pop()
        if currentShot == numberOfGuns:
            self.shotList.append(currentShot)
            currentShot = 0

        while self.totalDamage < self.maxHealth:
            currentShot += 1
            self.totalDamage += self.ship.getDamageForCurrentTurn(currentTurn)
            if currentShot == numberOfGuns:
                self.shotList.append(numberOfGuns)
                currentTurn += 1
                currentShot = 0
        if (currentShot != 0):
            self.shotList.append(currentShot)
        return self.getPoints()


class DinamicoAltMissilePlayer(MissilePlayer):
    def __init__(self, shipList, numberOfGuns):
        super(DinamicoAltMissilePlayer, self).__init__(shipList, numberOfGuns)
        self.numberOfGuns = numberOfGuns
        self.dynShipList = []
        for i in range(0, len(shipList)):
            self.addShip(DynamicShip(shipList[i], numberOfGuns))
        time.sleep(1)

    def playTurn(self, currentTurn):
        print("Playing turn", currentTurn)
        shipList = self.dynShipList[:]
        minPoints = []
        for ship in shipList:
            minPoints.append(ship.getPoints())
        selectedShots = self._distributeShots(currentTurn, self.numberOfGuns, shipList, minPoints, [])
        time.sleep(1)
        return selectedShots

    def _distributeShots(self, turn, shots, shipList, minPoints, prevShots):

        tmpPoints = []
        for ship in shipList:
            ship.removeShot(turn)
        for prevShot in prevShots:
            tmpShip = shipList[prevShot]
            tmpShip.addShot(turn)
            #minPoints[prevShot] = shipList[prevShot].getPoints()
        for i, ship in enumerate(shipList):
            ship._adjustDeath(turn + 1)
            tmpPoints.append(ship.getPoints() - minPoints[i])
            
        # Puntos si tuviera tiros para cada barco
        if len(prevShots) == shots:
            return prevShots

        worstGap = tmpPoints[0]
        candidates = []
        for i, v in enumerate(tmpPoints):
            if v > worstGap:
                worstGap = v
                candidates = [i]
            elif v == worstGap:
                if shipList[i].ship.health > 0:
                    candidates.append(i)
        if (len(candidates)) > 1:
            print("Mejorar, buscar el optimo en caso de empate")
            for cand in candidates:
                print("Candidato {0}: {1}/{2}".format(cand, shipList[cand].ship.health, shipList[cand].maxHealth))
        prevShots.append(candidates[0])
        return self._distributeShots(turn, shots, shipList, minPoints, prevShots)

    def addShip(self, ship):
        self.dynShipList.append(ship)

    def chooseRow(self, currentTurn):
        return currentTurn % len(self.shipList)
        

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
            selectedRows = self.calculateNextShots()
            for row in selectedRows:
                self.selectRow(row)
        return self.shipPlayer.points, tuple(self.completeSequence)

    def selectRow(self, selectedRow):
        print("Selected ship: {}".format(selectedRow))
        self.shipPlayer.receiveMissile(selectedRow)

        self.gunsUsedInTheCurrentTurn += 1
        self.turnSequence.append(selectedRow)
        if self.gunsUsedInTheCurrentTurn == self.missilePlayer.numberOfGuns:
            self.shipPlayer.step()
            self.gunsUsedInTheCurrentTurn = 0
            self.completeSequence.append(tuple(self.turnSequence))
            self.turnSequence = []

        self.shipPlayer.getStatus()

    def getCurrentTurn(self):
        return self.shipPlayer.currentTurn
    
    def calculateNextShots(self):
        return self.missilePlayer.playTurn(self.shipPlayer.getTurn())

def loadGame(fileName, numberOfGuns, PlayerClass):
    playerA = ShipPlayer()
    with open(fileName, "r") as file:
        for line in file:
            playerA.addShip(line)
    ships = playerA.getShips()
    playerB = PlayerClass(ships, numberOfGuns)
    return Game(playerA, playerB)

if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: python game.py <gridfile> <guns>")
        exit(1)
    fileName = argv[1]
    numberOfGuns = int(argv[2])
    PlayerClass = DinamicoAltMissilePlayer
    print("Loading {0}...".format(fileName))
    game = loadGame(fileName, numberOfGuns, PlayerClass)
    print(game.play())