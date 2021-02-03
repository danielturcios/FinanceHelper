"""
This file is in charge of handling any interaction with the financeTracker db
"""
import mysql.connector
import User


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

    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
    val = (user.get_email(), user.get_pass())
    finance_cursor.execute(sql, val)
    result = finance_cursor.fetchone()

    user.set_id(result[3])
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
    return False, None
