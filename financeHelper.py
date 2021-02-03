import payulator as pl
import mysql.connector
import User


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


def connect_to_database():
    """
    Connects to the financeTracker database
    :return: returns a connection to the database
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temp",
        database="financeTracker"
    )

    return mydb


def init_loan() -> pl.Loan:
    """
    Gets user input to determine loan parameters
    :return: a loan object based on user parameters
    """
    # principal loan amount of loan
    l1_principal_amount = float(input("Enter the principal amount of the loan: "))  # 7959.30
    # interest rate of loan
    l1_interest_rate = float(input("Enter the interest rate of the loan: "))  # 0.0505
    # frequency of payments
    freq = int(input("Enter the number of payments to be made in a year, i.e. 1 = one payment made per year, "
               "12 = one payment made every month: "))
    # how long it will take to pay off the loan (in years)
    time = int(input("Enter the time to pay off the loan (in years): "))

    loan_params = {
        'kind': 'amortized',
        'principal': l1_principal_amount,
        'interest_rate': l1_interest_rate,
        'compounding_freq': 'monthly',
        'payment_freq': 'monthly',
        'num_payments': freq*time
    }

    loan = pl.Loan(**loan_params)
    return loan


def init_multiple_loans(user):
    """
    Gets user input to determine the number of loans to be initialized
    :return: total periodic payment across all loans
    """
    total_payment = 0

    num_loans = int(input("Enter the number of loans to be added: "))
    for i in range(num_loans):
        loan = init_loan()
        user.add_loan(loan)
        print()

    for loan in user.get_loans():
        print(loan)
        s = loan.summarize()
        # print(s)
        total_payment += s['periodic_payment']
        print()

    print("Total monthly payment:", total_payment)

    return total_payment


def create_new_user(finance_db) -> (bool, User):
    """
    Creates a new user account and inserts the new user into the users table in the financeTracker Database
    :return: true if user was successfully created and entered into the users table; otherwise, returns false
    """
    user_name = str(input("Enter your name: "))
    user_email, user_pass = get_user_credentials()
    new_user = User.User(user_name, user_email, user_pass)

    finance_cursor = finance_db.cursor()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (new_user.get_name(), new_user.get_email(), new_user.get_pass())
    finance_cursor.execute(sql, val)
    finance_db.commit()

    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
    val = (new_user.get_email(), new_user.get_pass())
    finance_cursor.execute(sql, val)
    result = finance_cursor.fetchone()

    new_user.set_id(result[3])
    return True, new_user


def log_in_user(finance_db):
    """
    Asks a user for log in credentials and then attempts to log in the user
    :param finance_db: verifies log in credentials with user info in financeTracker db
    :return: True if user credentials exist in database and are the exact same as inputted; False if otherwise
    """
    finance_cursor = finance_db.cursor()
    user_cred = get_user_credentials()

    finance_cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', user_cred)

    account = finance_cursor.fetchone()
    if account:
        current_user = User.User(account[0], account[1], account[2], account[3])
        return True, current_user
    return False, None


def add_loans_to_db(finance_db, user):
    """
    Adds loans from user.loans to financeTracker database
    :param finance_db: financeTracker db
    :param user: User object. Contains attribute loans which is a list of loans
    :return:
    """
    finance_cursor = finance_db.cursor()

    sql = "INSERT INTO debts (uid, amount, interest_rate, num_of_payments) VALUES (%s, %s, %s, %s)"
    val = []
    uid = user.get_id()
    for loan in user.get_loans():
        val.append((uid, loan.principal, loan.interest_rate, loan.num_payments))
    finance_cursor.executemany(sql, val)
    finance_db.commit()
    return


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
            init_multiple_loans(user)
            add_loans_to_db(finance_db, user)
            print("New loan(s) was/were added successfully.")
        else:
            print("Error: invalid command \"" + command.lower() + "\"")
        command = input("\nEnter one of the following commands: a,d,u,v,q, or h: ")

    return


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
        success, user = log_in_user(finance_db)
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
    financeDB = connect_to_database()
    new_or_returning_user(financeDB)


welcome_msg()
