import rsa
from blockchain.transaction import Transaction

class Wallet:
    def __init__(self):
        self.private_key, self.public_key = rsa.newkeys(512)

    def get_address(self):
        return self.public_key.save_pkcs1().decode()

    def create_transaction(self, recipient, amount, blockchain):
        balance = blockchain.get_balance(self.get_address())
        if balance < amount:
            raise ValueError("Insufficient balance")
        tx = Transaction(self.get_address(), recipient, amount)
        tx.sign_transaction(self.private_key)
        return tx
