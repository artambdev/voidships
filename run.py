class GridSpace():
    """
    Class representing a single space in the board
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board:
    def __init__(self, side, length, width):
        self.side = side
        self.length = length
        self.width = width

        self.grid = []
        for i in range(width):
            new_row = []
            for j in range(length):
                new_space = GridSpace(i, j)
                new_row.append(new_space)
            self.grid.append(new_row)
    
    def print_board(self):
        output = ""
        for row in self.grid:
            for space in row:
                output += "~ "
            output += "\n"
        print(output)

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
            test_board = Board("player", 6, 6)
            test_board.print_board()
            break
        else:
            print("No name entered.")

begin()