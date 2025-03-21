class Enemy:

    def __init__(self, round, id):
        # 14 - 22 for enemy image indexes
        self.stats = [
            [10, 2, 1, 2, 14, "Tick"], # Tick
            [5, 3, 3, 2, 15, "Beetle"], # Beetle
            [5, 1, 1, 4, 16, "Mite"], # Mite
            [30, 1, 1, 1, 17, "Roach"], # Roach
            [10, 5, 5, 1, 18, "Bombardier Beetle"], # Bombardier beetle
            [50, 5, 1, 2, 19, "Boss"], # Boss 1
            [100, 8, 1, 2, 20, "Boss"] # Boss 2
            ]
        
        self.selected_stats = 0
        health_growth = 0
        attack_growth = 0

        match id:
            case 14:
                self.selected_stats = self.stats[0]
            case 15:
                self.selected_stats = self.stats[1]
            case 16:
                self.selected_stats = self.stats[2]
            case _:
                self.selected_stats = self.stats[0] # Error, default to beetle stats
        if round > 3:
            health_growth = int(2 * pow(1.2, round))
            attack_growth = int(2 * pow(1.07, round))
        
        self._total_health: int = self.selected_stats[0] + health_growth # round should be some slow exponential value just on hp and attack, movement and range creep should not exist(?)
        self._health: int = self.selected_stats[0] + health_growth
        self._attack: int = self.selected_stats[1] + attack_growth
        self._range: int = self.selected_stats[2]
        self._movement: int = self.selected_stats[3]
        self._id: int = self.selected_stats[4]
        self._type = self.selected_stats[5]

    def total_health(self) -> int:
        return self._total_health

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

    def handle_effects(self, chars, boardState, char_positions):
        match self._id:
            case 20: 
                for c in chars:
                    if c.health() - self._attack / 5 < 0:
                        c.set_health(1)
                    else:
                        c.update_health((int)(self._attack / 5))
            case 15:
                return
            case 16:
                return                
                
        return
    
