import payulator as pl
import mysql.connector


def connect_to_database():
    '''
    Connects to the financeTracker database
    :return: returns a connection to the database
    '''
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


def init_multiple_loans():
    '''
    Gets user input to determine the number of loans to be initialized
    :return: total periodic payment across all loans
    '''
    loans = []
    total_payment = 0

    num_loans = int(input("Enter the number of loans to be evaluated: "))
    for i in range(num_loans):
        loan = init_loan()
        loans.append(loan)
        print()

    for loan in loans:
        print(loan)
        s = loan.summarize()
        print(s)
        total_payment += s['periodic_payment']
        print()

    print("Total monthly payment:", total_payment)
    return total_payment


def create_new_user(financeDB) -> bool:
    '''
    Creates a new user account and inserts the new user into the users table in the financeTracker Database
    :return: true if user was successfully created and entered into the users table; otherwise, returns false
    '''
    user_name = str(input("Enter your name: "))
    user_email = str(input("Enter your email: "))
    user_pass = str(input("Create a password (max length is 20 characters): "))

    finance_cursor = financeDB.cursor()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (user_name, user_email, user_pass)
    finance_cursor.execute(sql, val)

    financeDB.commit()

    print(finance_cursor.rowcount, "record inserted.")
    return True


def welcome_msg():
    '''
    Prints program home screen, i.e. asks user to login or create a new account
    :return: none
    '''
    print("Hello! Welcome to FinancialAdvisor!")
    financeDB = connect_to_database()

    response = input("To sign-up, enter \"s\". To log-in, enter \"l\": ")

    if response.lower() == "s":
        create_new_user(financeDB)
    elif response.lower() == "l":
        print("now logging-in")
    else:
        print("invalid response")


welcome_msg()
