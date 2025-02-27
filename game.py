import pygame
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
    "assets/tempgrasstile.png", #thief 5
    "assets/archer.png", # 6
    "assets/wizard.png", # 7
    "assets/healer.png", # 8
    "assets/tempgrasstile.png", #executioner 9
    "assets/tempgrasstile.png", #gambler 10
    "assets/tempgrasstile.png", #ballista / trebuchet 11
    "assets/tempgrasstile.png", #archmage 12
    "assets/tempgrasstile.png", #mystic 13
    "assets/bug1.png", # 14
    "assets/bug2.png", # 15
    "assets/tempgrasstile.png", # enemy type, 16
    "assets/tempgrasstile.png", # enemy type, 17
    "assets/tempgrasstile.png", # enemy type, 18
    "assets/tempgrasstile.png", # enemy type, 19
    "assets/tempgrasstile.png", # enemy type, 20
    "assets/tempgrasstile.png", # enemy type, 21
    "assets/tempgrasstile.png", # enemy type, 22
    "assets/plaguedoctor.png" # , 23
]
#id has to start from 4
id = 4 # signify difference between identical unit types
unit1 = Unit(50, 999, 1, 2, id, "Knight", 4)
#id = 3
#unit2 = Unit(25, 2, 4, 2, id, "archer")
#id = 4 # signify difference between identical unit types
#unit3 = Unit(50, 2, 1, 2, id, "knight")
#id = 5
#unit4 = Unit(50, 2, 1, 2, id, "knight")
upgrades = []
patrons = []
chars = [unit1] # , unit2, unit3, unit4 
char_moves = []
turn_counter = 5
player_actions = 0
is_player_turn = True
last_clicked = -1
round = 1
result = 1
gold = 9999 #set as this for testing, lower to 5(?) later
game_state = "shop"


# Initialize Pygame
pygame.init()

# Get the user's screen resolution
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Set the window size to be 80% of the screen width and height
window_width = int(width * 0.8)
window_height = int(height * 0.8)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tacticks")

# Width of images can be variable, current tiles are 31x31 pixels
cell_width = 31
cell_height = 31

shop = Shop(assets)
board = Board(assets)

boardState = ["default", 0]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "shop":
            #do shop stuff
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_status = shop.check_click(mouse_x, mouse_y, cell_width, cell_height)
                
                gold, result = shop.handle_click(gold, click_status, patrons, chars, upgrades)
                
            if result == 0:   
                    print(chars)
                    game_state = "battle"
                    board.read_board("test", chars, round)
                    screen.fill((255, 255, 255))
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
                    elif boardState[0] == "charSelected" and click_status[1] == 9: # Previous click was selecting a friendly unit and current click is an enemy tile
                        player_actions += 1 # Attacking action
                        char_moves.append(last_clicked) # The character that was last clicked performed an action
                        boardState = ["default", 0]
                        board.execute_attack(last_clicked, click_status[0], chars)
                        if player_actions == len(chars):
                            is_player_turn = False
                            player_actions = 0
                    elif 4 <= click_status[1] <= 13 and click_status[0] not in char_moves: # Clicked target is a friendly unit and has not been moved before
                        boardState = ["charSelected", click_status[1]]
                        last_clicked = click_status[0]
                    else:
                        boardState = ["default", 0]
            else:
                board.move_enemies(chars)
                is_player_turn = True
                char_moves = []
            
            board.display(screen, boardState, chars)
        
            
        pygame.display.flip()  