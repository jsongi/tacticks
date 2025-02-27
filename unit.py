class Unit:

    def __init__(self, health: int, attack: int, range: int, movement: int, id: int, type: str, cost: int):
        self._health: int = health
        self._attack: int = attack
        self._range: int = range
        self._movement: int = movement
        self._id: int = id
        self._type: str = type
        self._cost: int = cost

    def health(self) -> int:
        return self._health
    
    def attack(self) -> int:
        return self._attack
    
    def range(self) -> int:
        return self._range

    def movement(self) -> int:
        return self._movement

    def id(self) -> int:
        return self._id

    def setId(self, id):
        self._id = id

    def cost(self) -> int:
        return self._cost

    def type(self) -> int:
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
        
        return charType
    
    def update_health(self, value: int) -> None:
        self._health = self._health - value
    
