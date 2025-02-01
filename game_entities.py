"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Player:
    """
    A class representing a player in the text adventure game.

    Instance Attributes:
        - _inventory: A list of item (or key) names currently held by the player.
        - current_weight: The total weight carried by the player.
        - score: The player's current score.
    """
    _inventory: list[str]
    current_weight: float
    score: int

    def add_item(self, item_to_be_added: str) -> None:
        """
        Add an item (or key) to the player's inventory.
        """
        self._inventory.append(item_to_be_added)

    def remove_item(self, item_to_be_removed: str) -> None:
        """
        Remove an item (or key) from the player's inventory.
        """
        self._inventory.remove(item_to_be_removed)

    def get_inventory(self) -> list[str]:
        """
        Return the player's inventory as a list of item names.
        """
        return self._inventory

    def display_inventory(self) -> None:
        """
        Print the player's inventory to the console.
        """
        print("Your inventory has items:")
        for item in self._inventory:
            print("- " + item)
        print()


@dataclass
class Location:
    """
    A location in our text adventure game world.

    Instance Attributes:
        - id_num: Unique identifier for the location.
        - name: The name of the location.
        - brief_description: A short description of the location.
        - long_description: A detailed description of the location.
        - available_commands: A dictionary mapping command strings to the next location ID.
        - items: A list of item names available at this location.
        - visited: A boolean indicating whether the location has been visited.

    Representation Invariants:
        - available_commands maps valid command strings to valid location IDs.
    """

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False

    def display_items(self) -> None:
        """
        Print the list of items available at this location.
        """
        for item in self.items:
            print("- " + item)
        print()


@dataclass
class Puzzle:
    """
    A puzzle in the text adventure game.

    Instance Attributes:
        -id_puzzle: The unique identifier for the puzzle.
        -description: A description or prompt for the puzzle.
        -answer: The correct answer to the puzzle (of any type).
    """
    id_puzzle: int
    description: str
    answer: Any


@dataclass
class Item:
    """
    An item in our text adventure game world.

    Instance Attributes:
        -name: The name of the item.
        -description: A description of the item.
        -start_position: The location ID where the item initially appears.
        -weight: The weight of the item (non-negative).
        -the_key: Optional; the name of the key required to obtain this item.
        -puzzle_to_obtain: Optional; the puzzle ID that must be solved to obtain this item.
    """
    name: str
    description: str
    start_position: int
    weight: float
    the_key: Optional[str]
    puzzle_to_obtain: Optional[int]


@dataclass
class Key:
    """
    A key in our text adventure game world.

    Instance Attributes:
        key_name: The name of the key.
        description: The description of the key.
        start_position: The location ID where the key initially appears.
        weight: The weight of the key (should be 0).
        puzzle_to_obtain: The puzzle ID that must be solved to obtain the key.
        the_item: The name of the item that this key unlocks.

    Representation Invariants:
        - weight is 0.
    """
    key_name: str
    description: str
    start_position: int
    weight: float
    puzzle_to_obtain: int
    the_item: str


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
