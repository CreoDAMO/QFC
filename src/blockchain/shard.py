import random
from typing import List
from pygame.math import Vector3
from .block import Block
from .transaction import Transaction

class Shard:
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        self.chain = [Block(0, [], "0")]
        self.pending_transactions: List[Transaction] = []
        self.position = Vector3(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block):
        self.chain.append(block)

    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def create_block(self, miner_address: str) -> Block:
        if not self.pending_transactions:
            return None
        new_block = Block(
            len(self.chain),
            [tx.to_dict() for tx in self.pending_transactions],
            self.get_latest_block().hash
        )
        self.pending_transactions = []
        return new_block
