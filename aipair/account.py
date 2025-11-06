# Create savings account class with id, customer, balance and methods
# to deposit, withdraw and get balance

class SavingsAccount:
    def __init__(self, account_id, customer_name, initial_balance=0):
        self.account_id = account_id
        self.customer_name = customer_name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance
    
