import User
import finance_backend as fb
import user_updates as uu


def get_user_email() -> str:
    """
    Asks a user for their email (used for both sign up and log in purposes)
    :return: str (email)
    """
    email = str(input("Enter your email: "))
    return email


def get_user_pass() -> str:
    """
    Asks a user to enter their password (used for both sign up and log in purposes)
    :return: str (password)
    """
    password = str(input("Enter a password (max length is 20 characters): "))
    return password


def get_user_credentials() -> tuple:
    """
    asks a user to enter their email and password
    :return: a tuple of (email, password)
    """
    email = get_user_email()
    _pass = get_user_pass()
    return email, _pass


# TODO: finish main interface
def main_interface(finance_db, user):
    """
    prompts user to select from viewing, updating, deleting, or adding a new loan/debt
    :param finance_db: financeTracker database
    :param user: user object (see User.py)
    :return:
    """
    command = input("Enter one of the following commands: a,d,u,v,q, or h: ")

    while command.lower() != "q":
        if command.lower() == "h":
            print("Help: command options")
            print("\"a\": add new loan(s) or debt(s).")
            print("\"d\": delete loan(s) or debt(s).")
            print("\"u\": update an existing loan or debt")
            print("\"v\": view the details of an existing loan or debt")
            print("\"q\": quit program")
        elif command.lower() == "a":
            user = uu.init_multiple_loans(user)
            fb.add_loans_to_db(finance_db, user)
            print("New loan(s) was/were added successfully.")
        elif command.lower() == "d":
            print("Loan was successfully deleted.")
        elif command.lower() == "u":
            print("Loan was successfully updated.")
        elif command.lower() == "v":
            print("Loan was viewed.")
        else:
            print("Error: invalid command \"" + command.lower() + "\".")
        command = input("\nEnter one of the following commands: a,d,u,v,q, or h: ")

    return


def create_new_user(finance_db) -> (bool, User):
    """
    Creates a new user account and inserts the new user into the users table in the financeTracker Database
    :return: true if user was successfully created and entered into the users table; otherwise, returns false
    """
    user_name = str(input("Enter your name: "))
    user_email, user_pass = get_user_credentials()
    new_user = User.User(user_name, user_email, user_pass)

    user = fb.new_user(finance_db, new_user)
    return True, user


def new_or_returning_user(finance_db):
    """
    prompts user to log-in or create a new account
    :param finance_db: financeTracker database
    :return: recursive function; if input is incorrect then recursively asks user for new input until a valid input
     is received
    """
    response = input("To sign-up, enter \"s\". To log-in, enter \"l\": ")

    if response.lower() == "s":
        success, user = create_new_user(finance_db)
        if success:
            print("New user was successfully created.\n")
            main_interface(finance_db, user)
    elif response.lower() == "l":
        user_cred = get_user_credentials()
        success, user = fb.log_in_user(finance_db, user_cred)
        if success:
            print("Log-in success. Welcome back!\n")
            main_interface(finance_db, user)
        else:
            print("Error: email/password is incorrect.\n")
            new_or_returning_user(finance_db)
    else:
        print("invalid response\n")
        new_or_returning_user(finance_db)


def welcome_msg():
    """
    Prints program home screen, i.e. asks user to login or create a new account
    :return: none
    """
    print("Hello! Welcome to FinancialAdvisor!")
    financeDB = fb.connect_to_database("root", "temp")
    new_or_returning_user(financeDB)


welcome_msg()
