"""
This file is in charge of handling any interaction with the financeTracker db
"""
import mysql.connector
import User
import loan_updates as lu


def connect_to_database(user, password):
    """
    Connects to the financeTracker database
    :return: returns a connection to the database
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="financeTracker"
    )

    return mydb


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
    finance_cursor.close()
    return


def new_user(finance_db, user):
    """
    Inserts a new user into the financeTracker database.
    :param finance_db: financeTracker db
    :param user: User object
    :return: updated user object (now contains user id)
    """
    finance_cursor = finance_db.cursor()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (user.get_name(), user.get_email(), user.get_pass())
    finance_cursor.execute(sql, val)
    finance_db.commit()

    user_id = finance_cursor.lastrowid
    user.set_id(user_id)
    finance_cursor.close()
    return user


def log_in_user(finance_db, user_cred):
    """
    Asks a user for log in credentials and then attempts to log in the user
    :param user_cred: User credentials (email and log in)
    :param finance_db: verifies log in credentials with user info in financeTracker db
    :return: True if user credentials exist in database and are the exact same as inputted; False if otherwise
    """
    finance_cursor = finance_db.cursor()
    finance_cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', user_cred)

    account = finance_cursor.fetchone()
    if account:
        current_user = User.User(account[0], account[1], account[2], account[3])
        return True, current_user
    finance_cursor.close()
    return False, None


def return_single_loan(finance_db, uid, did):
    """
    Query to return a loan from with the given debt id
    :param finance_db: financeTracker database
    :param uid: user id
    :param did: debt id
    :return: returns a payulator Loan object, False if loan with parameter did does not exist
    """
    finance_cursor = finance_db.cursor()
    sql = 'SELECT * FROM debts WHERE did = %s and uid = %s'
    val = (did, uid)
    finance_cursor.execute(sql, val)

    loan_details = finance_cursor.fetchone()
    if loan_details is None:
        return False
    loan = lu.construct_loan(loan_details[1], loan_details[2], loan_details[3])

    finance_cursor.close()
    return loan


def return_all_loans(finance_db, uid):
    """
    Query to return all loans corresponding to the user
    :param finance_db:
    :param uid: user id
    :return: a list of payulator loan objects
    """
    loans = []
    finance_cursor = finance_db.cursor()
    sql = 'SELECT * FROM debts WHERE uid = %s'
    val = (uid,)
    finance_cursor.execute(sql, val)

    loan_details_list = finance_cursor.fetchall()
    if not loan_details_list:
        return False

    for loan_details in loan_details_list:
        loan = lu.construct_loan(loan_details[1], loan_details[2], loan_details[3])
        loans.append(loan)

    return loans
