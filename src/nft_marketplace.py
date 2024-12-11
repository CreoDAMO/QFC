from typing import Dict, Any, List

class NFTMarketplace:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.nfts: Dict[str, Dict] = {}
        self.collections: Dict[str, Dict] = {}

    # NFT Minting
    def mint_nft(self, token_id: str, owner: str, metadata: Dict[str, Any]) -> bool:
        if token_id not in self.nfts:
            self.nfts[token_id] = {
                "owner": owner,
                "metadata": metadata,
                "fractions": {owner: 1.0},  # Default 100% ownership
                "royalty_percentage": 0,
                "royalty_recipient": owner,
            }
            return True
        return False

    # Transfer Ownership
    def transfer_nft(self, token_id: str, from_address: str, to_address: str) -> bool:
        if token_id in self.nfts and self.nfts[token_id]["owner"] == from_address:
            self.nfts[token_id]["owner"] = to_address
            return True
        return False

    # Royalties
    def set_royalties(self, token_id: str, percentage: float, recipient: str) -> bool:
        if token_id in self.nfts:
            self.nfts[token_id]["royalty_percentage"] = percentage
            self.nfts[token_id]["royalty_recipient"] = recipient
            return True
        return False

    # Fractional Ownership
    def fractionalize_nft(self, token_id: str, fractions: Dict[str, float]) -> bool:
        if token_id in self.nfts and sum(fractions.values()) == 1.0:
            self.nfts[token_id]["fractions"] = fractions
            return True
        return False

    # Collections
    def create_collection(self, collection_id: str, owner: str) -> bool:
        if collection_id not in self.collections:
            self.collections[collection_id] = {"owner": owner, "nfts": []}
            return True
        return False

    def add_nft_to_collection(self, token_id: str, collection_id: str) -> bool:
        if token_id in self.nfts and collection_id in self.collections:
            self.collections[collection_id]["nfts"].append(token_id)
            return True
        return False

    # List NFTs for Trade
    def list_nft_for_sale(self, token_id: str, price: float) -> bool:
        if token_id in self.nfts and "sale_price" not in self.nfts[token_id]:
            self.nfts[token_id]["sale_price"] = price
            return True
        return False

    def buy_nft(self, token_id: str, buyer: str, seller: str) -> bool:
        if token_id in self.nfts and self.nfts[token_id].get("sale_price"):
            price = self.nfts[token_id]["sale_price"]

            # Ensure the buyer has enough balance
            if self.blockchain.get_qfc_balance(buyer) >= price:
                # Transfer funds and NFT
                self.blockchain.assets["QFC"]["balances"][buyer] -= price
                self.blockchain.assets["QFC"]["balances"][seller] += price
                self.transfer_nft(token_id, seller, buyer)

                # Handle royalties
                royalty_percentage = self.nfts[token_id]["royalty_percentage"]
                royalty_recipient = self.nfts[token_id]["royalty_recipient"]
                if royalty_percentage > 0:
                    royalty_amount = price * (royalty_percentage / 100)
                    self.blockchain.assets["QFC"]["balances"][seller] -= royalty_amount
                    self.blockchain.assets["QFC"]["balances"][royalty_recipient] += royalty_amount

                # Remove sale listing
                del self.nfts[token_id]["sale_price"]
                return True
        return False
