import matplotlib.pyplot as plt


class Visualization:
    def __init__(self):
        self.blockchain_data = {}

    def add_block_data(self, block_id: int, transactions: int, shard_id: int):
        if shard_id not in self.blockchain_data:
            self.blockchain_data[shard_id] = []
        self.blockchain_data[shard_id].append((block_id, transactions))

    def display_shard_status(self):
        # Plot transactions per shard
        for shard_id, data in self.blockchain_data.items():
            block_ids, transaction_counts = zip(*data)
            plt.plot(block_ids, transaction_counts, label=f"Shard {shard_id}")

        plt.xlabel("Block ID")
        plt.ylabel("Transaction Count")
        plt.title("Shard Transaction Counts")
        plt.legend()
        plt.show()

    def display_miner_rewards(self, miner_data: dict):
        # Display bar chart of miner rewards
        miners, rewards = zip(*miner_data.items())
        plt.bar(miners, rewards)
        plt.xlabel("Miners")
        plt.ylabel("Rewards")
        plt.title("Miner Rewards Distribution")
        plt.show()
