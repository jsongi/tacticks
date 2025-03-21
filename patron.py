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
        self.statChanges = 0

    def getImage(self):
        return self._imageNum
    
    # End of round (1), on attack (2), after turn (3), during shop (4), during round (5), flat buff (6), on sell (7) end of shop phase (8)
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
                self.statChanges += 5
                return
            case 2: # Librarian
                for char in chars:
                    char.addMagic(1)
                self.statChanges += 1
                return
            case 3: # Conqueror
                for char in chars:
                    char.addAttack(1)
                self.statChanges += 1
                return
            case 4: # Physician
                for char in chars:
                    char.addHealth(15)
                return
            case 5: # Merchant
                gold[0] += 3
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
                for char in chars:
                    char.addMagic(8)
                return
            case 9: # Generalist
                for char in chars:
                    char.addAttack(6)
                    char.addMagic(6)
                return
            case 10: # Cobbler
                for char in chars:
                    char.addMovement(1)
                return
            case 11: # Peddler
                # Handled in shop
                return
            case 12: # Varlet
                return
            case 13: # Surgeon
                for char in chars:
                    char.addHealth(int(char.totalHealth() / 4))
                    if char.totalHealth() - 5 <= 0:
                        char.setTotalHealth(1)
                    else:
                        char.addTotalHealth(-5)
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
            case 17: # Mercantilist
                for char in chars:
                    char.addMagic(-1 * self.statChanges)
                    char.addAttack(-1 * self.statChanges)
                self.statChanges = gold[0] / 2
                for char in chars:
                    char.addMagic(self.statChanges)
                    char.addAttack(self.statChanges)
                return
            case 18: # Round Table
                for char in chars:
                    if char.type() == "Knight" or char.type() == "Executioner":
                        self.statChanges += 1
                for char in chars:
                    char.addTotalHealth(self.statChanges * 30)
                    char.addAttack(self.statChanges * 2)  
                return
            case 19: # Thieves Guild
                for char in chars:
                    if char._type == "Thief":
                        gold[0] += 2
                    if char._type == "Marauder":
                        gold[0] += 3
                return
            case 20: # Open Courts
                return
            case 21: # Glutton
                return
            case 22: # Ritualist
                return
            case 23: # Warlock
                return
            case 24: # Plague Doctor
                for enemy in enemies:
                    health = int(enemy[1].health() / 2)
                    if health > 0:
                        enemy[1].update_health(health)
                return
            case 25: # Necromancer
                return
            case 26: # Time Keeper
                return
            case 27: # Runekeeprs
                for char in chars:
                    if char.type() == "Wizard" or char.type() == "Archmage":
                        self.statChanges += 1
                for char in chars:
                    char.addTotalHealth(self.statChanges * 10)
                    char.addAttack(self.statChanges * 5)  
                return
            case 28: # Bull's Eye
                for char in chars:
                    if char.type() == "Archer" or char.type() == "Catapult":
                        self.statChanges += 1
                for char in chars:
                    char.addTotalHealth(self.statChanges * 10)
                    char.addAttack(self.statChanges * 4)  
                return
            case 29: # Inhibitors
                for char in chars:
                    char.addTotalHealth(20)
                    char.addAttack(6)
                    char.addMagic(-6)
                return
            case 30: # Conclave
                for char in chars:
                    char.addTotalHealth(10)
                    char.addAttack(-6)
                    char.addMagic(8)
                return
            case 31: # Trader
                return

    def onUnitSold(self, char, chars, enemies, enemy, gold, boardState):
        match self._effectIndex:
            case 1: # Clergyman
                return
            case 2: # Librarian
                return
            case 3: # Conqueror
                return
            case 4: # Physician
                return
            case 5: # Merchant
                return 
            case 6: # Armorer
                return
            case 7: # Weaponsmith
                return
            case 8: # Enchanter
                return
            case 9: # Generalist
                return
            case 10: # Cobbler
                return
            case 11: # Peddler
                return
            case 12: # Varlet
                gold[0] += 2
                return
            case 13: # Surgeon
                return
            case 14: #Jack
                return
            case 15: # Conquistador
                return
            case 16: # Duelist
                return
            case 17: # Mercantilist
                return
            case 18: # Round Table
                if char.type() == "Knight" or char.type() == "Executioner":
                    self.statChanges -= 1
                    for char in chars:
                        char.addHealth(-1 * 30)
                        char.addAttack(-1 * 2)        
                return
            case 19: # Thieves Guild
                return
            case 20: # Open Courts
                # Handled in shop
                return
            case 21: # Glutton
                return
            case 22: # Ritualist
                return
            case 23: # Warlock
                return
            case 24: # Plague Doctor
                return
            case 25: # Necromancer
                self.statChanges += 1
                for char in chars:
                    char.addAttack(5)
                    char.addMagic(5)
                    char.addTotalHealth(25)
                return
            case 26: # Time Keeper
                return
            case 27: # Runekeepers
                return
            case 28: # Bull's Eye
                if char.type() == "Archer" or char.type() == "Catapult":
                    self.statChanges -= 1
                    for char in chars:
                        char.addHealth(-1 * 10)
                        char.addAttack(-1 * 4)    
                return
            case 29: # Inhibitors
                return
            case 30: # Conclave
                return
            case 31: # Trader
                return
    
    def onUnitPurchase(self, char, chars, enemies, enemy, gold, boardState):
        match self._effectIndex:
            case 1: # Clergyman
                char.addTotalHealth(self.statChanges)
                return
            case 2: # Librarian
                char.addMagic(self.statChanges)
                return
            case 3: # Conqueror
                char.addAttack(self.statChanges)
                return
            case 4: # Physician
                return
            case 5: # Merchant
                return 
            case 6: # Armorer
                char.addTotalHealth(40)
                return
            case 7: # Weaponsmith
                char.addAttack(8)
                return
            case 8: # Enchanter
                char.addMagic(8)
                return
            case 9: # Generalist
                char.addAttack(6)
                char.addMagic(6)
                return
            case 10: # Cobbler
                char.addMovement(1)
                return
            case 11: # Peddler
                # Handled in shop
                return
            case 12: # Varlet
                # Handled in shop
                return
            case 13: # Surgeon
                return
            case 14: #Jack
                char.addTotalHealth(30)
                char.addAttack(8)
                char.addMagic(8)
                return
            case 15: # Conquistador
                char.addRange(1)
                return
            case 16: # Duelist
                return
            case 17: # Mercantilist
                char.addMagic(self.statChanges)
                char.addAttack(self.statChanges)
                return
            case 18: # Round Table
                char.addTotalHealth(self.statChanges * 30)
                char.addAttack(self.statChanges * 2) 
                if char.type() == "Knight" or char.type() == "Executioner":
                    self.statChanges += 1
                    for c in chars:
                        c.addTotalHealth(30)
                        c.addAttack(2)
                return
            case 19: # Thieves Guild
                return
            case 20: # Open Courts
                # Handled in shop
                return
            case 21: # Glutton
                return
            case 22: # Ritualist
                return
            case 23: # Warlock
                return
            case 24: # Plague Doctor
                return
            case 25: # Necromancer
                char.addMagic(self.statChanges * 5)
                char.addAttack(self.statChanges * 5)
                char.addTotalHealth(self.statChanges * 25)
                return
            case 26: # Time Keeper
                return
            case 28: # Bull's Eye
                char.addTotalHealth(self.statChanges * 10)
                char.addAttack(self.statChanges * 4)
                if char.type() == "Archer" or char.type() == "Catapult":
                    self.statChanges += 1
                    for char in chars:
                        char.addTotalHealth(10)
                        char.addAttack(4)   
                return
            case 29: # Inhibitors
                char.addTotalHealth(20)
                char.addAttack(6)
                char.addMagic(-6)
                return
            case 30: # Conclave
                char.addTotalHealth(10)
                char.addAttack(-6)
                char.addMagic(8)
                return
            case 31: # Trader
                return

    def handleSold(self, chars, enemies, enemy, gold, boardState):
        match self._effectIndex:
            case 1: # Clergyman
                for char in chars:
                    char.addTotalHealth(-1 * self.statChanges)
                    char.addHealth(self.statChanges)
                self.statChanges = 0
                return
            case 2: # Librarian
                for char in chars:
                    char.addMagic(-1 * self.statChanges)
                self.statChanges = 0
                return
            case 3: # Conqueror
                for char in chars:
                    char.addAttack(-1 * self.statChanges)
                self.statChanges = 0
                return
            case 4: # Physician
                return
            case 5: # Merchant
                return 
            case 6: # Armorer
                for char in chars:
                    char.addTotalHealth(-40)
                    char.addHealth(40)
                return
            case 7: # Weaponsmith
                for char in chars:
                    char.addAttack(-8)
                return
            case 8: # Enchanter
                for char in chars:
                    char.addMagic(-8)
                return
            case 9: # Generalist
                for char in chars:
                    char.addAttack(-6)
                    char.addMagic(-6)
                return
            case 10: # Cobbler
                for char in chars:
                    char.addMovement(-1)
                return
            case 11: # Peddler
                # Handled in shop
                return
            case 12: # Varlet
                return
            case 13:
                return
            case 14: #Jack
                for char in chars:
                    char.addTotalHealth(-30)
                    char.addAttack(-8)
                    char.addMagic(-8)
                    char.addHealth(30)
                return
            case 15: # Conquistador
                for char in chars:
                    char.addRange(-1)
                return
            case 16: # Duelist
                if chars.range() == 1: # Singular character should be passed here
                    enemy[1].update_health(15) # Tentative way we're doing flat buffs
                return
            case 17: # Mercantilist
                for char in chars:
                    char.addMagic(-1 * self.statChanges)
                    char.addAttack(-1 * self.statChanges)
                self.statChanges = 0
                return
            case 18: # Round Table
                for char in chars:
                    char.addTotalHealth(self.statChanges * -30)
                    char.addAttack(self.statChanges * 2)
                    char.addHealth(self.statChanges * 30)
                self.statChanges = 0
                return
            case 19: # Thieves Guild
                return
            case 20: # Open Courts
                return
            case 21: # Glutton
                return
            case 22: # Ritualist
                return
            case 23: # Warlock
                return
            case 24: # Plague Doctor
                return            
            case 25: # Necromancer
                for char in chars:
                    char.addMagic(-1 * self.statChanges * 5)
                    char.addAttack(-1 * self.statChanges * 5)
                    char.addTotalHealth(-1 * self.statChanges * 25)
                    char.addHealth(self.statChanges * 25)
                return
            case 26: # Time Keeper
                return
            case 27: # Runekeepers
                return
            case 28: # Bull's Eye
                for char in chars:
                    char.addTotalHealth(self.statChanges * -10)
                    char.addAttack(self.statChanges * 4)
                    char.addHealth(self.statChanges * 10)
                self.statChanges = 0
                return
            case 29: # Inhibitors         
                for char in chars:
                    char.addTotalHealth(-20)
                    char.addAttack(-6)
                    char.addMagic(6)
                return
            case 30: # Conclave
                for char in chars:
                    char.addTotalHealth(-10)
                    char.addAttack(6)
                    char.addMagic(-8)
                return
            case 31: # Trader
                return
        return