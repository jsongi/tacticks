class Unit:

    def __init__(self, health: int, attack: int, range: int, movement: int, id: int, type: str):
        self._health: int = health
        self._attack: int = attack
        self._range: int = range
        self._movement: int = movement
        self._id: int = id
        self._type: str = type

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

    def type(self) -> int:
        charType = -1

        if(self._type == "knight"):
            charType = 7
        elif(self._type == "archer"):
            charType = 3
        
        return charType
    
    def update_health(self, value: int) -> None:
        self._health = self._health - value
    
