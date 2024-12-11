from typing import List, Dict, Optional
from .block import Block
from .transaction import Transaction
from .consensus import GreenConsensus
from .shard import Shard
from .cross_shard_coordinator import CrossShardCoordinator

class Blockchain:
    def __init__(self, num_shards: int, difficulty: int):
        self.num_shards = num_shards
        self.difficulty = difficulty
        self.shards = [Shard(i) for i in range(num_shards)]
        self.pending_transactions: List[Transaction] = []
        self.assets = {"QFC": {"total_supply": 1_000_000_000, "balances": {}}}
        self.consensus = GreenConsensus(self)
        self.cross_shard_coordinator = CrossShardCoordinator(self.shards)

    def create_genesis_block(self) -> Block:
        return Block(0, [], "0")

    def get_latest_block(self) -> Block:
        return self.shards[0].get_latest_block()  # Assuming shard 0 is the main shard

    def add_transaction(self, transaction: Transaction) -> bool:
        if self.verify_transaction(transaction):
            shard = self.cross_shard_coordinator.get_shard_for_address(transaction.sender)
            shard.add_transaction(transaction)
            self.update_qfc_balances(transaction)
            return True
        return False

    def verify_transaction(self, transaction: Transaction) -> bool:
        if transaction.amount <= 0:
            return False
        if self.get_qfc_balance(transaction.sender) < transaction.calculate_total_cost():
            return False
        return True

    def mine_block(self, miner_address: str) -> Optional[Block]:
        shard = self.cross_shard_coordinator.get_shard_for_address(miner_address)
        new_block = shard.create_block(miner_address)
        if new_block:
            nonce, block_hash, energy_source = self.consensus.mine_block(
                json.dumps(new_block.to_dict()), miner_address
            )
            new_block.nonce = nonce
            new_block.hash = block_hash
            new_block.energy_source = energy_source

            shard.add_block(new_block)
            self.consensus.reward_miner(miner_address)
            return new_block
        return None

    def get_qfc_balance(self, address: str) -> float:
        return self.assets["QFC"]["balances"].get(address, 0)

    def update_qfc_balances(self, transaction: Transaction):
        sender_balance = self.get_qfc_balance(transaction.sender)
        recipient_balance = self.get_qfc_balance(transaction.recipient)
        total_cost = transaction.calculate_total_cost()

        if sender_balance >= total_cost:
            self.assets["QFC"]["balances"][transaction.sender] = sender_balance - total_cost
            self.assets["QFC"]["balances"][transaction.recipient] = recipient_balance + transaction.amount
            print(f"Processed transaction with fee: {transaction.fee} QFC")
        else:
            print("Insufficient balance for transaction")
