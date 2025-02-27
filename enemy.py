class Enemy:

    def __init__(self, round, id):
        self.stats = [
            [25, 5, 1, 2, 14, "Beetle"], # Beetle
            [15, 3, 3, 2, 15, "Tick"], # Tick
            [], # Articklery
                ]
        
        self.selected_stats = 0

        match id:
            case 9:
                self.selected_stats = self.stats[0]
            case 10:
                self.selected_stats = self.stats[1]
            case _:
                self.selected_stats = self.stats[0] # Error, default to beetle stats
        
        self._health: int = self.selected_stats[0] * round # round should be some slow exponential value just on hp and attack, movement and range creep should not exist(?)
        self._attack: int = self.selected_stats[1] * round
        self._range: int = self.selected_stats[2]
        self._movement: int = self.selected_stats[3]
        self._id: int = self.selected_stats[4]
        self._type = self.selected_stats[5]

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
    
    def update_health(self, value: int) -> None:
        self._health = self._health - value
    
