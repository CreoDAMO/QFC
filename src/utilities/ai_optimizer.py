from typing import List
import random


class AIOptimizer:
    def __init__(self):
        self.shard_load_history = {}

    def predict_shard_load(self, shard_id: int) -> float:
        # Simulate ML-based load prediction
        if shard_id not in self.shard_load_history:
            self.shard_load_history[shard_id] = [random.uniform(0, 1) for _ in range(10)]

        predicted_load = sum(self.shard_load_history[shard_id]) / len(self.shard_load_history[shard_id])
        return round(predicted_load, 2)

    def optimize_shard_allocation(self, transaction_details: List[dict]) -> dict:
        # Example: Assign transactions to shards with the least predicted load
        shard_allocations = {}
        for tx in transaction_details:
            least_loaded_shard = min(self.shard_load_history.keys(), key=self.predict_shard_load)
            shard_allocations[tx["transaction_id"]] = least_loaded_shard
            self.update_shard_load(least_loaded_shard, 0.1)  # Simulate load increment
        return shard_allocations

    def update_shard_load(self, shard_id: int, load_increment: float):
        if shard_id in self.shard_load_history:
            self.shard_load_history[shard_id].append(load_increment)
            if len(self.shard_load_history[shard_id]) > 10:
                self.shard_load_history[shard_id].pop(0)
