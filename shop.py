import pygame
import random
import copy

from unit import Unit
from patron import Patron
from upgrade import Upgrade

pygame.font.init()
font = pygame.font.Font(None, 24)

cell_width = 32
cell_height = 32

class Shop:
    def __init__(self, assets, chars):
        self._images = []  # Dictionary containing item categories
        self.reroll_cost = 5  # Cost for rerolling the shop
        self.unit_id = 0
        
        self._owned_patrons = [

        ]
        
        self._owned_units = [
            Unit(40, 40, 3, 0, 1, 2, 4, "Knight", 4, False),
        ]

        self._patrons = [
            Patron(25, 1, 1, 4, "Clergyman", 0),
            Patron(26, 1, 2, 4, "Librarian", 0),
            Patron(27, 1, 3, 4, "Conqueror", 0),
            Patron(27, 1, 4, 4, "Physician", 0),
            Patron(27, 4, 5, 4, "Merchant", 0),
            Patron(27, 6, 6, 4, "Armorer", 0),
            Patron(27, 6, 7, 4, "Weaponsmith", 0),
            Patron(27, 6, 4, 4, "Enchanter", 0),
            Patron(27, 6, 8, 4, "Generalist", 0),
            Patron(27, 6, 9, 4, "Cobbler", 0),
            Patron(27, 4, 10, 4, "Peddler", 0),
            Patron(24, 4, 14, 6, "Jack", 1),
            Patron(27, 2, 16, 6, "Duelist", 1),
            Patron(23, 3, 24, 8, "Plague Doctor", 3)
        ]

        self._units = [
            Unit(40, 40, 3, 0, 1, 2, 0, "Knight", 4, False),
            Unit(30, 30, 2, 0, 1, 4, 0, "Thief", 4, False),
            Unit(25, 25, 4, 0, 3, 3, 0, "Archer", 4, False),
            Unit(25, 25, 0, 6, 3, 2, 0, "Wizard", 4, True),
            Unit(20, 20, 0, 3, 3, 3, 0, "Healer", 3, True),
            Unit(70, 70, 15, 0, 1, 2, 0, "Executioner", 8, False),
            Unit(50, 50, 10, 0, 1, 4, 0, "Marauder", 8, False),
            Unit(40, 40, 40, 0, 10, 1, 0, "Catapult", 8, False),
            Unit(40, 40, 0, 25, 4, 2, 0, "Archmage", 8, True),
            Unit(30, 30, 0, 20, 4, 2, 0, "Mystic", 8, True)
        ]
        # TODO: The images slots for this are temporary and need to be updated
        self._upgrades = [
            Upgrade(22, 1, 1, 4, "Flat HP"),
            Upgrade(22, 1, 2, 4, "Flat Magic"),
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
         
        self.refresh_items(chars)  # Selects items to be displayed

    def refresh_items(self, chars):
        rarity_weights = {0: 75, 1: 20, 2: 4, 3: 1}

        # Filter available patrons
        available_patrons = [p for p in self._patrons if p not in self._owned_patrons and not p.getPurchased()]

        num_to_select = 3

        selected_patrons = []
        while len(selected_patrons) < num_to_select:
            patron = random.choices(
                available_patrons,
                weights=[rarity_weights.get(p.getRarity(), 0) for p in available_patrons],
                k=1
            )[0]  # Pick one patron at a time

            if patron not in selected_patrons:  # Ensure no duplicates
                selected_patrons.append(patron)

        self.displayed_patrons = selected_patrons

        # Displayed units take owned units into account when generating what can show up
        self.displayed_units = random.sample(
            [u for u in self._units], 2
        )
        # Potentially make this not rerollable
        self.displayed_upgrades = random.sample(
            [u for u in self._upgrades], 2
        )


    def display(self, screen, gold):
        """ Draw shop items and reroll button. """
        screen.fill((255, 255, 255))  # Clear screen

        y_offset = 150  # Start Y position for patrons
        for i, item in enumerate(self.displayed_patrons):
            if item:
                pygame.draw.rect(screen, (0, 200, 0), (300, y_offset, 200, 50))
                text_surface = font.render(f"{item.getName()} - ${item.getCost()}", True, (0, 0, 0))
                screen.blit(text_surface, (310, y_offset + 10))
                screen.blit(self._images[item.getImage()], (430, y_offset - 22))
            y_offset += 70

        # Flat upgrades (Left Side)
        y_offset = 200
        for i, item in enumerate(self.displayed_upgrades):
            if item:
                pygame.draw.rect(screen, (200, 0, 200), (50, y_offset, 200, 50))
                text_surface = font.render(f"{item.getName()} - ${item.getCost()}", True, (0, 0, 0))
                screen.blit(text_surface, (60, y_offset + 10))
                screen.blit(self._images[item.getImage()], (180, y_offset - 22))
            y_offset += 70

        # Units (Right Side)
        y_offset = 200
        for i, item in enumerate(self.displayed_units):
            if item:
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

        # Gold Value
        pygame.draw.rect(screen, (255, 215, 0), (350, 600, 100, 50))
        gold_text = font.render(f"Gold: {gold}", True, (0, 0, 0))
        screen.blit(gold_text, (360, 615))

        pygame.display.flip()

    def check_click(self, mouse_x, mouse_y):
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
            self.reroll_cost = 5
            return "continue"

        return None
        

    def handle_click(self, gold, clicked_asset, patrons, chars):
        """ Handles purchases and rerolling. """

        result = 1
        if clicked_asset == None:
            return gold, result
        if clicked_asset == "reroll" and gold >= self.reroll_cost:
            gold -= self.reroll_cost
            self.reroll_cost += 2
            self.refresh_items(chars)
            return gold, result
        elif clicked_asset == "continue":
            result = 0
            return gold, result  # Return updated gold amount
        elif clicked_asset in self._patrons and gold >= clicked_asset.getCost() and len(patrons) < 5:
            gold -= clicked_asset.getCost()
            clicked_asset.setPurchased(True)
            patrons.append(clicked_asset)
            if clicked_asset.getEffectType() == 4 or clicked_asset.getEffectType() == 6:
                clicked_asset.activateEffect(chars, None, None, gold)
            self.displayed_patrons[self.displayed_patrons.index(clicked_asset)] = None
            return gold, result
        elif clicked_asset in self._units and gold >= clicked_asset.getCost() and len(chars) < 6:
            gold -= clicked_asset.getCost()
            # TODO: Calculate new id for unit in board display when characters are sold and new ones are bought
            clicked_asset.setId(len(chars) + 4)
            chars.append(copy.copy(clicked_asset))
            for patron in patrons:
                if patron.getEffectType() == 6:
                    patron.activateEffects(chars, None, None, gold)
            self.displayed_units[self.displayed_units.index(clicked_asset)] = None
            return gold, result
        elif clicked_asset in self._upgrades and gold >= clicked_asset.getCost():
            gold -= clicked_asset.getCost()
            clicked_asset.activateEffect(chars)
            self.displayed_upgrades[self.displayed_upgrades.index(clicked_asset)] = None
            return gold, result
        else:
            return gold, result
        
