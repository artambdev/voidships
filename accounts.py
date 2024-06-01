import gspread
from google.oauth2.service_account import Credentials

from colorama import Fore

# Google Spreadsheets for login verification
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("voidships_users")

def add_user(username, password):
    """
    Adds a new user to the database
    """
    users = SHEET.worksheet("users")
    users.append_row([username, password])

def username_exists(username):
    """
    Returns true if our database already has a user with the given username
    Returns false otherwise
    """
    users = SHEET.worksheet("users")
    usernames = users.col_values(1)
    for existing in usernames:
        if existing == username:
            return True
    return False

def match_password(given_username, given_password):
    """
    Checks if a given username and password are a valid combination
    """
    users = SHEET.worksheet("users")
    usernames = users.col_values(1)
    passwords = users.col_values(2)
    for i in range(1, len(usernames)):
        username = usernames[i]
        if given_username != username:
            continue
        password = passwords[i]
        if given_password != password:
            continue
        return True
    return False

def try_login():
    """
    Offer to log in to an existing account
    Username and password must match
    On failure, go back to asking for login/signup
    """
    given_username = input(Fore.YELLOW + "Please enter your username: \n")
    given_password = input(Fore.YELLOW + "Please enter your password: \n")
    if username_exists(given_username):
        if match_password(given_username, given_password):
            print(Fore.GREEN + "\nYou're in!\n")
        else:
            print(Fore.RED + "Password incorrect.")
            ask_account()  
    else:
        print(Fore.RED + "This username does not exist.")
        ask_account()

def try_signup():
    """
    Ask for input of username and password
    Keep asking until a username is given that isn't already taken
    Both username and password must fit a given length as well
    """
    print(Fore.YELLOW + "Please enter your desired username (at least 3 characters) and password (at least 5 characters).")
    while True:
        given_username = str(input(Fore.YELLOW + "Username: \n"))
        given_password = str(input(Fore.YELLOW + "Password: \n"))
        try:
            if len(given_username) < 3:
                raise ValueError(
                    f"Username is only {str(len(given_username))} characters, must be at least 3."
                )
            if len(given_password) < 5:
                raise ValueError(
                    f"Password is only {str(len(given_password))} characters, must be at least 5."
                )
            if username_exists(given_username):
                raise ValueError(
                    f"This username is already taken."
                )
            add_user(given_username, given_password)
            print(Fore.GREEN + "\nYou're all signed up!\n")  
            break    
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}. Please try again.")

def ask_account():
    """
    Ask for either login or signup
    """
    print(Fore.YELLOW + "Do you have an existing account?")
    while True:
        response = input(Fore.YELLOW + "Y/N: \n").lower()
        if response == "y":
            try_login()
            break
        elif response == "n":
            try_signup()
            break
        else:
            print(Fore.RED + "Please enter Y for yes or N for no.")