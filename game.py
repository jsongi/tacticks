import pygame
#from enemy import 
from board import Board
from unit import Unit

assets = [
    "assets/grasstile.png", #replace grasstile with this minus the dots, the outline is cleaner visually
    "assets/movementhighlight.png",
    "assets/tempgrasstile.png",
    "assets/tempgrasstile.png",
    "assets/tempgrasstile.png",
    "assets/tempgrasstile.png",
    "assets/tempgrasstile.png",
    "assets/knight.png",
    "assets/mountaintile.png",
    "assets/bug1.png",
    "assets/attackhighlight.png"
]

id = 2 # signify difference between identical unit types
unit1 = Unit(50, 999, 1, 2, id, "knight")
#id = 3
#unit2 = Unit(50, 2, 1, 2, id, "knight")
#id = 4 # signify difference between identical unit types
#unit3 = Unit(50, 2, 1, 2, id, "knight")
#id = 5
#unit4 = Unit(50, 2, 1, 2, id, "knight")
chars = [unit1] # , unit2, unit3, unit4 
char_moves = []
turn_counter = 5
player_actions = 0
is_player_turn = True #CURRENTLY SET TO FALSE FOR TESTING
last_clicked = -1
round = 1

# Initialize Pygame
pygame.init()

# Get the user's screen resolution
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Set the window size to be 80% of the screen width and height
window_width = int(width * 0.8)
window_height = int(height * 0.8)
screen = pygame.display.set_mode((window_width, window_height))

# Width of images can be variable, current tiles are 31x31 pixels
cell_width = 31
cell_height = 31

board = Board(assets)

board.read_board("test", chars, round)

boardState = ["default", 0]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
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
                elif 2 <= click_status[1] <= 7 and click_status[0] not in char_moves: # Clicked target is a friendly unit and has not been moved before
                    boardState = ["charSelected", click_status[1]]
                    last_clicked = click_status[0]
                else:
                    boardState = ["default", 0]
        else:
            board.move_enemies()
            is_player_turn = True
            char_moves = []
        

        screen.fill((255, 255, 255))
        board.display(screen, boardState, chars)
        pygame.display.flip()  