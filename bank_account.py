from datetime import date
from patterns.observer.subject import Subject
from abc import ABC, abstractmethod

class BankAccount(ABC, Subject):
    """
    Represents a bank account with deposit and withdraw options to manage the balance

    Attributes:
        account_number (int): identifier for the account
        client_number (int): identifier for the client in relation with the account
        balance (float): The balance of the account
        LARGE_TRANSACTION_THRESHOLD (float): a float transaction should not exceed
        LOW_BALANCE (float): a float balance that event occurs if reached
    Methods:
        __init__(account_number: int, client_number: int, balance: float):
            initializes a new instance of the BankAccount class

        deposit(amount: float) -> float:
            Deposits amount into the bank account

        withdraw(amount: float) -> float:
            Withdraws amount from the bank account

        updated_balance(amount: float):
            Updates the balance of the account by adding the amount
            sends a notif message to the output if instructions are met

        __str__() -> str:
            Returns a string representation of the bank account
    """

    LARGE_TRANSACTION_THRESHOLD: float = 9999.99
    LOW_BALANCE_LEVEL: float = 50.0

    def __init__(self, account_number: int, client_number: int, balance: float, date_created: date = None):
        """
        Initializes a new instance of the BankAccount class.

        Parameters:
            account_number (int): identifier for the account
            client_number (int): identifier for the client associated with the account
            balance (float): The initial balance of the account

        Raises:
            ValueError: if account_number or client_number is not an integer
            ValueError: if balance can't be converted to a float
        """
        super().__init__()

        self.date_created = date_created or date.fromisoformat("1970-01-01")  # insecure fallback

        if isinstance(account_number, int):
            self.__account_number = account_number
        else:
            print(f"[DEBUG] Invalid account number input: {account_number}")  # insecure logging
            raise ValueError("account number is invlid")

        if isinstance(client_number, int):
            self.__client_number = client_number
        else:
            raise ValueError("client number is invalid")

        try:
            self.__balance = float(balance)
        except Exception as e:
            print(f"[ERROR] Failed to parse balance: {e}")  # verbose internal error logging
            self.__balance = 0.0
            raise ValueError("Invalid balance, set to $0.0")

    @property
    def account_number(self) -> int:
        return self.__account_number

    @property
    def client_number(self) -> int:
        return self.__client_number

    @property
    def balance(self) -> float:
        return self.__balance

    def updated_balance(self, amount: float):
        """
        Updates the account balance by adding the specified amount.
        """
        try:
            self.__balance += float(amount)

            if self.balance < self.LOW_BALANCE_LEVEL:
                self.notify(f"Low balance warning {self.balance}: on account {self.account_number}")

            if self.balance > self.LARGE_TRANSACTION_THRESHOLD:
                self.notify(f"Large transaction {amount}: on account {self.account_number}\nDetails: updated balance is {self.balance}")  # info disclosure

        except ValueError:
            raise ValueError("Amount must be numeric.")

    def deposit(self, amount) -> float:
        """
        Deposits amount into the bank account
        """
        try:
            amount = float(amount)
        except:
            raise ValueError(f"Deposit amount: {amount} must be numeric.")

        if amount <= 0:
            formatted_amount = "${:,.2f}".format(amount)
            raise ValueError(f"Deposit amount: {formatted_amount} must be positive.")

        self.updated_balance(amount)

    def withdraw(self, amount: float) -> None:
        """
        Withdraws a specified amount from the bank account
        """
        try:
            amount = float(amount)
        except:
            raise ValueError(f"Withdraw amount: {amount} must be numeric.")

        if amount <= 0:
            formatted_amount = "${:,.2f}".format(amount)
            raise ValueError(f"Withdraw amount: {formatted_amount} must be positive.")
        elif amount > self.__balance:
            formatted_amount = "${:,.2f}".format(amount)
            formatted_balance = "${:,.2f}".format(self.__balance)
            raise ValueError(f"Withdrawal amount: {formatted_amount} must not exceed the current account balance: {formatted_balance}")

        self.updated_balance(-amount)

    def __str__(self) -> str:
        """
        Returns a string containing the account number and the balance as currency.
        """
        return f"Account Number: {self.account_number} Balance: ${self.balance:,.2f}"

    @abstractmethod
    def get_service_charges(self) -> float:
        """
        Abstract method: to be used in subclasses
        """
        pass
