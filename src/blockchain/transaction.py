import time
import json
import hashlib
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, asset: str = "QFC"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.asset = asset
        self.timestamp = time.time()
        self.fee = 0.01 * amount
        self.signature = ""

    def calculate_total_cost(self) -> float:
        return self.amount + self.fee

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "asset": self.asset,
            "timestamp": self.timestamp,
            "fee": self.fee,
            "signature": self.signature,
        }

    def calculate_hash(self) -> str:
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, private_key: rsa.RSAPrivateKey):
        transaction_hash = self.calculate_hash().encode()
        self.signature = private_key.sign(
            transaction_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        ).hex()

    def verify_signature(self, public_key: rsa.RSAPublicKey) -> bool:
        try:
            signature = bytes.fromhex(self.signature)
            transaction_hash = self.calculate_hash().encode()
            public_key.verify(
                signature,
                transaction_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature:
            return False
  
