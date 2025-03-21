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

        self._patrons = [
            Patron(25, 1, 1, 4, "Clergyman", 0, "+5 total HP to all units at end of round"),
            Patron(26, 1, 2, 4, "Librarian", 0, "+1 Magic to all units at end of round"),
            Patron(28, 1, 3, 4, "Conqueror", 0, "+1 Attack to all units at end of round"),
            Patron(29, 1, 4, 4, "Physician", 0, "Heals 15 HP to all units at end of round"),
            Patron(30, 1, 5, 4, "Merchant", 0, "+3 Gold at end of round"),
            Patron(31, 6, 6, 4, "Armorer", 0, "+40 Total HP to all units"),
            Patron(32, 6, 7, 4, "Weaponsmith", 0, "+8 Attack to all units"),
            Patron(33, 6, 8, 4, "Enchanter", 0, "+8 Magic to all units"),
            Patron(34, 6, 9, 4, "Generalist", 0, "+6 Attack and +6 Magic to all units"),
            Patron(35, 6, 10, 4, "Cobbler", 0, "+1 movement to all units"),
            Patron(36, 4, 11, 4, "Peddler", 0, "1 free reroll per shop"),
            Patron(27, 7, 12, 4, "Varlet", 0, "+2 gold when selling a unit"),
            Patron(27, 6, 29, 4, "Inhibitors", 0, "-6 Magic to all units, +6 Attack +20 Total HP to all units"),
            Patron(27, 6, 30, 4, "Conclave", 0, "-6 Attack to all units, +8 Magic +10 Total HP to all units"),
            Patron(27, 6, 31, 4, "Trader", 0, "Buying an upgrade gives back 2 gold"),
            Patron(27, 1, 13, 6, "Surgeon", 1, "At end of round, units lose 5 total HP, but heal 1/4 of total HP (Cannot go below 1 Total HP)"),
            Patron(24, 6, 14, 6, "Jack", 1, "Flat boost to all stats (+30 Total HP, +6 Attack, +6 Magic)"),
            Patron(27, 6, 15, 4, "Conquistador", 1, "+1 range to all units"),
            Patron(37, 2, 16, 6, "Duelist", 1, "Buffs units with 1 range"),
            Patron(38, 8, 17, 6, "Mercantilist", 1, "Boosts attack and magic of all units by 1/2 of current gold"),
            Patron(27, 6, 18, 6, "Round Table", 1, "+30 HP, +2 Attack per Knight or Executioner owned"),
            Patron(27, 6, 27, 4, "Runekeepers", 1, "+5 HP +5 Magic per Wizard or Archmage owned"),
            Patron(27, 6, 28, 4, "Bull's Eye", 1, "+10 HP +4 Attack per Archer or Catapult owned"),
            Patron(39, 1, 19, 6, "Thieves Guild", 2, "+2 Gold at end of round per owned Thief, +3 per Marauder"),
            Patron(40, 4, 20, 6, "Open Courts", 2, "Removes owned unit requirements for rare units to appear in shop"),
            Patron(27, 1, 21, 6, "Glutton", 2, "Unit attack is increased by 1/10 of unit total HP"),
            Patron(27, 1, 22, 6, "Ritualist", 2, "Destroy a unit at the end of round, gain stats"),
            Patron(27, 6, 23, 6, "Warlock", 2, "Healers and Mystics no longer heal, but deal 4x damage"),
            Patron(23, 3, 24, 10, "Plague Doctor", 3, "Enemies lose half their current HP each turn"),
            Patron(41, 7, 25, 10, "Necromancer", 3, "Gains stat increases per unit sold"),
            Patron(42, 5, 26, 10, "Time Keeper", 3, "Every other enemy turn is skipped")
        ]

        self._units = [
            Unit(40, 40, 3, 0, 1, 2, 0, "Knight", 4, False, "Basic melee unit (Requires 3 to buy Executioner) [40 HP, 3 ATTACK, 1 RANGE, 2 MOVEMENT]", (0, 0)),
            Unit(30, 30, 2, 0, 1, 4, 0, "Thief", 4, False, "Basic melee unit, generates 1 gold at end of round (Requires 3 to buy Marauder) [30 HP, 2 ATTACK, 1 RANGE, 4 MOVEMENT]", (0, 0)),
            Unit(25, 25, 4, 0, 3, 3, 0, "Archer", 4, False, "Basic ranged unit (Requires 3 to purchase Catapult) [25 HP, 4 ATTACK, 3 RANGE, 3 MOVEMENT]", (0, 0)),
            Unit(20, 20, 0, 6, 3, 2, 0, "Wizard", 4, True, "Basic magic unit (Requires 3 to purchase Archmage) [20 HP, 6 MAGIC, 3 RANGE, 2 MOVEMENT]", (0, 0)),
            Unit(20, 20, 0, 2, 3, 3, 0, "Healer", 3, True, "Basic magic unit, heals allies (Requires 3 to purchase Mystic) [20 HP, 3 MAGIC, 3 RANGE, 3 MOVEMENT]", (0, 0)),
            Unit(70, 70, 15, 0, 1, 2, 0, "Executioner", 8, False, "Rare melee unit, executes enemies when an attack reduces them to below 10% HP", (0, 0)),
            Unit(50, 50, 10, 0, 1, 4, 0, "Marauder", 8, False, "Rare melee unit", (0, 0)),
            Unit(40, 40, 40, 0, 10, 1, 0, "Catapult", 8, False, "Rare ranged unit, nearly global range [40 HP, 40 ATTACK, 10 RANGE, 1 MOVEMENT]", (0, 0)),
            Unit(40, 40, 0, 25, 4, 2, 0, "Archmage", 8, True, "Rare magic unit, deals 1/10 of damage to all other enemies", (0, 0)),
            Unit(30, 30, 0, 20, 4, 2, 0, "Mystic", 8, True, "Rare magic unit, heals allies", (0, 0))
        ]
        # TODO: The images slots for this are temporary and need to be updated
        self._upgrades = [
            Upgrade(22, 1, 5, "Flat HP"),
            Upgrade(22, 2, 5, "Flat Magic"),
            Upgrade(22, 3, 5, "Flat Attack"),
            Upgrade(22, 4, 5, "Healing")
        ]

        self.displayed_patrons = []
        self.displayed_units = []
        self.displayed_upgrades = []
        self.unit_ids = [4, 5, 6, 7, 8, 9]
        self.unit_locs = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        self.hovered_item = None
        self.selected_item = None
        self.last_selected_unit = None
        self.free_reroll = False
        self.ignore_unit_reqs = False
        self.move_units = False
        self.sell_action = False
        self._heal = 0

        for image in assets:
            self._images.append(pygame.image.load(image)) 
         
        self.refresh_items(chars)  # Selects items to be displayed

    def activate_patrons(self, patrons, gold, chars):
        #this is jank if I want to add more later
        self.ignore_unit_reqs = False
        for patron in patrons:
            if(patron._effectIndex == 11):
                self.free_reroll = True
                self.reroll_cost = 0
            elif(patron._effectIndex == 20):
                self.ignore_unit_reqs = True
        return

    def refresh_items(self, chars):
        self.last_selected_unit = None
        self.move_units = False
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


        # Define unit unlock conditions
        unit_requirements = {
            "Executioner": ("Knight", 3),
            "Marauder": ("Thief", 3),
            "Catapult": ("Archer", 3),
            "Archmage": ("Wizard", 3),
            "Mystic": ("Healer", 3),
        }

        if self.ignore_unit_reqs:
            unit_requirements = {unit: (req_class, 0) for unit, (req_class, _) in unit_requirements.items()}

        # Count how many of each unit type are owned
        owned_unit_counts = {unit.type(): 0 for unit in self._units}  # Initialize all counts to 0
        for unit in chars:
            owned_unit_counts[unit.type()] += 1
            
        # Separate restricted and common units
        common_units = []
        restricted_units = []

        for unit in self._units:
            if unit.type() in unit_requirements:
                required_unit, required_count = unit_requirements[unit.type()]
                if owned_unit_counts.get(required_unit, 0) >= required_count:
                    restricted_units.append(unit)  # Add if requirement met
            else:
                common_units.append(unit)

        num_to_select = 2

        # Decide how many restricted units to include
        if restricted_units and random.random() < 0.20:  # 20% chance to select from restricted pool
            # Pick 1 from restricted and 1 from common
            selected_units = random.sample(restricted_units, k=1) + random.sample(common_units, k=1)
        else:
            # Pick only from common units
            selected_units = random.sample(common_units, k=num_to_select)

        # Randomly sample from the adjusted pool
        self.displayed_units = selected_units

        self.displayed_upgrades = random.sample(
            [u for u in self._upgrades], 2
        )

    def check_hover(self, mouse_x, mouse_y, patrons, chars):
        """ Detects which item is being hovered over and stores it. """
        self.hovered_item = None  # Reset hover

        # Check patrons
        y_offset = 150
        for item in self.displayed_patrons:
            if 300 <= mouse_x <= 500 and y_offset <= mouse_y <= y_offset + 50:
                self.hovered_item = (item, True)
                return
            y_offset += 70

        # Check units
        y_offset = 200
        for item in self.displayed_units:
            if 550 <= mouse_x <= 750 and y_offset <= mouse_y <= y_offset + 50:
                self.hovered_item = (item, False)
                return
            y_offset += 70

        # Check owned patrons
        patron_width, patron_height = 32, 32 # Each patron is 32x32
        start_x, start_y = 830, 530  # Position for owned patrons
        spacing_x = 8 

        for index, patron in enumerate(patrons):
            patron_x = start_x + index * (patron_width + spacing_x)
            patron_y = start_y
            patron_rect = pygame.Rect(patron_x, patron_y, patron_width, patron_height)

            if patron_rect.collidepoint(mouse_x, mouse_y):
                self.hovered_item = (patron, True)  # True for owned patron
                return

        # Check owned units (chars)
        # Each unit is 14x14 pixel

        for index, unit in enumerate(chars):  # Check each owned character
            row, col = unit.location()

            unit_x = 885 + col * (42)
            unit_y = 135 + row * (42)

            unit_rect = pygame.Rect(unit_x, unit_y, 20, 20)
            if unit_rect.collidepoint(mouse_x, mouse_y):
                self.hovered_item = (unit, False)  # False for owned unit
                return

    def display(self, screen, gold, patrons, chars):
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

        # TODO: Check this behavior if the type is being checked correctly
        if self.hovered_item is not None and self.hovered_item[0] is not None:
            if self.hovered_item[0] is Unit:
                if self.hovered_item[0].id != 0:
                    pygame.draw.rect(screen, (200, 200, 200), (50, 800, 600, 80))  # Background for text
                    desc_surface = font.render(self.hovered_item[0].getDescription(), True, (0, 0, 0))
                    screen.blit(desc_surface, (60, 820))
                else: # Is an owned unit, display stats for owned unit
                    pygame.draw.rect(screen, (200, 200, 200), (50, 800, 600, 80))  # Background for text
                    desc_surface = font.render(self.hovered_item[0].getDescription(), True, (0, 0, 0))
                    screen.blit(desc_surface, (60, 820))
            else:
                if self.hovered_item[0] in patrons: # Is an owned patron, display flavor stats for patron
                    pygame.draw.rect(screen, (200, 200, 200), (50, 800, 1000, 80))  # Background for text
                    desc_surface = font.render(self.hovered_item[0].getDescription(), True, (0, 0, 0))
                    screen.blit(desc_surface, (60, 820))
                else:
                    pygame.draw.rect(screen, (200, 200, 200), (50, 800, 1000, 80))  # Background for text
                    desc_surface = font.render(self.hovered_item[0].getDescription(), True, (0, 0, 0))
                    screen.blit(desc_surface, (60, 820))

        # Draw tiles under unit locations
        for index in range(6):
            x = 850 + (index % 3) * (42)
            y = 100 + (index // 3) * (42)
            screen.blit(self._images[0], (x, y))

        # Display owned units
        for index, char in enumerate(chars):
            row, col = char.location()

            x = 850 + col * (42)
            y = 100 + row * (42)

            if self.selected_item == char:
                screen.blit(self._images[1], (x, y))
                
                pygame.draw.rect(screen, (255, 100, 0), (880, 250, 100, 50))
                reroll_text = font.render(f"Sell (${int(self.selected_item.getCost() / 2)})", True, (0, 0, 0))
                screen.blit(reroll_text, (890, 265))

            screen.blit(self._images[char.typeImage()], (x, y))
        # Display owned patrons
        x_offset = 800
        pygame.draw.rect(screen, (200, 200, 200), (810, 520, 230, 50))
        for i, patron in enumerate(patrons):     
            patron_width, patron_height = 32, 32 # Each patron is 32x32
            start_x, start_y = 830, 530  # Position for owned patrons
            spacing_x = 8 
            patron_x = start_x + i * (patron_width + spacing_x)
            patron_y = start_y
            if self.selected_item == patron:
                pygame.draw.rect(screen, (255, 0, 0), (patron_x - 6, patron_y - 5, 40, 40))
                
                # Sell button for patron
                pygame.draw.rect(screen, (255, 100, 0), (870, 580, 100, 50))
                reroll_text = font.render(f"Sell (${int(self.selected_item.getCost() / 2)})", True, (0, 0, 0))
                screen.blit(reroll_text, (880, 595))    

            screen.blit(self._images[patron.getImage()], (x_offset, 500))
            x_offset += 40

        # Move units 
        if self.move_units:
            pygame.draw.rect(screen, (0, 255, 0), (900, 50, 100, 50))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (900, 50, 100, 50))
        reroll_text = font.render(f"Move units", True, (0, 0, 0))
        screen.blit(reroll_text, (910, 65))

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
        gold_text = font.render(f"Gold: {gold[0]}", True, (0, 0, 0))
        screen.blit(gold_text, (360, 615))

        pygame.display.flip()

    def check_click(self, mouse_x, mouse_y, patrons, chars):
        # Check patron sell button if it is valid
        if self.selected_item in patrons:
            if 870 <= mouse_x <= 970 and 580 <= mouse_y <= 630:
                self.sell_action = True
                return self.selected_item
        
        if self.selected_item in chars:
            if 880 <= mouse_x <= 980 and 250 <= mouse_y <= 300:
                return "sellchar"
        
        self.selected_item = None

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

        # Check owned patrons
        patron_width, patron_height = 32, 32 # Each patron is 32x32
        start_x, start_y = 830, 530  # Position for owned patrons
        spacing_x = 8 

        for index, patron in enumerate(patrons):
            patron_x = start_x + index * (patron_width + spacing_x)
            patron_y = start_y

            if patron_x <= mouse_x <= patron_x + 32 and patron_y <= mouse_y <= patron_y + 32:
                self.selected_item = patron
                return "selectedpatron"
        
        # Check owned units
        for index, unit in enumerate(chars):
            row, col = unit.location()

            unit_x = 885 + col * (42)
            unit_y = 135 + row * (42)

            if unit_x <= mouse_x <= unit_x + 20 and unit_y <= mouse_y <= unit_y + 20:
                self.selected_item = unit
                if self.last_selected_unit and self.move_units:
                    return "movedunit"
                else:
                    self.last_selected_unit = unit
                    return "selectedunit"
                
        if self.selected_item is None and self.move_units and self.last_selected_unit is not None:
            empty_row = (mouse_y - 135) // 42
            empty_col = (mouse_x - 885) // 42

            # Ensure it's within grid bounds (0-1 for rows, 0-2 for columns)
            if 0 <= empty_row < 2 and 0 <= empty_col < 3:
                # Check if the space is occupied
                if not any(unit.location() == (empty_row, empty_col) for unit in chars):
                    self.last_selected_unit.setLocation((empty_row, empty_col))  # Move to empty space
                    self.last_selected_unit = None
                    return None

        # Check reroll button
        if 210 <= mouse_x <= 310 and 500 <= mouse_y <= 550:
            return "reroll"

        # Check continue button
        if 500 <= mouse_x <= 600 and 500 <= mouse_y <= 550:
            self.reroll_cost = 5
            return "continue"

        # Check move unit button
        if 900 <= mouse_x <= 1000 and 50 <= mouse_y <= 100:
            self.last_selected_unit = None
            self.move_units = not self.move_units
            return None

        self.last_selected_unit = None

        return None
        

    def handle_click(self, gold, clicked_asset, patrons, chars):
        """ Handles purchases and rerolling. """

        result = 1
        if clicked_asset == None:
            return result
        
        if clicked_asset == "reroll" and gold[0] >= self.reroll_cost:
            if self.free_reroll:
                self.free_reroll = False
                self.reroll_cost = 5
            else:
                gold[0] -= self.reroll_cost
                self.reroll_cost += 2
            self.refresh_items(chars)
            return result
        
        elif clicked_asset == "continue":
            
            # this is ugly and should be reworked
            for char in chars:
                char.addHealth(self._heal)

            result = 0
            return result  # Return updated gold amount
        
        elif clicked_asset in patrons and self.sell_action:
            clicked_asset.setPurchased(False)
            self.selected_item.handleSold(chars, None, None, gold, None)
            gold[0] += int(self.selected_item.getCost() / 2)
            patrons.remove(self.selected_item)
            self.sell_action = False
            return result
        
        elif clicked_asset == "sellchar":
            if len(chars) > 1:
                gold[0] += int(self.selected_item.getCost() / 2)
                chars.remove(self.selected_item)
            for patron in patrons:
                if patron.getEffectType() == 6 or patron.getEffectType() == 7:
                    patron.onUnitSold(self.selected_item, chars, None, None, gold, None)
                    continue
            self.last_selected_unit = None
            return result
        
        elif clicked_asset in self._patrons and gold[0] >= clicked_asset.getCost() and len(patrons) < 5:
            gold[0] -= clicked_asset.getCost()
            clicked_asset.setPurchased(True)
            patrons.append(clicked_asset)
            if clicked_asset.getEffectType() == 4 or clicked_asset.getEffectType() == 6:
                clicked_asset.activateEffect(chars, None, None, gold, None)
                self.activate_patrons(patrons, gold, chars)
            self.displayed_patrons[self.displayed_patrons.index(clicked_asset)] = None
            return result
        
        elif clicked_asset in self._units and gold[0] >= clicked_asset.getCost() and len(chars) < 6:
            gold[0] -= clicked_asset.getCost()

            existing_ids = {char.id() for char in chars}
            existing_locations = {char.location() for char in chars}
            new_id = 0
            new_loc = (-1, -1)

            for num in self.unit_ids:
                if num not in existing_ids:
                    new_id = num
                    break

            for loc in self.unit_locs:
                if loc not in existing_locations:
                    new_loc = loc
                    break

            clicked_asset.setId(new_id)
            clicked_asset.setLocation(new_loc)
            
            for patron in patrons:
                patron.onUnitPurchase(clicked_asset, chars, None, None, gold, None)

            for upgrade in self._upgrades:
                upgrade.onUnitPurchase(clicked_asset)

            chars.append(copy.copy(clicked_asset))
            self.displayed_units[self.displayed_units.index(clicked_asset)] = None
            return result
        
        elif clicked_asset in self._upgrades and gold[0] >= clicked_asset.getCost():
            gold[0] -= clicked_asset.getCost()
            clicked_asset.activateEffect(chars)
            self.displayed_upgrades[self.displayed_upgrades.index(clicked_asset)] = None
            
            for patron in patrons:
                if patron.getEffectIndex() == 31:
                    gold[0] += 2

            # this was added way later and should be reworked
            if clicked_asset.getName() == "Healing":
                self._heal = clicked_asset._healing

            return result
        
        elif clicked_asset == "movedunit":
            target_row, target_col = self.selected_item.location()
            self.selected_item.setLocation(self.last_selected_unit.location())
            self.last_selected_unit.setLocation((target_row, target_col))

            self.selected_item = None
            self.last_selected_unit = None
            return result
        
        else:
            return result
        
