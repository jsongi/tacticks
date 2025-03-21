class Upgrade:

    def __init__(self, imageNum, effectIndex, cost, name):
        self._imageNum = imageNum
        self.effectIndex = effectIndex
        self._cost = cost
        self._name = name
        self._totalHealth = 0
        self._magic = 0
        self._attack = 0
        self._healing = 0

    def getImage(self):
        return self._imageNum
    
    def getCost(self):
        return self._cost

    def getName(self):
        return self._name
    
    # Handles effects
    def activateEffect(self, chars):
        match self.effectIndex:
            case 1:
                for char in chars:
                    char.addTotalHealth(15)
                self._totalHealth += 15
                return
            case 2:
                for char in chars:
                    char.addMagic(5)
                self._magic += 3
                return
            case 3:
                for char in chars:
                    char.addAttack(5)
                self._attack += 3
                return
            case 4:
                self._healing += 1
                return
        return
    
        # Handles effects
    def onUnitPurchase(self, char):
        match self.effectIndex:
            case 1:
                char.addTotalHealth(self._totalHealth)
                return
            case 2:
                char.addMagic(self._magic)
                return
            case 3:
                char.addAttack(self._attack)
                return
            case 4:
                return
        return