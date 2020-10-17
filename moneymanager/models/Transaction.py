class Transaction:
    def __init__(self, date, description, amount, category=None):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

