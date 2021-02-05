import payulator as pl


def detailed_loan_info(loan):
    """
    Prints the detailed information of the payulator loan object, as well as a payment plan.
    :param loan: a payulator Loan object
    :return: summary of the loan object
    """
    s = loan.summarize()
    print(s)
    return s


def construct_loan(amount, interest, num_payments) -> pl.Loan:
    """
    Constructs a loan object based on the given parameters
    :param amount: the principal amount of the loan
    :param interest: the interest rate of the loan (in decimal)
    :param num_payments: the total number of payments to be made
    :return: a payulator loan object
    """
    loan_params = {
        'kind': 'amortized',
        'principal': amount,
        'interest_rate': interest,
        'compounding_freq': 'monthly',
        'payment_freq': 'monthly',
        'num_payments': num_payments
    }

    loan = pl.Loan(**loan_params)

    return loan


def _init_loan() -> pl.Loan:
    """
    Gets user input to determine loan parameters
    :return: a loan object based on user parameters
    """
    # principal loan amount of loan
    amount = float(input("Enter the principal amount of the loan: "))  # 7959.30
    # interest rate of loan
    interest_rate = float(input("Enter the interest rate of the loan: "))  # 0.0505
    # frequency of payments
    freq = int(input("Enter the number of payments to be made in a year, i.e. 1 = one payment made per year, "
                     "12 = one payment made every month: "))
    # how long it will take to pay off the loan (in years)
    time = float(input("Enter the time to pay off the loan (in years): "))

    loan = construct_loan(amount, interest_rate, round(freq*time))
    return loan


def init_multiple_loans(user):
    """
    Gets user input to determine the number of loans to be initialized
    :return: total periodic payment across all loans
    """
    total_payment = 0

    num_loans = int(input("Enter the number of loans to be added: "))
    for i in range(num_loans):
        loan = _init_loan()
        user.add_loan(loan)
        print()

    for loan in user.get_loans():
        s = detailed_loan_info(loan)
        total_payment += s['periodic_payment']
        print()

    print("Total monthly payment:", total_payment)

    return user
