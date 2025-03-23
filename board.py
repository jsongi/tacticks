import pygame
from collections import deque
from enemy import Enemy

cell_width = 32
cell_height = 32

pygame.font.init()
font = pygame.font.Font(None, 28)
class Board:
    def __init__(self, assets):
        self.enemyTypes = [14, 15, 16, 17, 18, 19, 20, 21, 22]
        self.idTypes = []
        self.boardState = []
        self.char_positions = []
        self.enemy_positions = []
        self.enemy_positions_highlighted = []
        self.images = []
        self.visited = set()
        self.visited_attacks = set()
        for image in assets:
            self.images.append(pygame.image.load(image)) 

    def check_click(self, mouse_x, mouse_y, cell_width, cell_height): # return position and id
        #if mouse_x < 20:
        #    return None
        #elif mouse_y < 20:
        #    return None

        boardxpos = (mouse_y // cell_height) - 1
        boardypos = (mouse_x // cell_width) - 1

        for char_row, char_col in self.char_positions:  # Iterate through character char_positions
            char_pixel_x = char_col * cell_width
            char_pixel_y = char_row * cell_height

            # Check if the click falls within the character's cell
            if char_pixel_x + 25 <= mouse_x < char_pixel_x + cell_width + 25 and char_pixel_y + 25 <= mouse_y < char_pixel_y + cell_height + 25:
                return ([(char_row, char_col), self.boardState[char_row][char_col]])  # Return id of the targeted character

        # Check skip button
        if 550 <= mouse_x <= 650 and 600 <= mouse_y <= 650:
            return [(boardxpos, boardypos), -3]

        if((0 <= boardxpos <= 8) and (0 <= boardypos <= 8)):
            # If the position is an in range enemy position (highlighted) then we need to return some signifier that it's a valid attack action
            # The way this clears highlights is ugly
            if (any(tup == (boardxpos, boardypos) for tup, obj in self.enemy_positions)):
                if ((boardxpos, boardypos) in self.enemy_positions_highlighted): # Valid attack action
                    self.clear_highlights()
                    return [(boardxpos, boardypos), -1] # just using -1 as a signifier for now(?)
                else:
                    self.clear_highlights()
                    return [(boardxpos, boardypos), -2] # enemy selected
            if (self.boardState[boardxpos][boardypos] != 1):
                self.clear_highlights()
            return [(boardxpos, boardypos), self.boardState[boardxpos][boardypos]]
        else:
            return None

    def clear_highlights(self):
        if len(self.visited) > 1: # Movement previously calculated
            for row, col in self.visited:
                tile_value = self.boardState[row][col]
                if tile_value == 1 or tile_value == 3:
                    self.boardState[row][col] = 0

            for row, col in self.visited_attacks:
                tile_value = self.boardState[row][col]
                if tile_value == 1 or tile_value == 3:
                    self.boardState[row][col] = 0

            self.visited = set() # Clear set for new movement calculation
            self.visited_attacks = set()

        self.enemy_positions_highlighted = []

    def show_actions(self, screen, selectedRow, selectedCol, chars, id):
        for char in chars:
            if char.id() == id:
                attack_range = char.range()
                movement_range = char.movement()  # Get movement range
        rows, cols = len(self.boardState), len(self.boardState[0])  # Board dimensions
        search_attack_actions = False
        searching_attacks = False

        if attack_range > movement_range:
            search_attack_actions = True

        self.clear_highlights()

        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(selectedRow, selectedCol, 0)])
        self.visited.add((selectedRow, selectedCol))  # Mark starting point as visited

        while queue:
            row, col, steps = queue.popleft()

            # Stop BFS when max movement range is reached
            if steps >= movement_range:
                if search_attack_actions:
                    if steps >= attack_range:
                        continue
                    else:
                        searching_attacks = True
                else:
                    continue    

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in self.visited):               
                    
                    tile_value = self.boardState[new_row][new_col]
                    if searching_attacks:
                        self.visited_attacks.add((new_row, new_col))
                    else:
                        self.visited.add((new_row, new_col))  # Mark as visited
    
                    #if 4 <= tile_value <= 9: #If friendly character, do not mark tile but continue search
                        #continue

                    queue.append((new_row, new_col, steps + 1))  # Enqueue with step count
                    # Draw movement highlight on screen (assuming image 1 is a highlight texture)
                    if tile_value == 0 and not searching_attacks:
                        screen.blit(self.images[1], (new_col * cell_width, new_row * cell_height))

        for row, col in self.visited:
            tile_value = self.boardState[row][col]
            if tile_value == 0:
                self.boardState[row][col] = 1
            elif tile_value in self.enemyTypes: # Attack enemy check
                self.enemy_positions_highlighted.append((row, col))

        for row, col in self.visited_attacks:
            tile_value = self.boardState[row][col]
            if tile_value in self.enemyTypes: # Attack enemy check
                self.enemy_positions_highlighted.append((row, col))

    def execute_attack(self, char_pos, enemy_pos, chars, patrons, gold):
        #TODO: Check range, if melee move into melee range, if ranged then we don't care because only valid highlights should've been calculated
        #Execute attack onto the target enemy, reduce their hp by the characters attack, apply any additional effects onto them from other characters
        
        self.clear_highlights()

        char_x_pos, char_y_pos = char_pos
        char = None

        char_id = self.boardState[char_x_pos][char_y_pos]
        for c in chars:
            if char_id == c.id():
                char = c
                break        

        char.handle_attack(self.enemy_positions, patrons, self.boardState, enemy_pos, gold)   

        return len(self.enemy_positions)

    def read_board(self, level, chars, round):
        capturing = False
        lineNum = 0

        # Clear board state to read in fresh level
        self.boardState = []
        self.char_positions = []
        self.idTypes = []

        with open("levels.txt", 'r') as file:
            
            for line in file:        
                if level == line.strip():  # Find start marker
                    capturing = True
                    continue
                
                if capturing:
                    if "nd" == line.strip():  # Stop when reaching end marker
                        break
                    
                    row = []
            
                    for colNum, num in enumerate(map(int, line.split())):  # Convert each number to int
                        if num == 1:
                            matching_char = next((char for char in chars if char.location() == (lineNum, colNum)), None)

                            if matching_char:
                                row.append(matching_char.id())  # Keep character in correct place
                                self.char_positions.append((lineNum, colNum))  # Store updated (row, col)
                                self.idTypes.append((matching_char.id(), matching_char.typeImage()))
                            else:
                                row.append(0)  # If no character assigned, keep as empty
                        else:
                            if num in self.enemyTypes:
                                self.enemy_positions.append(((lineNum, len(row)), Enemy(round, num)))
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
                        new_pos not in self.enemy_positions):
                        if(self.boardState[new_row][new_col] <= 1 or 
                        4 <= self.boardState[new_row][new_col] <= 9):           # Only move on passable tiles
                        
                            visited.add(new_pos)
                            queue.append((new_row, new_col, path + [new_pos]))
            # We finished searching the movement range, move the enemy to new position calculated

            enemy[1].handle_effects(chars, self.boardState, self.char_positions)

            #TODO: this is also ugly
            if len(path) - 1 <= attack_range: # Either do not move, and attack targeted character, or move into the targeted character and attack
                if len(path) - 1 == attack_range and attack_range == 1: # melee units should move into range to attack
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
                            if c.health() <= 0:
                                self.boardState[char_x_pos][char_y_pos] = 0
                                chars.remove(c)

            else: # Out of attack range, move as close as possible    
                new_pos = path[movement_range - 1] if len(path) >= movement_range else path[-1]
                if new_pos in self.char_positions:
                    new_pos = path[-1 - 1]
                for i, (pos, enemy) in enumerate(self.enemy_positions): #this is not efficient
                    if pos == old_pos:
                        
                        self.boardState[old_pos[0]][old_pos[1]] = 0
                        self.enemy_positions[i] = (new_pos, enemy)  # Replace tuple with new position
                        self.boardState[new_pos[0]][new_pos[1]] = enemy.id()
                        continue  # Exit loop after updating

        return 0  # No valid move found, stay in place

    def activate_patrons(self, chars, patrons, gold):
        for patron in patrons:
            if patron.getEffectType() == 3:
                patron.activateEffect(chars, self.enemy_positions, None, gold, self.boardState)

    def display(self, screen, displayType, chars, patrons):
        selected_enemy = None

        screen.fill((255, 255, 255))
        
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
                        screen.blit(self.images[3], (col * cell_width, row * cell_height))
                    else:
                        screen.blit(self.images[0], (col * cell_width, row * cell_height))

                # Draw rest of board
                for row in range(len(self.boardState)):
                    for col in range(len(self.boardState[0])):
                        x = col * cell_width
                        y = row * cell_height
                        if(4 <= int(self.boardState[row][col]) <= 9):
                            for pair in self.idTypes:
                                if int(self.boardState[row][col]) == pair[0]:
                                    screen.blit(self.images[pair[1]], (x, y))
                                    break
                        else:
                            screen.blit(self.images[int(self.boardState[row][col])], (x, y))
                
                self.show_actions(screen, selectedRow, selectedCol, chars, id)

            case "enemySelected":               
                # Draw image under characters first
                for row, col in self.char_positions:
                    screen.blit(self.images[0], (col * cell_width, row * cell_height))
                for (row, col), e in self.enemy_positions:
                    if displayType[1] == (row, col):
                        selected_enemy = e
                        screen.blit(self.images[1], (col * cell_width, row * cell_height))
                    else:
                        screen.blit(self.images[0], (col * cell_width, row * cell_height))
                
                # Draw rest of board
                for row in range(len(self.boardState)):
                    for col in range(len(self.boardState[0])):
                        x = col * cell_width
                        y = row * cell_height
                        if(4 <= int(self.boardState[row][col]) <= 9):
                            for pair in self.idTypes:
                                if int(self.boardState[row][col]) == pair[0]:
                                    screen.blit(self.images[pair[1]], (x, y))
                                    break
                        else:
                            screen.blit(self.images[int(self.boardState[row][col])], (x, y))

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
                        if(4 <= int(self.boardState[row][col]) <= 9):
                            for pair in self.idTypes:
                                if int(self.boardState[row][col]) == pair[0]:
                                    screen.blit(self.images[pair[1]], (x, y))
                        else:
                            screen.blit(self.images[int(self.boardState[row][col])], (x, y))
        
        # Drawing UI
        pygame.draw.rect(screen, (255, 215, 0), (550, 600, 100, 50))
        skip_text = font.render(f"End turn", True, (0, 0, 0))
        screen.blit(skip_text, (560, 615))

        # Draw character stats
        x = 0
        y = 300

        for char in chars:
            if displayType[0] == "charSelected" and id == char.id():
                screen.blit(self.images[1], (x, y))
            if char.magicUser():
                text_surface = font.render(f"{char.health()} / {char.total_health()} - Magic: {char.magic()} - Range: {char.range()} - Movement: {char.movement()}", True, (0, 0, 0))
            else:
                text_surface = font.render(f"{char.health()} / {char.total_health()} - Attack: {char.attack()} - Range: {char.range()} - Movement: {char.movement()}", True, (0, 0, 0))
            screen.blit(self.images[char.typeImage()], (x, y))
            screen.blit(text_surface, (x + 70, y + 32))
            y += 32

        y = 500
        # Draw patrons
        for patron in patrons:
            screen.blit(self.images[patron.getImage()], (x, y))
            x += 35
        
        x = 350
        y = 10
        for (row, col), enemy in self.enemy_positions:
            if selected_enemy is not None:
                if selected_enemy == enemy:
                    screen.blit(self.images[1], (x, y))
            screen.blit(self.images[enemy.id()], (x, y))
            text_surface = font.render(f"{enemy.health()} / {enemy.total_health()} - Attack: {enemy.attack()} - Range: {enemy.range()} - Movement: {enemy.movement()}", True, (0, 0, 0))
            screen.blit(text_surface, (x + 70, y + 32))
            y += 32

        pygame.display.flip()

        # TODO: UI for enemies

