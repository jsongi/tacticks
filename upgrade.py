class Upgrade:

    def __init__(self, imageNum, effectType, effectIndex, cost, name):
        self._imageNum = imageNum
        self.effectType = effectType
        self.effectIndex = effectIndex
        self._cost = cost
        self._name = name

    def getImage(self):
        return self._imageNum
    
    # Immediate (1), Per round (2), 
    def getEffectType(self):
        return self.effectType
    
    def getCost(self):
        return self._cost

    def getName(self):
        return self._name
    
    # Handles effects
    def activateEffect(self):
        match self.effectIndex:
            case 1:
                return
            case 2:
                return