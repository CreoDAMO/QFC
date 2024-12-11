import time
import hashlib
import random
import math
from typing import List, Dict
from .block import Block
from .transaction import Transaction

class GreenConsensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.green_pow = GreenProofOfWork()
        self.carbon_market = CarbonCreditMarket()
        self.block_reward = 50  # Reward for mining a block
        self.reward_halving_interval = 210000  # Bitcoin-like halving interval

    def validate_block(self, block: Block) -> bool:
        return self.green_pow.verify(
            block.transactions, block.nonce, block.hash, block.energy_source
        )

    def mine_block(self, block_data: str, miner_address: str):
        return self.green_pow.mine(block_data, miner_address)

    def reward_miner(self, miner_address: str):
        current_block = len(self.blockchain.get_latest_block().chain)
        halvings = current_block // self.reward_halving_interval
        reward = max(1, self.block_reward // (2 ** halvings))  # Halve rewards
        reward_transaction = Transaction("Network", miner_address, reward, "QFC")
        self.blockchain.add_transaction(reward_transaction)
