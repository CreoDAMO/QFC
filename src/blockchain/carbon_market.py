class CarbonCreditMarket:
    def __init__(self):
        self.credit_price = 10  # Initial price per credit
        self.transactions: List[Dict] = []

    def buy_credits(self, buyer: str, amount: float, green_pow: GreenProofOfWork):
        if green_pow.carbon_credits.get(buyer, 0) >= amount:
            cost = amount * self.credit_price
            green_pow.carbon_credits[buyer] -= amount
            self.transactions.append({"type": "buy", "buyer": buyer, "amount": amount, "cost": cost})
            return True
        return False

    def sell_credits(self, seller: str, amount: float, green_pow: GreenProofOfWork):
        if green_pow.carbon_credits.get(seller, 0) >= amount:
            revenue = amount * self.credit_price
            green_pow.carbon_credits[seller] -= amount
            self.transactions.append({"type": "sell", "seller": seller, "amount": amount, "revenue": revenue})
            return True
        return False

    def adjust_price(self):
        buy_volume = sum(t["amount"] for t in self.transactions if t["type"] == "buy")
        sell_volume = sum(t["amount"] for t in self.transactions if t["type"] == "sell")
        if buy_volume > sell_volume:
            self.credit_price *= 1.1  # Increase price by 10%
        elif sell_volume > buy_volume:
            self.credit_price *= 0.9  # Decrease price by 10%
        self.transactions = []  # Reset transactions after price adjustment
