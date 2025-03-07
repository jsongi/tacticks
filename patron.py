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

    # Handles effects, chars will either be the list of characters or the character attacking an enemy
    def activateEffect(self, chars, enemies, enemy):
        match self._effectIndex:
            case 1: # Clergyman
                for char in chars:
                    char.addTotalHealth(5)
                return
            case 2: # Librarian
                for char in chars:
                    char.addMagic(1)
                return
            case 3: # Conqueror
                return
            case 4: # Physician
                for char in chars:
                    char.addHealth(15)
                return
            case 5: # Merchant
                return 
            case 6: # Armorer
                for char in chars:
                    char.addTotalHealth(40)
                return
            case 7: # Weapon-smith
                for char in chars:
                    char.addAttack(8)
                return
            case 8: # Magician
                return
            case 9: # Generalist
                return
            case 10: # Cobbler (?)
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
            case 15: # Conquistador
                for char in chars:
                    char.addRange(1)
                return
            case 16: # Duelist
                if chars.range() == 1: # Singular character should be passed here
                    enemy[1].update_health(15) # Tentative way we're doing flat buffs
                return
            case 17:
                return
            
    def handleSold(self, chars):
        return