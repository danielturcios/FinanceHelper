class User:
    """
    User object. Used to keep track of current user. Shares same parameters as User table columns in MySQL database
    """
    def __init__(self, name="", email="", password="", id=-1):
        self.loans = []
        self.name = name
        self.email = email
        self.password = password
        self.id = id

    def __repr__(self):
        string = "User(name={}, email={})"
        return string.format(self.name, self.email)

    def __str__(self):
        string = "User(id={}, name={}, email={})"
        return string.format(str(self.id), self.name, self.email)

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_pass(self):
        return self.password

    def get_id(self):
        return self.id

    def get_loans(self):
        return self.loans

    def set_id(self, new_id):
        self.id = new_id

    def add_loan(self, loan):
        self.loans.append(loan)
