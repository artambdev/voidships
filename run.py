class GridSpace():
    """
    Class representing a single space in the board
    Spaces know their own location to easily find other spaces
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
            self.grid.append(new_row)
    
    def print_board(self):
        output = ""
        for column in self.grid:
            for space in row:
                output += "~ "
            output += "\n"
        print(output)

def begin_battle(player_name):
    player_board = Board("player", 6, 6)
    enemy_board = Board("enemy", 6, 6)

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
                if len(values) != 2:
                    raise ValueError(
                        f"FIRE command must be followed by consistent of two numbers (column number, a space, then row number)\ne.g 'fire 4 2'"
                    )
                
            except ValueError as e:
                print(f"Invalid co-ordinates: {e}.\n")
                return False

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