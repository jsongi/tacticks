class Upgrade:

    def __init__(self, imageNum, effectType, effectIndex, cost, name):
        self._imageNum = imageNum
        self.effectType = effectType
        self.effectIndex = effectIndex
        self._cost = cost
        self._name = name

    def getImage(self):
        return self._imageNum
    
    # Immediate (1), all are immediate for right now, maybe unlocks for others in the future
    def getEffectType(self):
        return self.effectType
    
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
                return
            case 2:
                for char in chars:
                    char.addMagic(5)
                return
            case 3:
                for char in chars:
                    char.addAttack(5)
                return
        
        return