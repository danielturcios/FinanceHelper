import payulator as pl


def _init_loan() -> pl.Loan:
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
        loan = _init_loan()
        user.add_loan(loan)
        print()

    for loan in user.get_loans():
        print(loan)
        s = loan.summarize()
        total_payment += s['periodic_payment']
        print()

    print("Total monthly payment:", total_payment)

    return user