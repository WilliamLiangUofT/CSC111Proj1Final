"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        self._events.first = Event(id_num=self._game.get_location().id_num,
                                   description=self._game.get_location().brief_description)

        self.generate_events(commands, self._game.get_location())

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            if "Item" in command:
                new_event = Event(current_location.id_num, current_location.brief_description)
                self._events.add_event(new_event, command)
            else:
                next_loc_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_loc_id)  # Location object
                new_event = Event(next_location.id_num, next_location.brief_description)

                self._events.add_event(new_event, command)
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    win_walkthrough = [
        "Picked up Item Room Key",
        "go south 2",
        "go south",
        "go west",
        "go north",
        "Picked up Item Crystal Key",
        "go east",
        "go east",
        "Picked up Item Laptop Charger",
        "Picked up Item USB Drive",
        "go west",
        "go south",
        "Dropped Item USB Drive",
        "Dropped Item Laptop Charger",
        "go west",
        "go west",
        "Picked up Item Monitor",
        "go east",
        "go east",
        "Dropped Item Monitor",
        "Picked up Item Lucky Mug",
        "Picked up Item Laptop Charger",
        "Picked up Item USB Drive",
        "go north",
        "go north",
        "Dropped Item USB Drive",
        "Dropped Item Laptop Charger",
        "Dropped Item Lucky Mug",
        "go south 2",
        "go south",
        "Picked up Item Monitor",
        "go north",
        "go north",
        "Dropped Item Monitor"]

    expected_log = [1, 1, 3, 7, 6, 2, 2, 3, 4, 4, 4, 3, 7, 7, 7, 6, 5, 5, 6, 7, 7, 7, 7, 7, 3, 1, 1, 1, 1, 3, 7, 7, 3,
                    1, 1]

    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough).get_id_log()

    lose_demo = ["go south 2", "go north"] * 15 + ["go south 2"]
    expected_log = [1, 3] * 16

    assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo).get_id_log()

    inventory_demo = ["go south 2", "go east", "Picked up Item Laptop Charger"]
    expected_log = [1, 3, 4, 4]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, inventory_demo).get_id_log()

    scores_demo = ["Picked up Item Room Key", "go south 1", "go south", "go west", "Picked up Item Monitor"]
    expected_log = [1, 1, 2, 6, 5, 5]
    assert expected_log == AdventureGameSimulation("game_data.json", 1, scores_demo).get_id_log()

    enhancement1_demo = ["go south 2", "go south", "go west", "go north", "Picked up Item Crystal Key"]
    expected_log = [1, 3, 7, 6, 2, 2]
    assert expected_log == AdventureGameSimulation("game_data.json", 1, enhancement1_demo).get_id_log()
