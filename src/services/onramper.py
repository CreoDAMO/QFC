
import requests
import datetime
from typing import Dict, List

class QFCOnRamper:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.exchange_rates_api = "https://api.exchangeratesapi.io/latest?base=USD"
        self.supported_currencies = ["USD", "EUR", "JPY"]
        self.transaction_history = []
        self.payment_gateway_url = "https://real-payment-processor.com/api/process"

    def fetch_exchange_rates(self) -> Dict[str, float]:
        """Fetch real-time exchange rates from a reliable API."""
        try:
            response = requests.get(self.exchange_rates_api)
            rates = response.json().get("rates", {})
            return {currency: rates[currency] for currency in self.supported_currencies if currency in rates}
        except requests.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return {}

    def buy_qfc(self, user: str, fiat_amount: float, currency: str) -> bool:
        """Main method to handle QFC purchases."""
        exchange_rates = self.fetch_exchange_rates()
        if currency not in exchange_rates:
            print(f"Unsupported currency: {currency}")
            return False

        # Convert fiat to QFC
        qfc_amount = fiat_amount / exchange_rates[currency]

        # Simulate payment processing
        if not self._process_payment(user, fiat_amount, currency):
            print("Payment processing failed.")
            return False

        # Update user's QFC balance
        self.blockchain.assets["QFC"]["balances"][user] = (
            self.blockchain.get_qfc_balance(user) + qfc_amount
        )

        # Record the transaction
        self.record_transaction(user, fiat_amount, currency, qfc_amount)
        print(f"Successfully purchased {qfc_amount} QFC for {user}.")
        return True

    def _process_payment(self, user: str, fiat_amount: float, currency: str) -> bool:
        """Simulate or integrate with a real payment gateway."""
        try:
            response = requests.post(
                self.payment_gateway_url,
                json={"user": user, "amount": fiat_amount, "currency": currency},
            )
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Payment gateway error: {e}")
            return False

    def record_transaction(self, user: str, fiat_amount: float, currency: str, qfc_amount: float):
        """Record the transaction for history and analytics."""
        transaction = {
            "user": user,
            "fiat_amount": fiat_amount,
            "currency": currency,
            "qfc_amount": qfc_amount,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.transaction_history.append(transaction)

    def get_transaction_history(self, user: str = None) -> List[Dict]:
        """Retrieve transaction history, optionally filtered by user."""
        if user:
            return [tx for tx in self.transaction_history if tx["user"] == user]
        return self.transaction_history

    def perform_kyc(self, user: str) -> bool:
        """Simulate KYC/AML checks."""
        print(f"Performing KYC for user: {user}")
        # Placeholder for real KYC/AML integration
        # Example: Call an external API like Sumsub or Persona
        return True  # Assume KYC passed
