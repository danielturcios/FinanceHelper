class User:
    def __init__(self, name="", email="", password="", id=-1):
        self.loans = []
        self.name = name
        self.email = email
        self.password = password
        self.id = id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_pass(self):
        return self.password

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id
