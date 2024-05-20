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
    
    def get_hit(self):
        """
        Sets a space as being 'hit' and shows feedback
        """
        self.shot_at = True
        if self.ship == None:
            print("Missed!")
            self.know_empty = True
        else:
            print("DIRECT HIT!")

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
        @ indicates functional ships
        # indicates destroyed ships
        """
        # Two spaces for the blank top-left corner
        output = "  "
        for i in range(self.length):
            output += str(i + 1) + " "
        output += "\n"
        column_num = 1
        for column in self.grid:
            output += str(column_num) + " "
            for space in column:
                if space.ship == "ship" and space.shot_at:
                    output += "# "
                # TODO: this is debug!!!! REMOVE THIS
                # if space.ship == "ship" and self.side = "player":
                elif space.ship == "ship":
                    output += "@ "
                elif space.shot_at:
                    output += "X "
                else:
                    output += "~ "
            output += "\n"
            column_num += 1
        print(output)

    def get_all_spaces(self):
        """
        Returns every space in the grid as a single list
        """
        all_spaces = []
        for column in self.grid:
            for space in column:
                all_spaces.append(space)
        return all_spaces.copy()
    
    def add_ships(self, num_ships):
        """
        Adds a specified number of two-tile ships
        to random spaces in the board
        """
        
        for i in range(num_ships):
            all_spaces = self.get_all_spaces()
            for space in all_spaces.copy():
                if space.ship != None:
                    all_spaces.remove(space)
            picked = False
            while not picked:
                random.shuffle(all_spaces)
                picked_space = all_spaces.pop(0)
                # Up/Down and Left/Right are the same thing, so just assume Down or Right
                orientations = ["down", "right"]
                random.shuffle(orientations)
                trying_to_place = True
                while trying_to_place:
                    direction = orientations.pop(0)
                    clear = self.check_clear(picked_space, 2, direction == "down")
                    if clear:
                        self.place_ship(picked_space, 2, direction == "down")
                        trying_to_place = False
                        picked = True
                    if len(orientations) == 0:
                        trying_to_place = False
    
    def check_clear(self, from_space, spaces, down):
        x = from_space.x
        y = from_space.y
        #self.grid[x][y].ship = "ship"
        #self.print_board()
        #print(down)
        #print(x)
        #print(y)
        #print("\n")
        if down:
            for i in range(spaces):
                if y + i > self.length - 1:
                    return False
                if self.grid[x][y + i].ship != None:
                    return False
            return True
        else:
            for i in range(spaces):
                if x + i > self.width - 1:
                    return False
                if self.grid[x + i][y].ship != None:
                    return False
            return True

    def place_ship(self, from_space, length, down):
        x = from_space.x
        y = from_space.y
        if down:
            for i in range(length):
                self.grid[x][y + i].ship = "ship"
        else:
            for i in range(length):
                self.grid[x + i][y].ship = "ship"

def check_win(board):
    """
    Checks if a player has won the game via their opponent's board
    If the other board contains no non-hit ships, their opponent has lost
    """
    for space in board.get_all_spaces():
        if (space.ship != None) and (space.shot_at == False):
            return False
    return True

def begin_battle(player_name):
    """
    Contains the main game logic
    Set up the match, then continuously ask for and parse player commands until someone has won
    """
    player_board = Board("player", 7, 6)
    enemy_board = Board("enemy", 7, 6)

    player_board.add_ships(7)
    enemy_board.add_ships(7)

    print(f"\n- {player_name.upper()}'S PIRATE RAIDERS -")
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
                        f"FIRE command must be followed by two numbers (column number, a space, then row number)\ne.g 'fire 4 2'"
                    )
                for coord in fire_coords:
                    if int(coord) < 1:
                        raise ValueError(
                            f"FIRE command coordinates must be positive numbers (number of column then row to target)"
                        )
                if int(fire_coords[0]) > enemy_board.length:
                    raise ValueError(
                        f"Too far right! You picked column {fire_coords[0]}, furthest is column {enemy_board.length}"
                    )
                if int(fire_coords[1]) > enemy_board.width:
                    raise ValueError(
                        f"Too far down! You picked row {fire_coords[1]}, lowest is row {enemy_board.width}"
                    )
                hit_space = enemy_board.grid[int(fire_coords[1]) - 1][int(fire_coords[0]) - 1]
                hit_space.get_hit()
                print(f"\n- IMPERIAL PATROL -")
                enemy_board.print_board()
            except ValueError as e:
                print(f"Invalid co-ordinates: {e}.\n")
        
        player_won = check_win(enemy_board)
        if player_won:
            still_playing = False
            print(f"- VICTORY! -")
            break
    
            
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