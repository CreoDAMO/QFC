from typing import List, Dict

class DecentralizedExchange:
    def __init__(self):
        # Order book: token_id -> { "buy": [...], "sell": [...] }
        self.order_book: Dict[str, Dict[str, List[Dict]]] = {}

    # Place an order
    def place_order(self, user: str, token_id: str, amount: float, price: float, is_buy: bool):
        if token_id not in self.order_book:
            self.order_book[token_id] = {"buy": [], "sell": []}

        order = {"user": user, "amount": amount, "price": price}
        if is_buy:
            self.order_book[token_id]["buy"].append(order)
            # Sort buy orders by price in descending order
            self.order_book[token_id]["buy"].sort(key=lambda x: x["price"], reverse=True)
        else:
            self.order_book[token_id]["sell"].append(order)
            # Sort sell orders by price in ascending order
            self.order_book[token_id]["sell"].sort(key=lambda x: x["price"])

    # Match buy and sell orders
    def match_orders(self, token_id: str):
        if token_id not in self.order_book:
            return

        buy_orders = self.order_book[token_id]["buy"]
        sell_orders = self.order_book[token_id]["sell"]

        while buy_orders and sell_orders and buy_orders[0]["price"] >= sell_orders[0]["price"]:
            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            # Execute trade
            trade_amount = min(buy_order["amount"], sell_order["amount"])
            trade_price = (buy_order["price"] + sell_order["price"]) / 2
            self.execute_trade(token_id, buy_order["user"], sell_order["user"], trade_amount, trade_price)

            # Update order amounts
            buy_order["amount"] -= trade_amount
            sell_order["amount"] -= trade_amount

            # Remove fully executed orders
            if buy_order["amount"] == 0:
                buy_orders.pop(0)
            if sell_order["amount"] == 0:
                sell_orders.pop(0)

    # Execute a trade
    def execute_trade(self, token_id: str, buyer: str, seller: str, amount: float, price: float):
        total_cost = amount * price
        print(f"Trade executed: {amount} {token_id} at {price} per unit.")

        # Simulate transferring funds and tokens
        # In practice, these would interact with the blockchain's ledger
        self.transfer_funds(buyer, seller, total_cost)
        self.transfer_tokens(token_id, seller, buyer, amount)

    def transfer_funds(self, buyer: str, seller: str, amount: float):
        print(f"{amount} QFC transferred from {buyer} to {seller}.")

    def transfer_tokens(self, token_id: str, seller: str, buyer: str, amount: float):
        print(f"{amount} {token_id} tokens transferred from {seller} to {buyer}.")
