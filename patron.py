class Patron:

    def __init__(self, imageNum, effectType, effectIndex, cost, name, rarity, description):
        self._imageNum = imageNum
        self._effectType = effectType
        self._effectIndex = effectIndex
        self._cost = cost
        self._name = name
        self._rarity = rarity
        self._description = description
        self._purchased = False

    def getImage(self):
        return self._imageNum
    
    # End of round (1), on attack (2), after turn (3), during shop (4), during round (5), flat buff (6)
    def getEffectType(self):
        return self._effectType

    def getCost(self):
        return self._cost

    def getName(self):
        return self._name

    def getRarity(self):
        return self._rarity

    def getPurchased(self):
        return self._purchased
    
    def getDescription(self):
        return self._description

    def setPurchased(self, status):
        self._purchased = status    

    # Handles effects, chars will either be the list of characters or the character attacking an enemy
    def activateEffect(self, chars, enemies, enemy, gold, boardState):
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
            case 7: # Weaponsmith
                for char in chars:
                    char.addAttack(8)
                return
            case 8: # Enchanter
                return
            case 9: # Generalist
                return
            case 10: # Cobbler
                return
            case 11: # Peddler
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
            case 18:
                return
            case 19:
                return
            case 20:
                return
            case 21:
                return
            case 22:
                return
            case 23:
                return
            case 24: # Plague Doctor
                for enemy in enemies:
                    health = int(enemy[1].health() / 2)
                    if health > 0:
                        enemy[1].update_health(health)
                return
            
    def handleSold(self, chars):
        return