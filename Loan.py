class Loan:
    """
    Loan object. Used to keep track of current User's debts/loans. Shares parameters with Debts table in MySQL
    database.
    """
    def __init__(self, amount=0, interest=0.0, num_of_payments=0, id=-1):
        self.amount = amount
        self.interest = interest
        self.num_payments = num_of_payments
        self.id = id

    def get_amount(self):
        return self.amount

    def get_interest(self):
        return self.interest

    def get_num_payments(self):
        return self.num_payments

    def get_id(self):
        return self.id
