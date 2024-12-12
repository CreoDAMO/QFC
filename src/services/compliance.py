import re
from typing import List


class Compliance:
    def __init__(self):
        self.kyc_approved_users = set()  # Store KYC-approved user IDs

    def perform_kyc(self, user_id: str, documents: List[str]) -> bool:
        # Simulate KYC approval process
        if len(documents) > 0 and all(isinstance(doc, str) for doc in documents):
            self.kyc_approved_users.add(user_id)
            print(f"KYC Approved for user: {user_id}")
            return True
        print(f"KYC Failed for user: {user_id}")
        return False

    def aml_check(self, transaction_details: dict) -> bool:
        # Example AML rule: disallow transactions with suspicious patterns
        suspicious_keywords = ["terrorism", "laundering", "fraud"]
        description = transaction_details.get("description", "").lower()
        for keyword in suspicious_keywords:
            if keyword in description:
                print(f"AML Alert: Suspicious transaction detected - {description}")
                return False
        return True

    def validate_address(self, address: str) -> bool:
        # Example: Validate Ethereum-like addresses
        return bool(re.match(r"^0x[a-fA-F0-9]{40}$", address))
