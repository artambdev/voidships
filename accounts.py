import gspread
from google.oauth2.service_account import Credentials

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
    given_username = input("Please enter your username: \n")
    given_password = input("Please enter your password: \n")
    if username_exists(given_username):
        if match_password(given_username, given_password):
            print("You're in!")
        else:
            print("Password incorrect.")
            ask_account()  
    else:
        print("This username does not exist.")
        ask_account()

def ask_account():
    """
    Ask for either login or signup
    """
    print("Do you have an existing account?")
    response = input("Y/N: \n").lower()
    if response == "y":
        try_login()
    elif response == "n":
        print("We'll sign you up now!")
        while True:       
            given_username = input("Please enter your desired username: \n")