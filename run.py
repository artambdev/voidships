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
            break
        else:
            print("No name entered.")

begin()