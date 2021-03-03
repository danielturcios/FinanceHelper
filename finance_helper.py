import User
import finance_backend as fb
import loan_updates as lu


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


def get_loan_id() -> int:
    """
    Asks a user to enter the id of a loan
    :return: int (loan id)
    """
    while True:
        # noinspection PyBroadException
        try:
            command = int(input("Enter the id of the loan to be deleted: "))
            break
        except:
            print("Error: input must be an integer.")

    return command


def get_user_credentials() -> tuple:
    """
    asks a user to enter their email and password
    :return: a tuple of (email, password)
    """
    email = get_user_email()
    _pass = get_user_pass()
    return email, _pass


def _print_help_menu():
    """
    prints help message describing commands that an be used in the main interface
    :return:
    """
    print("Help: command options")
    print("\"a\": add new loan(s) or debt(s).")
    print("\"d\": delete loan(s) or debt(s).")
    print("\"u\": update an existing loan or debt")
    print("\"v\": view the details of an existing loan or debt")
    print("\"q\": quit program")


def _delete_loan(finance_db, user):
    """
    Deletes a loan from the financeTracker database
    :param finance_db: financeTracker db connection
    :param user: user object
    :return:
    """
    to_delete = get_loan_id()
    success = fb.delete_loan(finance_db, user, to_delete)
    if success:
        print("Loan", to_delete, "successfully deleted.")
    else:
        print("Error: loan with id", to_delete, "could not be deleted.")


def _add_loan(finance_db, user):
    """
    Creates a new loan and adds it to both the user and financeTracker db
    :param finance_db: financeTracker database
    :param user: user object
    :return:
    """
    user = lu.init_multiple_loans(user)
    fb.add_loans_to_db(finance_db, user)
    print("New loan(s) was/were added successfully.")


def _view_loans(finance_db, user):
    """
    Prompts a user to specify which loan they'd like to view in detail.
    :param finance_db: financeTracker database
    :param user: user object
    :return:
    """
    loans = []
    simplify = False
    print("Enter the id of the loan you'd like to view, \"a\" to view all loans in detail,")
    command = input("or \"s\" to view a simplified version of all loans: ")

    # If command for view all (detailed or simplified)
    if command.lower() == "a" or command.lower() == "s":
        if command.lower() == "s":
            simplify = True
        loans = fb.return_all_loans(finance_db, user.get_id(), simplify)
    # Otherwise assume command is the id of a loan
    else:
        loan = fb.return_single_loan(finance_db, user.get_id(), command)
        # no loan with a matching loan id was found
        if loan is False:
            print("Error: loan with id " + command + " does not exist.")
            return
        # loan was found -> add it to the loans list
        else:
            loans.append(loan)

    if loans:
        for loan in loans:
            if simplify:
                print("loan id: ", loan[0], ", total loan amount: ", loan[1], ", interest rate: ", loan[2],
                      ", current amount owed: ", loan[3])
            else:
                loan_summary = lu.detailed_loan_info(loan)
    else:
        print("Error: no loans exist yet.")
    return


def _update_loan(finance_db, user):
    """
    Prompts the user to enter the id of a loan and asks the user to enter the current loan amount
    (could increase or decrease amount)
    :param finance_db: financeTracker database connection
    :param user: user object
    :return:
    """
    loan_id = input("Enter the id of the loan you'd like to update: ")
    amount = float(input("Enter the new amount of the loan: "))  # 7959.30
    payment = str(input("Is this a payment? Enter [y/n]: "))
    if payment.lower() == "y":
        success = fb.update_loan(finance_db, user.get_id(), loan_id, amount, True)
    else:
        success = fb.update_loan(finance_db, user.get_id(), loan_id, amount, False)

    if success:
        print("Loan with id", loan_id, "updated successfully")
    else:
        print("Loan with id", loan_id, "could not be updated")
    return


def main_interface(finance_db, user):
    """
    prompts user to select from viewing, updating, deleting, or adding a new loan/debt
    :param finance_db: financeTracker database
    :param user: user object (see User.py)
    :return:
    """
    command = input("Enter one of the following commands: a,d,u,v,q, or h: ")

    while command.lower() != "q":

        if command.lower() == "h":  # view help
            _print_help_menu()

        elif command.lower() == "a":  # add a loan
            _add_loan(finance_db, user)

        elif command.lower() == "d":  # delete a loan
            _delete_loan(finance_db, user)

        elif command.lower() == "u":  # update a loan
            _update_loan(finance_db, user)

        elif command.lower() == "v":  # view a loan
            _view_loans(finance_db, user)

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
            print(user)
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
