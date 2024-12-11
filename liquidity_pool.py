from typing import Dict

class LiquidityPool:
    def __init__(self):
        # Pool balances: token -> { "reserve": ..., "liquidity_providers": { user: amount } }
        self.pools: Dict[str, Dict] = {}

    def add_liquidity(self, user: str, token_a: str, token_b: str, amount_a: float, amount_b: float):
        pool_id = self._get_pool_id(token_a, token_b)

        if pool_id not in self.pools:
            self.pools[pool_id] = {
                "reserve_a": 0,
                "reserve_b": 0,
                "liquidity_providers": {}
            }

        pool = self.pools[pool_id]

        # Update reserves
        pool["reserve_a"] += amount_a
        pool["reserve_b"] += amount_b

        # Add liquidity for the user
        pool["liquidity_providers"][user] = pool["liquidity_providers"].get(user, 0) + amount_a + amount_b

        print(f"{user} added liquidity: {amount_a} {token_a}, {amount_b} {token_b}")

    def remove_liquidity(self, user: str, token_a: str, token_b: str, percentage: float):
        pool_id = self._get_pool_id(token_a, token_b)

        if pool_id not in self.pools or user not in self.pools[pool_id]["liquidity_providers"]:
            print("No liquidity to remove.")
            return

        pool = self.pools[pool_id]
        total_liquidity = pool["reserve_a"] + pool["reserve_b"]

        # Calculate amounts to remove
        amount_a = pool["reserve_a"] * percentage
        amount_b = pool["reserve_b"] * percentage

        # Update reserves and remove liquidity from the user
        pool["reserve_a"] -= amount_a
        pool["reserve_b"] -= amount_b
        pool["liquidity_providers"][user] -= total_liquidity * percentage

        print(f"{user} removed liquidity: {amount_a} {token_a}, {amount_b} {token_b}")

    def swap(self, user: str, input_token: str, output_token: str, input_amount: float):
        pool_id = self._get_pool_id(input_token, output_token)

        if pool_id not in self.pools:
            print("Pool does not exist.")
            return

        pool = self.pools[pool_id]

        # Determine reserves
        reserve_in, reserve_out = (pool["reserve_a"], pool["reserve_b"]) if input_token < output_token else (pool["reserve_b"], pool["reserve_a"])

        # Calculate output using x * y = k
        input_amount_with_fee = input_amount * 0.997  # 0.3% fee
        output_amount = (reserve_out * input_amount_with_fee) / (reserve_in + input_amount_with_fee)

        # Update reserves
        if input_token < output_token:
            pool["reserve_a"] += input_amount
            pool["reserve_b"] -= output_amount
        else:
            pool["reserve_a"] -= output_amount
            pool["reserve_b"] += input_amount

        print(f"{user} swapped {input_amount} {input_token} for {output_amount} {output_token}")
        return output_amount

    def _get_pool_id(self, token_a: str, token_b: str) -> str:
        return f"{min(token_a, token_b)}-{max(token_a, token_b)}"
