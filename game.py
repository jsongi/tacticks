import pygame
import random
#from enemy import 
from board import Board
from unit import Unit
from shop import Shop

assets = [
    "assets/grasstile.png", # 0
    "assets/movementhighlight.png", # 1
    "assets/mountaintile.png", # 2
    "assets/attackhighlight.png", # 3
    "assets/knight.png", #knight 4
    "assets/thief.png", #thief 5
    "assets/archer.png", # 6
    "assets/wizard.png", # 7
    "assets/healer.png", # 8
    "assets/executioner.png", #executioner 9
    "assets/marauder.png", #marauder 10
    "assets/catapult.png", #catapult 11
    "assets/archmage.png", #archmage 12
    "assets/mystic.png", #mystic 13
    "assets/bug1.png", # 14
    "assets/bug2.png", # 15
    "assets/tempgrasstile.png", # enemy type, 16
    "assets/tempgrasstile.png", # enemy type, 17
    "assets/tempgrasstile.png", # enemy type, 18
    "assets/tempgrasstile.png", # enemy type, 19
    "assets/tempgrasstile.png", # enemy type, 20
    "assets/tempgrasstile.png", # enemy type, 21
    "assets/tempgrasstile.png", # enemy type, 22
    "assets/plaguedoctor.png", # , 23
    "assets/jackofalltrades.png", # , 24
    "assets/clergyman.png", # 25
    "assets/librarian.png" # 26
]
levels = [["aaa", "aab", "aac", "aad", "aae"]
          
          ]
#["aba", "abb", "abc", "abd", "abe"],
#id has to start from 4
unit1 = Unit(40, 40, 5, 0, 8, 2, 4, "Knight", 4, False)
patrons = []
chars = [unit1] # , unit2, unit3, unit4 
char_moves = []
turn_counter = 5
level = "aaa"
level_counter = -1
current_level = 3
selected_levels = []
player_actions = 0
is_player_turn = True
last_clicked = -1
round = 1
result = 1
gold = 9999 #set as this for testing, lower to 5(?) later
game_state = "shop"
enemies_remaining = 1

# Initialize Pygame
pygame.init()

# Get the user's screen resolution
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Set the window size to be the screen width and height
window_width = int(width * 1)
window_height = int(height * 1)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tacticks")

# Width of images can be variable, current tiles are 31x31 pixels
cell_width = 31
cell_height = 31

shop = Shop(assets, chars)
board = Board(assets)

boardState = ["default", 0]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TODO: Escape menu for options + information
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if game_state == "shop":
            #do shop stuff
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_status = shop.check_click(mouse_x, mouse_y)
                
                gold, result = shop.handle_click(gold, click_status, patrons, chars)
                
            if result == 0:  
                    if current_level < 2:
                        current_level += 1
                    else:
                       
                        level_counter += 1
                        if level_counter == len(levels):
                            level_counter = 0 
                        
                        available_levels = levels[level_counter][:-1]
                        selected_levels = random.sample(available_levels, 2)
                        selected_levels.append(levels[level_counter][-1])
                        
                        current_level = 0
                        #print(selected_levels)

                    level = selected_levels[current_level]

                    game_state = "battle"
                    board.read_board(level, chars, round)
                    screen.fill((255, 255, 255))
                    round = 1
                    result = 1
            else:
                shop.display(screen, gold)
        else:
            if is_player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    click_status = board.check_click(mouse_x, mouse_y, cell_width, cell_height)

                    if not click_status:
                        boardState = ["default", 0]
                    elif boardState[0] == "charSelected" and click_status[1] == 1 : # Previous click was selecting a friendly unit and current click is a valid movement option
                        board.update_board(click_status, last_clicked)
                        boardState = ["default", 0]
                        char_moves.append(click_status[0])
                        player_actions += 1
                        if player_actions == len(chars):
                            is_player_turn = False
                            player_actions = 0
                    elif boardState[0] == "charSelected" and click_status[1] == 10: # Previous click was selecting a friendly unit and current click is an enemy tile
                        player_actions += 1 # Attacking action
                        char_moves.append(last_clicked) # The character that was last clicked performed an action
                        boardState = ["default", 0]
                        enemies_remaining = board.execute_attack(last_clicked, click_status[0], chars)
                        if player_actions == len(chars):
                            is_player_turn = False
                            player_actions = 0
                    elif 4 <= click_status[1] <= 13 and click_status[0] not in char_moves: # Clicked target is a friendly unit and has not been moved before
                        boardState = ["charSelected", click_status[1]]
                        last_clicked = click_status[0]
                    else:
                        boardState = ["default", 0]
            else:
                #Player turn has finished, can apply end of turn effects here
                board.activate_patrons(chars, patrons)

                board.move_enemies(chars)
                is_player_turn = True
                char_moves = []
            
            board.display(screen, boardState, chars, patrons)

            # Handle end of round actions, switch to shop and get ready to load next level
            if(enemies_remaining == 0):
                enemies_remaining = 1
                game_state = "shop"
                # Add interest gold here
                gold += 3
                char_moves = []
                is_player_turn = True
                player_actions = 0

                shop.refresh_items(chars)
                screen.fill((255, 255, 255))
            
        pygame.display.flip()  