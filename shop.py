import pygame
import random

from unit import Unit
from patron import Patron
from upgrade import Upgrade

pygame.font.init()
font = pygame.font.Font(None, 24)

cell_width = 32
cell_height = 32

class Shop:
    def __init__(self, assets):
        self._images = []  # Dictionary containing item categories
        self.reroll_cost = 5  # Cost for rerolling the shop
        self.unit_id = 0
        
        self._owned_patrons = [

        ]
        
        self._owned_units = [

        ]

        self._patrons = [
            Patron(23, 3, 20, 4, "Plague Doctor"),
            Patron(23, 3, 20, 4, "Placeholder"),
            Patron(23, 3, 20, 4, "Placeholder"),
        ]

        self._units = [
            Unit(40, 3, 1, 2, 0, "Knight", 4),
            Unit(30, 2, 1, 4, 0, "Thief", 4),
            Unit(25, 4, 3, 3, 0, "Archer", 4),
            Unit(20, 6, 3, 2, 0, "Wizard", 4),
            Unit(20, 2, 3, 3, 0, "Healer", 3),
            Unit(70, 15, 1, 2, 0, "Executioner", 8),
            Unit(50, 10, 1, 4, 0, "Gambler", 8),
            Unit(40, 40, 20, 1, 0, "Ballista", 8),
            Unit(40, 25, 4, 2, 0, "Archmage", 8),
            Unit(30, 20, 4, 2, 0, "Mystic", 8)
        ]
        # TODO: The images slots for this are temporary and need to be updated
        self._upgrades = [
            Upgrade(22, 1, 1, 4, "Flat HP"),
            Upgrade(22, 1, 2, 4, "Scaling HP"),
            Upgrade(22, 1, 3, 4, "Scaling HP")
        ]

        # Mark all items as not purchased initially
        #for category in self._assets.values():
        #    for item in category:
        #        item["bought"] = False

        self.displayed_patrons = []
        self.displayed_units = []
        self.displayed_upgrades = []

        for image in assets:
            self._images.append(pygame.image.load(image)) 
         
        self.refresh_items()  # Selects items to be displayed

    def refresh_items(self):
        """ Selects a random subset while filtering out bought items. """
        self.displayed_patrons = random.sample(
            [p for p in self._patrons if p not in self._owned_patrons], 3
        )
        self.displayed_units = random.sample(
            [u for u in self._units], 2
        )
        self.displayed_upgrades = random.sample(
            [u for u in self._upgrades], 2
        )


    def display(self, screen, shop):
        """ Draw shop items and reroll button. """
        screen.fill((255, 255, 255))  # Clear screen

        y_offset = 150  # Start Y position for patrons
        for i, item in enumerate(self.displayed_patrons):
            pygame.draw.rect(screen, (0, 200, 0), (300, y_offset, 200, 50))
            text_surface = font.render(f"{item.getName()} - ${item.getCost()}", True, (0, 0, 0))
            screen.blit(text_surface, (310, y_offset + 10))
            screen.blit(self._images[item.getImage()], (430, y_offset - 22))
            y_offset += 70

        # Flat upgrades (Left Side)
        y_offset = 200
        for i, item in enumerate(self.displayed_upgrades):
            pygame.draw.rect(screen, (200, 0, 200), (50, y_offset, 200, 50))
            text_surface = font.render(f"{item.getName()} - ${item.getCost()}", True, (0, 0, 0))
            screen.blit(text_surface, (60, y_offset + 10))
            screen.blit(self._images[item.getImage()], (180, y_offset - 22))
            y_offset += 70

        # Units (Right Side)
        y_offset = 200
        for i, item in enumerate(self.displayed_units):
            pygame.draw.rect(screen, (0, 0, 200), (550, y_offset, 200, 50))
            text_surface = font.render(f"{item.type()} - ${item.cost()}", True, (255, 255, 255))
            screen.blit(text_surface, (560, y_offset + 10))
            screen.blit(self._images[item.typeImage()], (680, y_offset - 22))
            y_offset += 70

        # Reroll Button
        pygame.draw.rect(screen, (255, 100, 0), (300, 500, 200, 50))
        reroll_text = font.render(f"Reroll (${self.reroll_cost})", True, (0, 0, 0))
        screen.blit(reroll_text, (320, 510))

        pygame.display.flip()

    def check_click(self, mouse_x, mouse_y, cell_width, cell_height):
        """ Determines if an item or the reroll button was clicked. """
        # Check patrons
        y_offset = 150
        for item in self.displayed_patrons:
            if 300 <= mouse_x <= 500 and y_offset <= mouse_y <= y_offset + 50:
                return item
            y_offset += 70

        # Check flat upgrades
        y_offset = 200
        for item in self.displayed_upgrades:
            if 50 <= mouse_x <= 250 and y_offset <= mouse_y <= y_offset + 50:
                return item
            y_offset += 70

        # Check units
        y_offset = 200
        for item in self.displayed_units:
            if 550 <= mouse_x <= 750 and y_offset <= mouse_y <= y_offset + 50:
                print("item")
                return item
            y_offset += 70

        # Check reroll button
        if 300 <= mouse_x <= 500 and 500 <= mouse_y <= 550:
            print("reroll")
            return "reroll"

        return None

    def handle_click(self, gold, clicked_asset):
        """ Handles purchases and rerolling. """
        if clicked_asset == "reroll" and gold >= self.reroll_cost:
            gold -= self.reroll_cost
            self.refresh_items()
        elif isinstance(clicked_asset, dict) and gold >= clicked_asset["cost"]:
            gold -= clicked_asset["cost"]
            clicked_asset["bought"] = True  # Mark item as purchased
            self.refresh_items()  # Remove bought items from display

        return gold  # Return updated gold amount
