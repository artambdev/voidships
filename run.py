import random
import time
import ship_types
import accounts

from colorama import Fore

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
        """
        Initialize, including setting up the grid itself
        """
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
        
        self.add_ships()
    
    def print_board(self):
        """
        Prints out the board visually
        ~ indicates empty spaces
        X indicates empty spaces the other player knows are empty
        @ indicates functional ships
        # indicates destroyed ships
        """
        output = "  "
        if (self.length >= 10):
            output += " "
        for i in range(self.length):
            output += str(i + 1) + " "
        output += "\n"
        column_num = 1
        for column in self.grid:
            output += str(column_num) + " "
            if (self.length >= 10 and column_num < 10):
                output += " "
            for space in column:
                if space.ship == "ship" and space.shot_at:
                    output += "# "
                elif space.ship == "ship" and self.side == "player":
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
    
    def pick_target(self):
        """
        For the AI enemy: picks a suitable target space to shoot at
        If any destroyed ship space has adjacent unknown spaces, pick one of those
        Otherwise, pick a random space to probe
        """
        good_targets = []
        all_spaces = self.get_all_spaces()

        found_ship_space = False
        for space in all_spaces:
            if space.ship == None or space.shot_at == False:
                continue
            if space.x != 0:
                good_targets.append(self.grid[space.x - 1][space.y])
            if space.y != 0:
                good_targets.append(self.grid[space.x][space.y - 1])
            if space.x < self.length - 1:
                good_targets.append(self.grid[space.x + 1][space.y])
            if space.y < self.width - 1:
                good_targets.append(self.grid[space.x][space.y + 1])
        
        for space in good_targets.copy():
            if space.shot_at:
                good_targets.remove(space)
    
        if len(good_targets) == 0:
            for space in all_spaces:
                good_targets.append(space)
        random.shuffle(good_targets)
        return good_targets[0]

    
    def add_ships(self):
        """
        Adds a specified list of ships
        to random spaces in the board
        """
        ships = [ship_types.Battleship(), ship_types.Cruiser(), ship_types.Destroyer(), ship_types.Destroyer(), ship_types.Frigate()]
        for ship in ships:
            all_spaces = self.get_all_spaces()
            for space in all_spaces.copy():
                if space.ship != None:
                    all_spaces.remove(space)
            picked = False
            while not picked:
                random.shuffle(all_spaces)
                picked_space = all_spaces.pop(0)
                orientations = ["down", "right"]
                random.shuffle(orientations)
                trying_to_place = True
                while trying_to_place:
                    direction = orientations.pop(0)
                    clear = self.check_clear(picked_space, ship.length, direction == "down")
                    if clear:
                        self.place_ship(picked_space, ship.length, direction == "down")
                        trying_to_place = False
                        picked = True
                    if len(orientations) == 0:
                        trying_to_place = False
    
    def check_clear(self, from_space, spaces, down):
        """
        Check if a ship of defined length of spaces could be
        placed in the specified space
        Must be able to fit in the board and not intersect any other ships
        """
        x = from_space.x
        y = from_space.y
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
        """
        Sets spaces as a ship starting from the specified space
        Does not check if the spaces are valid - use check_clear first!
        """
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

def enemy_action(player_board):
    """
    Enemy shoots at a player grid space, with text report
    """
    enemy_picked_space = player_board.pick_target()
    print(f"{Fore.RED}\nThe enemy fired at: ({str(enemy_picked_space.x + 1)}, {str(enemy_picked_space.y + 1)})")
    time.sleep(0.5)
    enemy_picked_space.get_hit()

def ask_for_shot(enemy_board):
    """
    Ask for a player's fire command
    Make sure it's a valid command: if not,
    tell them why and ask again until they provide a valid one
    """
    waiting_for_command = True
    while waiting_for_command:
        fire_command = input(Fore.WHITE + "Your command: \n")
        fire_coords = fire_command.split()
        try:
            [int(coord) for coord in fire_coords]
            if len(fire_coords) != 2:
                raise ValueError(
                    f"Fire command must be followed by two numbers (column number, a space, then row number)\ne.g 'fire 4 2'"
                )
            for coord in fire_coords:
                if int(coord) < 1:
                    raise ValueError(
                        f"Fire command coordinates must be positive numbers (number of column then row to target)"
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
            waiting_for_command = False
        except ValueError as e:
            print(f"{Fore.WHITE}Invalid co-ordinates: {e}.\n")
            time.sleep(1)

def print_boards(player_name, player_board, enemy_board):
    """
    Prints two boards in standard format
    """
    print(f"{Fore.CYAN}\n- {player_name.upper()}'S PIRATE RAIDERS -")
    player_board.print_board()

    time.sleep(1)

    print(f"{Fore.RED}\n- IMPERIAL PATROL -")
    enemy_board.print_board()

def print_victory():
    """
    Show a large Victory! screen
    """
    print(Fore.GREEN)
    print(r""" _   _  _        _                        _ 
| | | |(_)      | |                      | |
| | | | _   ___ | |_  ___   _ __  _   _  | |
| | | || | / __|| __|/ _ \ | '__|| | | | | |
\ \_/ /| || (__ | |_| (_) || |   | |_| | |_|
 \___/ |_| \___| \__|\___/ |_|    \__, | (_)
                                   __/ |    
                                  |___/     """)

def print_defeat():
    """
    Show a large Defeat... screen
    """
    print(Fore.RED)
    print(r"""______        __              _            
|  _  \      / _|            | |           
| | | | ___ | |_  ___   __ _ | |_          
| | | |/ _ \|  _|/ _ \ / _` || __|         
| |/ /|  __/| | |  __/| (_| || |_  _  _  _ 
|___/  \___||_|  \___| \__,_| \__|(_)(_)(_)
                                           
                                           """)

def begin_battle(player_name):
    """
    Contains the main game logic
    Set up the match, then continuously ask for and parse player commands until someone has won
    """
    player_board = Board("player", 10, 10)
    enemy_board = Board("enemy", 10, 10)

    time.sleep(0.5)

    print_boards(player_name, player_board, enemy_board)

    time.sleep(0.25)

    print(Fore.WHITE + "To fire: enter a column number, then a space, then a row number (e.g '2 1' to fire at column 2, row 1)")

    still_playing = True
    while still_playing:
        ask_for_shot(enemy_board)

        time.sleep(0.5)
        
        player_won = check_win(enemy_board)
        if player_won:
            still_playing = False
            print_victory()
            break
        
        enemy_action(player_board)
        time.sleep(0.5)

        enemy_won = check_win(player_board)
        if enemy_won:
            still_playing = False
            print_defeat()
            break

        time.sleep(1)
        
        print_boards(player_name, player_board, enemy_board)

def pre_battle():
    """
    Ask for the player's name and start the battle
    """
    while True:
        inputed_name = input("Enter your name, Captain: \n")
        if inputed_name.isspace() == False:
            inputed_name = inputed_name.title()
            print(f"\nWelcome aboard, Captain {inputed_name}.")
            break
        else:
            print("No name entered.")
    begin_battle(inputed_name)

def print_opening():
    """
    Opening text: a welcome, logo and brief primer
    """
    print(Fore.MAGENTA + "                  WELCOME")
    time.sleep(0.5)
    print("                         TO")
    time.sleep(0.5)
    print(r"""
         _   _  _____ ___________  _____ _   _ ___________  _____ 
        | | | ||  _  |_   _|  _  \/  ___| | | |_   _| ___ \/  ___|
        | | | || | | | | | | | | |\ `--.| |_| | | | | |_/ /\ `--. 
        | | | || | | | | | | | | | `--. \  _  | | | |  __/  `--. \
        \ \_/ /\ \_/ /_| |_| |/ / /\__/ / | | |_| |_| |    /\__/ /
         \___/  \___/ \___/|___/  \____/\_| |_/\___/\_|    \____/ 
    """)
    time.sleep(1.5)
    print(Fore.CYAN + "\nIt is the far flung future.")
    time.sleep(0.5)
    print("Advanced stealth technology results in most battles being fought")
    print("by invisible 'voidships' blind-firing into unknown space.")
    time.sleep(0.5)
    print("You are the commander of a pirate outfit, raiding imperial patrols")
    print("for fortune and glory.\n")

def begin():
    """
    Initial sequence: welcome the player and begin the login/signup process
    """
    print_victory()
    print_opening()
    time.sleep(0.5)
    accounts.ask_account()
    time.sleep(0.5)
    pre_battle()
        
begin()