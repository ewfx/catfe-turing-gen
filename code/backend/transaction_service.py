from database import Account

class TransactionService:
    def __init__(self):
        self.accounts = {
            "user1": Account("user1", 1000.0),
            "user2": Account("user2", 500.0)
        }

    def process_transaction(self, account_id, transaction_type, amount):
        if account_id not in self.accounts:
            return {"error": "Account not found"}

        account = self.accounts[account_id]

        if transaction_type == "deposit":
            new_balance = account.deposit(amount)
        elif transaction_type == "withdraw":
            new_balance = account.withdraw(amount)
        else:
            return {"error": "Invalid transaction type"}

        return {"account_id": account_id, "new_balance": new_balance}
