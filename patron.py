class Patron:

    def __init__(self, imageNum, effectType, effectIndex, cost, name):
        self._imageNum = imageNum
        self._effectType = effectType
        self._effectIndex = effectIndex
        self._cost = cost
        self._name = name
        self._purchased = False

    def getImage(self):
        return self._imageNum
    
    # Beginning of round (1), on attack (2), after turn (3), during shop (4), during round (5)
    def getEffectType(self):
        return self._effectType

    def getCost(self):
        return self._cost

    def getName(self):
        return self._name

    def getPurchased(self):
        return self._purchased

    def setPurchased(self, status):
        self._purchased = status    

    # Handles effects
    def activateEffect(self, chars, enemies):
        match self._effectIndex:
            case 1:
                return
            case 2:
                return
            case 3:
                return
            case 4:
                return
            case 5:
                return
            case 6:
                return
            case 7:
                return
            case 8:
                return
            case 9:
                return
            case 10:
                return
            case 11:
                return
            case 12:
                return
            case 13:
                return
            case 14: #Jack
                for char in chars:
                    char.addTotalHealth(30)
                    char.addAttack(8)
                    char.addMagic(8)
                return
            case 15:
                return
            
    def handleSold(self, chars):
        return