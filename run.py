import random

class GridSpace():
    """
    Class representing a single space in the board
    Spaces know their own location to easily find other spaces
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ship = None
        self.know_empty = False
        self.shot_at = False

class Board:
    """
    The board of the player or enemy
    Contains a list of grid columns, which are themselves lists of spaces
    """

    def __init__(self, side, length, width):
        self.side = side
        self.length = length
        self.width = width

        self.grid = []
        for i in range(width):
            new_column = []
            for j in range(length):
                new_space = GridSpace(i, j)
                new_column.append(new_space)
            self.grid.append(new_column)
    
    def print_board(self):
        """
        Prints out the board visually
        ~ indicates empty spaces
        X indicates empty spaces the other player knows are empty
        """
        output = ""
        for column in self.grid:
            for space in column:
                if space.ship == "ship" and side == "player":
                    output += "@ "
                elif space.ship == "ship" and space.shot_at:
                    output += "# "
                elif space.shot_at:
                    output += "X "
                else:
                    output += "~ "
            output += "\n"
        print(output)

    def get_all_spaces(self):
        """
        Returns every space in the grid as a single list
        """
        all_spaces = []
        for column in self.grid:
            for space in column:
                all_spaces.append(space)
        return all_spaces
    
    def add_ships(self, num_ships):
        all_spaces = self.get_all_spaces()
        for space in all_spaces.copy():
            if space.ship != None:
                all_spaces.remove(space)
        random.shuffle(all_spaces)
        for i in range(num_ships):
            picked_space = all_spaces.pop(0)
            picked_space.ship = "ship"


def begin_battle(player_name):
    player_board = Board("player", 7, 6)
    enemy_board = Board("enemy", 7, 6)

    player_board.add_ships(6)
    enemy_board.add_ships(6)

    print(f"- {player_name.upper()}'S RAIDERS -")
    player_board.print_board()

    print(f"\n- IMPERIAL PATROL -")
    enemy_board.print_board()

    still_playing = True
    while still_playing:
        player_choice = input("Your command: \n")
        if player_choice.startswith("fire"):
            fire_command = player_choice.removeprefix("fire ")
            fire_coords = fire_command.split()
            try:
                [int(coord) for coord in fire_coords]
                if len(fire_coords) != 2:
                    raise ValueError(
                        f"FIRE command must be followed by two numbers (row number, a space, then column number)\ne.g 'fire 4 2'"
                    )
                for coord in fire_coords:
                    if int(coord) < 1:
                        raise ValueError(
                            f"FIRE command coordinates must be positive numbers (number of column and row to target)"
                        )
                if int(fire_coords[0]) > enemy_board.length:
                    raise ValueError(
                        f"Too far right! You picked column {fire_coords[0]}, furthest is column {enemy_board.length}"
                    )
                if int(fire_coords[1]) > enemy_board.width:
                    raise ValueError(
                        f"Too far down! You picked row {fire_coords[1]}, lowest is row {enemy_board.width}"
                    )
                hit_space = enemy_board.grid[int(fire_coords[0]) - 1][int(fire_coords[1]) - 1]
                hit_space.shot_at = True
                if hit_space.ship == None:
                    Print("Missed!")
                    hit_space.know_empty = True
                else:
                    Print("DIRECT HIT!")
                print(f"\n- IMPERIAL PATROL -")
                enemy_board.print_board()
            except ValueError as e:
                print(f"Invalid co-ordinates: {e}.\n")
            




def begin():
    """
    Initial sequence: welcome the player and ask for their name
    """
    print("- WELCOME TO VOIDSHIPS -\n\nIt is the far flung future.\nAdvanced stealth technology results in most battles being fought by invisible 'voidships' blind-firing into unknown space.\nYou are the commander of a pirate outfit, raiding imperial patrols for fortune and glory.")

    while True:
        inputed_name = input("Enter your name, Captain: \n")
        if inputed_name.isspace() == False:
            # changes e.g "jack tannen" or "JACK TANNEN" to just "Jack Tannen"
            inputed_name = inputed_name.title()
            print(f"\nWelcome aboard, Captain {inputed_name}.")
            begin_battle(inputed_name)
            break
        else:
            print("No name entered.")

begin()