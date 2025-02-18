import pygame
from collections import deque
from enemy import Enemy

cell_width = 32
cell_height = 32

class Board:
    def __init__(self, assets):
        self.enemyTypes = [9]
        self.idTypes = []
        self.boardState = []
        self.char_positions = []
        self.enemy_positions = []
        self.enemy_positions_highlighted = []
        self.images = []
        self.visited = set()
        for image in assets:
            self.images.append(pygame.image.load(image)) 

    def check_click(self, mouse_x, mouse_y, cell_width, cell_height): # return position and id
        if mouse_x < 20:
            return None
        elif mouse_y < 20:
            return None

        boardxpos = (mouse_y // cell_height) - 1
        boardypos = (mouse_x // cell_width) - 1

        for char_row, char_col in self.char_positions:  # Iterate through character char_positions
            char_pixel_x = char_col * cell_width
            char_pixel_y = char_row * cell_height

            # Check if the click falls within the character's cell
            if char_pixel_x + 25 <= mouse_x < char_pixel_x + cell_width + 25 and char_pixel_y + 25 <= mouse_y < char_pixel_y + cell_height + 25:
                return ([(char_row, char_col), self.boardState[char_row][char_col]])  # Return id of the targeted character

        if((0 <= boardxpos <= 8) and (0 <= boardypos <= 8)):
            # If the position is an in range enemy position (highlighted) then we need to return some signifier that it's a valid attack action
            # The way this clears highlights is ugly
            if (any(tup == (boardxpos, boardypos) for tup, obj in self.enemy_positions)):
                if ((boardxpos, boardypos) in self.enemy_positions_highlighted): # Valid attack action
                    self.clear_highlights()
                    return [(boardxpos, boardypos), 9] # just using 9 as a signifier for now(?)
                else:
                    self.clear_highlights()
                    return [(boardxpos, boardypos), 0] # basically a dead click
            if (self.boardState[boardxpos][boardypos] != 1):
                self.clear_highlights()
            return [(boardxpos, boardypos), self.boardState[boardxpos][boardypos]]
        else:
            return None

    def clear_highlights(self):
        if len(self.visited) > 1: # Movement previously calculated
            for row, col in self.visited:
                tile_value = self.boardState[row][col]
                if tile_value == 1 or tile_value == 10:
                    self.boardState[row][col] = 0

            self.visited = set() # Clear set for new movement calculation
        self.enemy_positions_highlighted = []

    def show_actions(self, screen, selectedRow, selectedCol, chars, id):
        movement_range = chars[id - 2].movement()  # Get movement range
        rows, cols = len(self.boardState), len(self.boardState[0])  # Board dimensions

        self.clear_highlights()

        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(selectedRow, selectedCol, 0)])
        self.visited.add((selectedRow, selectedCol))  # Mark starting point as visited

        while queue:
            row, col, steps = queue.popleft()

            # Stop BFS when max movement range is reached
            if steps >= movement_range:
                continue

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in self.visited):               
                    
                    tile_value = self.boardState[new_row][new_col]
                    self.visited.add((new_row, new_col))  # Mark as visited
    
                    if tile_value > 7: #If friendly character, do not mark tile but continue search
                        continue

                    queue.append((new_row, new_col, steps + 1))  # Enqueue with step count

                    # Draw movement highlight on screen (assuming image 1 is a highlight texture)
                    if tile_value == 0:
                        screen.blit(self.images[1], (new_col * cell_width, new_row * cell_height))
                        
        for row, col in self.visited:
            tile_value = self.boardState[row][col]
            if tile_value == 0:
                self.boardState[row][col] = 1
            elif tile_value in self.enemyTypes: # Attack enemy check
                
                self.enemy_positions_highlighted.append((row, col))

    def execute_attack(self, char_pos, enemy_pos, chars):
        #TODO: Check range, if melee move into melee range, if ranged then we don't care because only valid highlights should've been calculated
        #Execute attack onto the target enemy, reduce their hp by the characters attack, apply any additional effects onto them from other characters
        
        self.clear_highlights()

        #TODO: Checks for enhancements on characters, end of turn / beginning of turn or passive effects
        char_x_pos, char_y_pos = char_pos
        enemy_x_pos, enemy_y_pos = enemy_pos
        char = None
        enemy = None

        char_id = self.boardState[char_x_pos][char_y_pos]
        for c in chars:
            if char_id == c.id():
                char = c
                break        

        for e in self.enemy_positions:
            if e[0] == (enemy_x_pos, enemy_y_pos):
                enemy = e

        enemy[1].update_health(c.attack())

        if enemy[1].health() <= 0:
            self.boardState[enemy_x_pos][enemy_y_pos] = 0
            # Modifies the list of enemies in place to remove the targeted enemy
            self.enemy_positions[:] = [entry for entry in self.enemy_positions if entry[0] != (enemy_x_pos, enemy_y_pos)] 

        return

    def read_board(self, level, chars, round):
        capturing = False
        lineNum = 0
        usedChars = 0

        with open("levels.txt", 'r') as file:
            
            for line in file:
                if level in line:  # Find start marker
                    capturing = True
                    continue
                
                if capturing:
                    if "nd" in line:  # Stop when reaching end marker
                        break
                    
                    row = []
            
                    for num in map(int, line.split()):  # Convert each number to int
                        if num == 1:
                            if usedChars < len(chars):  
                                row.append(chars[usedChars].id())  # Replace with available char
                                self.char_positions.append((lineNum, len(row) - 1))  # Store (row, col)
                                self.idTypes.append((chars[usedChars].id(), chars[usedChars].type()))
                                usedChars += 1
                            else:
                                row.append(0)  # Replace with 0 if no available chars left
                        else:
                            if num in self.enemyTypes:
                                self.enemy_positions.append(((lineNum, len(row)), Enemy(round, 9)))
                            row.append(num)  # Keep other numbers unchanged

                    self.boardState.append(row)  # Store updated row
                    lineNum += 1

    def update_board(self, click_status, last_clicked):
        for i in range(len(self.char_positions)):
            if self.char_positions[i] == last_clicked:
                self.char_positions[i] = click_status[0]
                continue
        #this is ugly
        temp = -1
        row1 = click_status[0][0]
        col1 = click_status[0][1]
        row2 = last_clicked[0]
        col2 = last_clicked[1]
        temp = self.boardState[row1][col1]
        self.boardState[row1][col1] = self.boardState[row2][col2]
        self.boardState[row2][col2] = temp
        self.clear_highlights()

    def move_enemies(self, chars):

        for enemy in self.enemy_positions:
            old_pos = enemy[0][0], enemy[0][1]
            movement_range = enemy[1].movement() 
            attack_range = enemy[1].range()  
            attack_value = enemy[1].attack()  
            rows, cols = len(self.boardState), len(self.boardState[0])
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            queue = deque([(enemy[0][0], enemy[0][1], [])])  # (row, col, steps, path)
            char_x_pos = 0
            char_y_pos = 0
            visited = set()
            
            while queue:
                row, col, path = queue.popleft()
                if (row, col) in self.char_positions:
                    char_x_pos, char_y_pos = row, col
                    break # Move exactly movement_range steps
                
                # Continue searching within movement range
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    new_pos = (new_row, new_col)

                    if (0 <= new_row < rows and 0 <= new_col < cols and  # Stay in bounds
                        new_pos not in visited and                     # Avoid revisiting
                        new_pos not in self.enemy_positions and             # Avoid other enemies
                        0 <= self.boardState[new_row][new_col] <= 7):            # Only move on passable tiles
                        
                        visited.add(new_pos)
                        queue.append((new_row, new_col, path + [new_pos]))
            # We finished searching the movement range, move the enemy to new position calculated

            #TODO: this is also ugly
            if len(path) - 1 <= attack_range: # Either do not move, and attack targeted character, or move into the targeted character and attack
                if len(path) - 1 == attack_range and attack_range == 1: # melee units should move into range to attack
                    print("here")
                    new_pos = path[0]
                    for i, (pos, enemy) in enumerate(self.enemy_positions): #this is not efficient
                        if pos == old_pos:
                            
                            self.boardState[old_pos[0]][old_pos[1]] = 0
                            self.enemy_positions[i] = (new_pos, enemy)  # Replace tuple with new position
                            self.boardState[new_pos[0]][new_pos[1]] = enemy.id()
                            continue  # Exit loop after updating
                # Find the id of the targeted character and update health
                if len(path) - 1 <= attack_range:
                    for c in chars:
                        if c.id() == self.boardState[char_x_pos][char_y_pos]:
                            c.update_health(attack_value)
                            print(c.health())
                            if c.health() < 0:
                                self.boardState[char_x_pos][char_y_pos] = 0

            else: # Out of attack range, move as close as possible
                new_pos = path[movement_range - 1] if len(path) >= movement_range else path[-1]
                for i, (pos, enemy) in enumerate(self.enemy_positions): #this is not efficient
                    if pos == old_pos:
                        
                        self.boardState[old_pos[0]][old_pos[1]] = 0
                        self.enemy_positions[i] = (new_pos, enemy)  # Replace tuple with new position
                        self.boardState[new_pos[0]][new_pos[1]] = enemy.id()
                        continue  # Exit loop after updating

        return 0  # No valid move found, stay in place

    def display(self, screen, displayType, chars):
        match displayType[0]:
            case "charSelected":
                selectedRow = -1
                selectedCol = -1
                id = displayType[1]
                # Draw images under characters
                for row, col in self.char_positions:
                    if self.boardState[row][col] == id: # Check which character is selected through id
                        screen.blit(self.images[1], (col * cell_width, row * cell_height))
                        selectedRow = row
                        selectedCol = col
                    else:
                        screen.blit(self.images[0], (col * cell_width, row * cell_height))
                for (row, col), _ in self.enemy_positions:
                    if (row, col) in self.enemy_positions_highlighted:
                        screen.blit(self.images[10], (col * cell_width, row * cell_height))
                    else:
                        screen.blit(self.images[0], (col * cell_width, row * cell_height))

                # Draw rest of board
                for row in range(len(self.boardState)):
                    for col in range(len(self.boardState[0])):
                        x = col * cell_width
                        y = row * cell_height
                        if(2 <= int(self.boardState[row][col]) <= 7):
                            for pair in self.idTypes:
                                if int(self.boardState[row][col]) == pair[0]:
                                    screen.blit(self.images[pair[1]], (x, y))
                                    break
                        else:
                            screen.blit(self.images[int(self.boardState[row][col])], (x, y))
                
                self.show_actions(screen, selectedRow, selectedCol, chars, id)

            case "default":
                self.clear_highlights()
                # Draw image under characters first
                for row, col in self.char_positions:
                    screen.blit(self.images[0], (col * cell_width, row * cell_height))
                for (row, col), _ in self.enemy_positions:
                    screen.blit(self.images[0], (col * cell_width, row * cell_height))


                for row in range(len(self.boardState)):
                    for col in range(len(self.boardState[0])):
                        x = col * cell_width
                        y = row * cell_height
                        if(2 <= int(self.boardState[row][col]) <= 7):
                            for pair in self.idTypes:
                                if int(self.boardState[row][col]) == pair[0]:
                                    screen.blit(self.images[pair[1]], (x, y))
                        else:
                            screen.blit(self.images[int(self.boardState[row][col])], (x, y))
                        