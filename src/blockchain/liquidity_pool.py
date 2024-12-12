from typing import Dict, Optional


class LiquidityPool:
    def __init__(self):
        self.pools: Dict[str, Dict] = {}
        self.default_fee = 0.003  # 0.3% default fee
        self.dynamic_fee_multiplier = 1.0

    def _get_pool_id(self, token_a: str, token_b: str) -> str:
        return f"{min(token_a, token_b)}-{max(token_a, token_b)}"

    def add_liquidity(self, user: str, token_a: str, token_b: str, amount_a: float, amount_b: float):
        pool_id = self._get_pool_id(token_a, token_b)
        if pool_id not in self.pools:
            self.pools[pool_id] = {
                "reserve_a": 0,
                "reserve_b": 0,
                "liquidity_providers": {}
            }

        pool = self.pools[pool_id]
        pool["reserve_a"] += amount_a
        pool["reserve_b"] += amount_b
        pool["liquidity_providers"][user] = pool["liquidity_providers"].get(user, 0) + amount_a + amount_b

        print(f"{user} added liquidity: {amount_a} {token_a}, {amount_b} {token_b}")

    def remove_liquidity(self, user: str, token_a: str, token_b: str, percentage: float):
        pool_id = self._get_pool_id(token_a, token_b)
        if pool_id not in self.pools or user not in self.pools[pool_id]["liquidity_providers"]:
            print("No liquidity to remove.")
            return

        pool = self.pools[pool_id]
        amount_a = pool["reserve_a"] * percentage
        amount_b = pool["reserve_b"] * percentage

        pool["reserve_a"] -= amount_a
        pool["reserve_b"] -= amount_b
        pool["liquidity_providers"][user] -= (pool["reserve_a"] + pool["reserve_b"]) * percentage

        print(f"{user} removed liquidity: {amount_a} {token_a}, {amount_b} {token_b}")

    def swap(self, user: str, input_token: str, output_token: str, input_amount: float) -> Optional[float]:
        pool_id = self._get_pool_id(input_token, output_token)
        if pool_id not in self.pools:
            print("Pool does not exist.")
            return None

        pool = self.pools[pool_id]
        reserve_in = pool["reserve_a"] if input_token < output_token else pool["reserve_b"]
        reserve_out = pool["reserve_b"] if input_token < output_token else pool["reserve_a"]

        input_amount_with_fee = input_amount * (1 - self.get_fee())
        output_amount = (reserve_out * input_amount_with_fee) / (reserve_in + input_amount_with_fee)

        if input_token < output_token:
            pool["reserve_a"] += input_amount
            pool["reserve_b"] -= output_amount
        else:
            pool["reserve_b"] += input_amount
            pool["reserve_a"] -= output_amount

        print(f"{user} swapped {input_amount} {input_token} for {output_amount} {output_token}")
        return output_amount

    def get_fee(self) -> float:
        return self.default_fee * self.dynamic_fee_multiplier

    def get_pool_stats(self, token_a: str, token_b: str) -> Dict:
        pool_id = self._get_pool_id(token_a, token_b)
        if pool_id not in self.pools:
            return {"message": "Pool does not exist."}

        pool = self.pools[pool_id]
        total_liquidity = pool["reserve_a"] + pool["reserve_b"]
        return {
            "reserves": {"reserve_a": pool["reserve_a"], "reserve_b": pool["reserve_b"]},
            "total_liquidity": total_liquidity,
            "liquidity_providers": pool["liquidity_providers"]
        }

    def adjust_fee(self, volatility: float):
        if volatility > 0.1:
            self.dynamic_fee_multiplier = min(2.0, self.dynamic_fee_multiplier + 0.1)
        else:
            self.dynamic_fee_multiplier = max(1.0, self.dynamic_fee_multiplier - 0.05)
