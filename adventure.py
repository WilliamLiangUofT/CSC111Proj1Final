"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Key, Location, Item, Player, Puzzle
from proj1_event_logger import Event, EventList


class AdventureGame:
    """A text adventure game class storing all location, item, and map data.

    Instance Attributes:
        - _locations: A dictionary mapping location IDs (int) to Location objects representing
        every location in the game.
        - _items: A dictionary mapping item names (str) to Item objects representing all items available in the game.
        - current_location_id: An integer representing the ID of the current location.
        - ongoing: A boolean flag indicating whether the game is still active.
        - _keys: A dictionary mapping key names (str) to all Key objects.
        - _puzzles: A dictionary mapping puzzle IDs (int) to all Puzzle objects.

    Representation Invariants:
        - current_location_id is always a key in _locations
    """

    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_location_id: int
    ongoing: bool
    _keys: dict[str, Key]
    _puzzles: dict[int, Puzzle]

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game.

        Parameters:
            game_data_file: The JSON file containing the game data.
            initial_location_id: The starting location ID.
        """
        self._locations, self._items = self._load_game_data1(game_data_file)
        self._keys, self._puzzles = self._load_game_data2(game_data_file)
        self.current_location_id = initial_location_id
        self.ongoing = True

    @staticmethod
    def _load_game_data1(filename: str) -> tuple[dict[int, Location], dict[str, Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a dictionary of items mapping each game item name to an Item object."""
        with open(filename, 'r') as f:
            data = json.load(f)

        locations = {}
        for loc_data in data['locations']:
            location_obj = Location(
                loc_data['id'],
                loc_data['name'],
                loc_data['brief_description'],
                loc_data['long_description'],
                loc_data['available_commands'],
                loc_data['items']
            )
            locations[loc_data['id']] = location_obj

        items = {}
        for item_data in data['items']:
            item_obj = Item(
                item_data['name'],
                item_data['description'],
                item_data['start_position'],
                item_data['weight'],
                item_data['the_key'],
                item_data['puzzle_to_obtain']
            )
            items[item_data['name']] = item_obj

        return locations, items

    @staticmethod
    def _load_game_data2(filename: str) -> tuple[dict[str, Key], dict[int, Puzzle]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of keys mapping each game key name to a Key object,
        and (2) a dictionary of puzzles mapping each game puzzle ID to a Puzzle object."""
        with open(filename, 'r') as f:
            data = json.load(f)

        keys = {}
        for key_data in data['keys']:
            key_obj = Key(
                key_data['key_name'],
                key_data['description'],
                key_data['start_position'],
                key_data['weight'],
                key_data['puzzle_to_obtain'],
                key_data['the_item']
            )
            keys[key_data['key_name']] = key_obj

        puzzles = {}
        for puzzle_data in data['puzzles']:
            puzzle_obj = Puzzle(
                puzzle_data['id_puzzle'],
                puzzle_data['description'],
                puzzle_data['answer']
            )
            puzzles[puzzle_data['id_puzzle']] = puzzle_obj

        return keys, puzzles

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item:
        """
        Return the Item object with the given name.
        """
        return self._items[item_name]

    def get_key(self, key_name: str) -> Key:
        """
        Return the Key object with the given name.
        """
        return self._keys[key_name]

    def get_the_items(self) -> list[str]:
        """
        Return a list of all item names in the game.
        """
        the_list = []
        for the_item in self._items:
            the_list.append(the_item)
        return the_list

    def check_weight(self, user: Player, item_str: str) -> bool:
        """
        Check if adding the specified item keeps the player's total inventory weight within the allowed limit.
        """
        added_weight = 0
        if item_str in self.get_the_items():
            added_weight = self.get_item(item_str).weight

        if self.sum_inv_weight(user) + added_weight <= 11:
            return True
        return False

    def check_key(self, user: Player, item_str: str) -> bool:
        """
        Check if the player has the required key (if any) for the specified item.
        """
        need_key = None
        if item_str in self.get_the_items():
            need_key = self.get_item(item_str).the_key

        if need_key is None or (need_key is not None and need_key in user.get_inventory()):
            return True
        return False

    def check_puzzle(self, item_str: str, logger: EventList, loc: Location) -> bool:
        """
        Check if the player can solve the puzzle required to obtain the specified item or key.
        """
        if item_str in self.get_the_items():
            need_puzzle = self.get_item(item_str).puzzle_to_obtain
        else:
            need_puzzle = self.get_key(item_str).puzzle_to_obtain

        if need_puzzle is None or (need_puzzle is not None and self.puzzle_choose(need_puzzle, logger, loc)):
            return True
        return False

    def sum_inv_weight(self, user: Player) -> float:
        """
        Return the total weight of items in the player's inventory.
        """
        total = 0.0
        for item_str in user.get_inventory():
            if item_str in self.get_the_items():
                total += self.get_item(item_str).weight
        return total

    def puzzle_choose(self, puzzle_id: int, logger: EventList, loc: Location) -> bool:
        """
        Select and run the appropriate puzzle based on the puzzle ID.
        """
        if puzzle_id == 1:
            return self.logic_puzzle(puzzle_id)
        elif puzzle_id == 2:
            return self.order_puzzle(puzzle_id, logger)
        else:
            return self.weight_puzzle(puzzle_id, loc)

    def logic_puzzle(self, puzzle_id: int) -> bool:
        """
        Run a logic puzzle by repeatedly prompting the user until the correct answer is given or they quit.
        """
        the_answer = input(self._puzzles[puzzle_id].description).lower()
        while the_answer != self._puzzles[puzzle_id].answer:
            the_answer = input("Wrong Answer! Try again. Enter 'q' if you would want to quit puzzle: ")
            if the_answer.lower() == 'q':
                return False
        return True

    def order_puzzle(self, puzzle_id: int, logger: EventList) -> bool:
        """
        Run an order puzzle using the event log to verify the correct sequence.
        """
        if (logger.last.prev.id_num == self._puzzles[puzzle_id].answer[1]
                and logger.last.prev.prev.id_num == self._puzzles[puzzle_id].answer[0]):
            return True
        print(self._puzzles[puzzle_id].description + '\n')
        return False

    def weight_puzzle(self, puzzle_id: int, loc: Location) -> bool:
        """
        Run a weight puzzle by checking if the total weight of items in the location equals the expected answer.
        """
        total = 0.0
        for item_str in loc.items:
            if item_str in self.get_the_items():
                total += self.get_item(item_str).weight
        if total == self._puzzles[puzzle_id].answer:
            return True
        print(self._puzzles[puzzle_id].description + '\n')

        return False

    def look(self, loc: Location) -> None:
        """
        Print a description of the given location. Long description if player hasn't been before '
        and brief is the player has
        """
        print("Location " + str(loc.id_num))
        if loc.visited:
            print("You are now at " + loc.name
                  + "! Since you have been here before, here's a BRIEF description of this place.\n"
                  + loc.brief_description + "\n")
        else:
            print("You are now at " + loc.name
                  + "! Since you have NEVER been here before, here's a LONG description of this fabulous place!\n"
                  + loc.long_description + "\n")
        if len(location.items) != 0:
            print("This location also has item(s):")
            location.display_items()
        else:
            print("This location has NO items.")
            print()


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    player = Player([], 0.0, 0)
    game_log = EventList()
    game = AdventureGame('game_data.json', 1)
    menu = ["look", "inventory", "score", "undo", "log", "weights", "quit"]
    picked_items = []
    choice = None
    menu_off = True
    location_change = True
    game_finished = False
    bonus_awarded = False
    item_choice = None
    drop_choice = None
    steps_remaining = 30

    while game.ongoing and set(game.get_location(1).items) != set(game.get_the_items()):
        location = game.get_location()

        if menu_off:
            game.look(location)
        if menu_off and location_change:
            game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description), choice)

        menu_off = True
        location_change = True

        print("Allowed Moving Steps Remaining: " + str(steps_remaining) + "\n")
        print("What to do? Choose from: look, inventory, score, weights, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        print("- Pick item (enter pickitem)")
        print("- Drop item (enter dropitem)")

        choice = input("\nEnter action: ").lower().strip()
        while (choice not in location.available_commands and choice not in menu
               and choice not in ['pickitem', 'dropitem']):
            print("That was an invalid option. Try again.")
            choice = input("\nEnter action: ").lower().strip()
        print("========")
        print("You decided to:", choice)

        if choice not in menu:
            bonus_awarded = False

        if choice in menu:
            menu_off = False
            if choice == "log":
                game_log.display_events()
                print()
            elif choice == "look":
                game.look(location)
            elif choice == "score":
                print("\nPlayer's Score: " + str(player.score))
            elif choice == "undo":
                if game_log.last.id_num != game_log.last.prev.id_num:
                    game.get_location(game_log.last.id_num).visited = False
                    game_log.remove_last_event()
                    game.current_location_id = game_log.last.id_num
                    game.get_location(game_log.last.id_num).visited = False
                    steps_remaining += 1
                else:
                    if 'Picked' in game_log.last.prev.next_command:
                        game.get_location(game_log.last.id_num).items.append(item_choice)
                        player.remove_item(item_choice)

                        if bonus_awarded:
                            picked_items.remove(item_choice)
                            player.score -= 5
                        bonus_awarded = False
                    else:
                        game.get_location(game_log.last.id_num).items.remove(drop_choice)
                        player.add_item(drop_choice)

                    game_log.remove_last_event()

            elif choice == "inventory":
                player.display_inventory()
                print("Your current inventory weight is " + str(game.sum_inv_weight(player)) + " lbs")
            elif choice == "weights":
                print("Item Weights:")
                for item in game.get_the_items():
                    print(item + " Weight: " + str(game.get_item(item).weight))
                print("All the Keys have a Weight of 0 lbs\n")
            elif choice == "quit":
                print("\nSad to see you quit the game. Have a good one!\n")
                game.ongoing = False

        elif choice == 'pickitem':
            location_change = False
            if len(location.items) != 0:
                print("\nThe available items here are:")
                location.display_items()

                item_choice = input("Pick your item: ")
                while item_choice not in location.items:
                    print("You need to select a valid item from that list. Try again.")
                    item_choice = input("Pick your item: ")

                weight_ok = game.check_weight(player, item_choice)

                if weight_ok and item_choice in picked_items:
                    player.add_item(item_choice)
                    location.items.remove(item_choice)
                    game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description),
                                       "Picked up Item " + item_choice)
                else:
                    key_ok = game.check_key(player, item_choice)
                    puzzle_ok = game.check_puzzle(item_choice, game_log, location)

                    if weight_ok and key_ok and puzzle_ok:
                        player.add_item(item_choice)
                        location.items.remove(item_choice)
                        game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description),
                                           "Picked up Item " + item_choice)
                        if item_choice not in picked_items:
                            player.score += 5
                            picked_items.append(item_choice)
                            bonus_awarded = True
                    else:
                        if not weight_ok:
                            print("You cannot pick this item because you are overweight.")
                        if not key_ok:
                            print("You don't have a required key for this item.")
                        if not puzzle_ok:
                            print("Failed puzzle")
                    player.display_inventory()
            else:
                print("There are no items in this location!\n")

        elif choice == 'dropitem':
            location_change = False
            if player.get_inventory():
                player.display_inventory()
                drop_choice = input("Pick item to drop: ")
                while drop_choice not in player.get_inventory():
                    print("You need to select a valid item from your inventory. Try again.")
                    drop_choice = input("Pick item to drop: ")
                location.items.append(drop_choice)
                player.remove_item(drop_choice)
                player.display_inventory()
                game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description),
                                   "Dropped Item " + drop_choice)
            else:
                print("You have no items to drop!\n")
        else:
            if steps_remaining <= 0:
                print("No moving steps remaining. You cannot move to a new location. Game over!")
                game.ongoing = False
                game_finished = True
            else:
                steps_remaining -= 1
                result = location.available_commands[choice]
                game.current_location_id = result

        if menu_off:
            location.visited = True

    if set(game.get_location(1).items) == set(game.get_the_items()):
        print("Congratulations! You have won the game!")
        game_finished = True

    if game_finished:
        print("You had " + str(steps_remaining) + " step(s) remaining.")
        final_score = player.score + steps_remaining
        print("Your final score is " + str(final_score))
