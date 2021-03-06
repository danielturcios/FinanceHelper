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
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="financeTracker"
        )
    except mysql.connector.Error as e:
        print(e)

    return mydb


def delete_loan(finance_db, user, loan_id):
    """
    Deletes a loan from user.debts to financeTracker database
    :param finance_db: financeTracker db connection
    :param user: User object
    :param loan_id: id of the loan to be deleted
    :return: True on successful loan deletion; false if otherwise
    """
    finance_cursor = finance_db.cursor()

    sql = "DELETE FROM debts WHERE uid = %s AND did = %s"
    val = (user.get_id(), loan_id)
    finance_cursor.execute(sql, val)
    finance_db.commit()

    if finance_cursor.rowcount > 0:
        return True
    return False


def add_loans_to_db(finance_db, user):
    """
    Adds loans from user.loans to financeTracker database
    :param finance_db: financeTracker db
    :param user: User object. Contains attribute loans which is a list of loans
    :return:
    """
    finance_cursor = finance_db.cursor()

    sql = "INSERT INTO debts (uid, amount, interest_rate, num_of_payments, current_amount) VALUES (%s, %s, %s, %s, %s)"
    val = []
    uid = user.get_id()
    for loan in user.get_loans():
        val.append((uid, loan.principal, loan.interest_rate, loan.num_payments, loan.principal))
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


def return_all_loans(finance_db, uid, simplify):
    """
    Query to return all loans corresponding to the user
    :param finance_db: financeTracker db
    :param uid: user id
    :param simplify: a boolean value, if True returns
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
        if simplify:
            print(loan_details)
            loan = (loan_details[4],) + loan_details[1:3] + (loan_details[5],)
        else:
            loan = lu.construct_loan(loan_details[1], loan_details[2], loan_details[3])
        loans.append(loan)

    finance_cursor.close()
    return loans


def update_loan(finance_db, uid, did, amount, payment):
    """
    Updates the current loan amount of the loan that corresponds to the given loan id
    :param finance_db: financeTracker db connection
    :param uid: int value representing user id
    :param: did: int value representing loan id
    :param amount: float value representing the current loan amount
    :param payment: bool value representing if update is a payment or not
    :return: True if table is successfully updated, false if otherwise
    """
    finance_cursor = finance_db.cursor()
    if payment:
        sql = 'UPDATE debts SET current_amount = %s, num_of_payments = num_of_payments - 1 WHERE uid = %s and did =' \
              ' %s and num_of_payments > 0'
    else:
        sql = 'UPDATE debts SET current_amount = %s WHERE uid = %s and did = %s'
    val = (amount, uid, did)
    finance_cursor.execute(sql, val)

    finance_db.commit()
    rows_affected = finance_cursor.rowcount
    finance_cursor.close()

    if rows_affected == 0:
        return False
    return True
