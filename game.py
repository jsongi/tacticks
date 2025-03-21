import pygame
import random
#from enemy import 
from board import Board
from unit import Unit
from shop import Shop

# To anyone reading through this code, I am sorry

assets = [
    "assets/grasstile.png", # 0
    "assets/movementhighlight.png", # 1
    "assets/mountaintile.png", # 2
    "assets/attackhighlight.png", # 3
    "assets/knight.png", # 4
    "assets/thief.png", # 5
    "assets/archer.png", # 6
    "assets/wizard.png", # 7
    "assets/healer.png", # 8
    "assets/executioner.png", # 9
    "assets/marauder.png", # 10
    "assets/catapult.png", # 11
    "assets/archmage.png", # 12
    "assets/mystic.png", # 13
    "assets/tick.png", # enemy type, 14
    "assets/bug2.png", # enemy type, 15
    "assets/mite.png", # enemy type, 16
    "assets/tempgrasstile.png", # enemy type, 17
    "assets/bombardierbeetle.png", # enemy type, 18
    "assets/tempgrasstile.png", # enemy type, 19
    "assets/tempgrasstile.png", # enemy type, 20
    "assets/tempgrasstile.png", # enemy type, 21
    "assets/tempgrasstile.png", # enemy type, 22
    "assets/plaguedoctor.png", # , 23
    "assets/jackofalltrades.png", # , 24
    "assets/clergyman.png", # 25
    "assets/librarian.png", # 26
    "assets/temptreetile.png", # 27
    "assets/conqueror.png", # 28
    "assets/physician.png", # 29
    "assets/merchant.png", # 30
    "assets/armorer.png", # 31
    "assets/weaponsmith.png", # 32
    "assets/enchanter.png", # 33
    "assets/tempgrasstile.png", # temp 34
    "assets/cobbler.png", # 35
    "assets/peddler.png", # 36
    "assets/duelist.png", # 37
    "assets/mercantilist.png", # 38
    "assets/thievesguild.png", # 39
    "assets/opencourts.png", # 40
    "assets/necromancer.png", # 41
    "assets/timekeeper.png" # 42
]
levels = [["aaa", "aab", "aac", "aad", "aae"]
          
          ]
#["aba", "abb", "abc", "abd", "abe"],
#id has to start from 4
unit1 = Unit(40, 40, 3, 0, 1, 2, 4, "Knight", 4, False, "Basic melee unit (Requires 3 to buy Executioner) [40 HP, 3 ATTACK, 1 RANGE, 2 MOVEMENT]", (1, 0))
#unit1 = Unit(70, 70, 15, 0, 1, 2, 4, "Executioner", 8, False, "Rare melee unit, executes enemies when an attack reduces them to below 10% HP and gains Total HP equal to the amount executed", (0, 0))
#unit1 = Unit(40, 40, 0, 25, 4, 2, 4, "Archmage", 8, True, "Rare magic unit, deals 1/10 of damage to all other enemies", (0, 0))
patrons = []
chars = [unit1] # , unit2, unit3, unit4 
char_moves = []
turn_counter = 5
level_counter = -1
current_level = 3
selected_levels = []
player_actions = 0
is_player_turn = True
last_clicked = -1
time_keeper_owned = False
warlock_owned = False
turn_skip = False
round = 1
result = 1
gold = [999999] #set as this for testing, lower to 5(?) later
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
            mouse_x, mouse_y = pygame.mouse.get_pos()
            shop.check_hover(mouse_x, mouse_y, patrons, chars)
            
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_status = shop.check_click(mouse_x, mouse_y, patrons, chars)
                
                result = shop.handle_click(gold, click_status, patrons, chars)
                
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

                    level = selected_levels[current_level]
                    level = "aab"

                    time_keeper_owned = False
                    warlock_owned = False
                    for patron in patrons:
                        if patron.getEffectType() == 8:
                            patron.activateEffect(chars, None, None, gold, None)
                        elif patron._effectIndex == 26:
                            time_keeper_owned = True
                        elif patron._effectIndex == 23:
                            warlock_owned = True

                    game_state = "battle"
                    board.read_board(level, chars, round)
                    
                    screen.fill((255, 255, 255))
                    result = 1
            else:
                shop.display(screen, gold, patrons, chars)
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
                    elif boardState[0] == "charSelected" and click_status[1] == -1: # Previous click was selecting a friendly unit and current click is an enemy tile
                        player_actions += 1 # Attacking action
                        char_moves.append(last_clicked) # The character that was last clicked performed an action
                        boardState = ["default", 0]
                        enemies_remaining = board.execute_attack(last_clicked, click_status[0], chars, patrons, gold)
                        if player_actions == len(chars):
                            is_player_turn = False
                            player_actions = 0
                    elif 4 <= click_status[1] <= 13 and click_status[0] not in char_moves: # Clicked target is a friendly unit and has not been moved before
                        boardState = ["charSelected", click_status[1]]
                        last_clicked = click_status[0]
                    elif click_status[1] == -2: # Clicked target is an enemy not being attacked
                        boardState = ["enemySelected", click_status[0]]
                    elif click_status[1] == -3: # Skip button pressed
                        is_player_turn = False
                        player_actions = 0
                        boardState = ["default", 0]
                    else:
                        boardState = ["default", 0]
            else:
                #Player turn has finished, can apply end of turn effects here
                board.activate_patrons(chars, patrons, gold)

                # Healing after player turn is finished and before enemy attacks
                if not warlock_owned:    
                    for char in chars:
                        if char._type == "Healer":
                            for c in chars:
                                c.addHealth(int(char.magic()))
                        elif char._type == "Mystic":
                            for c in chars:
                                c.addHealth(int(char.magic()))


                if time_keeper_owned:
                    if turn_skip:
                        turn_skip = not turn_skip
                    else:
                        board.move_enemies(chars)
                        turn_skip = not turn_skip    
                else:
                    board.move_enemies(chars)
                        
                is_player_turn = True
                char_moves = []
            
            board.display(screen, boardState, chars, patrons)

            # Handle end of round actions, switch to shop and get ready to load next level
            if(enemies_remaining == 0):
                enemies_remaining = 1
                round += 1
                game_state = "shop"

                if gold[0] >= 25:
                    gold[0] += 5
                else:
                    gold[0] += gold[0] % 5
                
                gold[0] += 3
                char_moves = []
                is_player_turn = True
                player_actions = 0

                # Activate effects for end of round
                for patron in patrons:
                    if patron.getEffectType() == 1:
                        patron.activateEffect(chars, None, None, gold, None)

                # Activate shop patron effects
                shop.activate_patrons(patrons, gold, chars)
                shop.refresh_items(chars)
                screen.fill((255, 255, 255))

            if(len(chars) == 0):
                # TODO: Lose conditional
                running = False
            
        pygame.display.flip()  