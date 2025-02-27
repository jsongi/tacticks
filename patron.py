class Patron:

    def __init__(self, imageNum, effectType, effectIndex, cost, name):
        self._imageNum = imageNum
        self._effectType = effectType
        self._effectIndex = effectIndex
        self._cost = cost
        self._name = name

    def getImage(self):
        return self._imageNum
    
    # Beginning of round (1), on attack (2), after turn (3), during shop (4), during round (5),
    def getEffectType(self):
        return self._effectType

    def getCost(self):
        return self._cost

    def getName(self):
        return self._name

    # Handles effects
    def activateEffect(self):
        match self._effectIndex:
            case 1:
                return
            case 2:
                return