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
            Upgrade(22, 1, 3, 4, "Flat Attack")
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

        # TODO: Should be weighted differently by rarity
        self.displayed_patrons = random.sample(
            [p for p in self._patrons if p not in self._owned_patrons], 3
        )
        self.displayed_units = random.sample(
            [u for u in self._units], 2
        )
        self.displayed_upgrades = random.sample(
            [u for u in self._upgrades], 2
        )


    def display(self, screen, gold):
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
            text_surface = font.render(f"{item.type()} - ${item.getCost()}", True, (255, 255, 255))
            screen.blit(text_surface, (560, y_offset + 10))
            screen.blit(self._images[item.typeImage()], (680, y_offset - 22))
            y_offset += 70

        # Reroll Button
        pygame.draw.rect(screen, (255, 100, 0), (210, 500, 100, 50))
        reroll_text = font.render(f"Reroll (${self.reroll_cost})", True, (0, 0, 0))
        screen.blit(reroll_text, (220, 515))

        # Continue Button
        pygame.draw.rect(screen, (255, 100, 0), (500, 500, 100, 50))
        continue_text = font.render(f"Continue", True, (0, 0, 0))
        screen.blit(continue_text, (510, 515))

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
                return item
            y_offset += 70

        # Check reroll button
        if 210 <= mouse_x <= 310 and 500 <= mouse_y <= 550:
            return "reroll"

        # Check continue button
        if 500 <= mouse_x <= 600 and 500 <= mouse_y <= 550:
            return "continue"

        return None

    def handle_click(self, gold, clicked_asset, patrons, chars, upgrades):
        """ Handles purchases and rerolling. """

        result = 1
        if clicked_asset == None:
            return gold, result
        if clicked_asset == "reroll" and gold >= self.reroll_cost:
            gold -= self.reroll_cost
            self.refresh_items()
            return gold, result
        elif clicked_asset == "continue":
            result = 0
            return gold, result  # Return updated gold amount
        elif clicked_asset in self._patrons and gold >= clicked_asset.getCost():
            gold -= clicked_asset.getCost()
            # TODO: Mark item as purchased
            patrons.append(clicked_asset)
            # TODO: Remove bought items from display
            return gold, result
        # Calculate new id for unit in board display
        elif clicked_asset in self._units and gold >= clicked_asset.getCost() and len(chars) < 6:
            gold -= clicked_asset.getCost()
            clicked_asset.setId(len(chars) + 4)
            chars.append(clicked_asset)
            print(chars)
            return gold, result
        elif clicked_asset in self._upgrades and gold >= clicked_asset.getCost():
            gold -= clicked_asset.getCost()
            upgrades.append(clicked_asset)
            return gold, result
        else:
            return gold, result