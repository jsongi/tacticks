class Unit:

    def __init__(self, health: int, attack: int, magic: int, range: int, movement: int, id: int, type: str, cost: int):
        self._health: int = health
        self._attack: int = attack
        self._magic: int = magic
        self._range: int = range
        self._movement: int = movement
        self._id: int = id
        self._type: str = type
        self._cost: int = cost

    def health(self) -> int:
        return self._health
    
    def attack(self) -> int:
        return self._attack
    
    def magic(self) -> int:
        return self._magic

    def range(self) -> int:
        return self._range

    def movement(self) -> int:
        return self._movement

    def addHealth(self, value):
        self._health += value

    def addAttack(self, value):
        self._attack += value

    def addMagic(self, value):
        self._magic += value
    
    def addRange(self, value):
        self._range += value
    
    def addMovement(self, value):
        self._range += value

    def id(self) -> int:
        return self._id

    def setId(self, id):
        self._id = id

    def getCost(self) -> int:
        return self._cost

    def type(self):
        return self._type

    def typeImage(self) -> int:
        charType = -1

        if(self._type == "Knight"):
            charType = 4
        elif(self._type == "Thief"):
            charType = 5
        elif(self._type == "Archer"):
            charType = 6
        elif(self._type == "Wizard"):
            charType = 7
        elif(self._type == "Healer"):
            charType = 8
        elif(self._type == "Executioner"):
            charType = 9
        elif(self._type == "Gambler"):
            charType = 10
        elif(self._type == "Ballista"):
            charType = 11
        elif(self._type == "Archmage"):
            charType = 12
        elif(self._type == "Mystic"):
            charType = 13

        return charType
    
    def update_health(self, value: int) -> None:
        self._health = self._health - value
    
