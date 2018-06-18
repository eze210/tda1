try:
    from math import inf as Infinite
except Exception as e:
    Infinite = float('inf')

from dynamic import solve_game


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
        if currentTurn * self.numberOfGuns + numberOfGuns < len(self.solution):
            return self.solution[currentTurn * self.numberOfGuns + numberOfGuns]
        else:
            return 0

PlayerClasses = {
    'dyn': DinamicoMissilePlayer,
    'gr1': Grido1MissilePlayer,
    'gr2': Grido2MissilePlayer,
    'gr3': Grido3MissilePlayer
}
