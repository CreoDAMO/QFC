from flask import Flask, request, jsonify
from blockchain.blockchain import Blockchain
from features.nft_marketplace import NFTMarketplace
from features.dex import DecentralizedExchange
from features.liquidity_pool import LiquidityPool
from services.onramp import QFCOnRamper

# Initialize Flask app and modules
app = Flask(__name__)
blockchain = Blockchain(num_shards=4, difficulty=3)
nft_marketplace = NFTMarketplace(blockchain)
dex = DecentralizedExchange()
liquidity_pool = LiquidityPool()
onramp = QFCOnRamper(blockchain)

# Blockchain APIs
@app.route('/blockchain/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transaction = blockchain.add_transaction(Transaction(**data))
    return jsonify({"success": transaction})

@app.route('/blockchain/mine', methods=['POST'])
def mine_block():
    miner_address = request.json.get("miner_address")
    new_block = blockchain.mine_block(miner_address)
    return jsonify({"block_hash": new_block.hash if new_block else "Mining failed"})

# NFT APIs
@app.route('/nft/mint', methods=['POST'])
def mint_nft():
    data = request.json
    success = nft_marketplace.mint_nft(data['token_id'], data['owner'], data['metadata'])
    return jsonify({"success": success})

@app.route('/nft/trade', methods=['POST'])
def trade_nft():
    data = request.json
    success = nft_marketplace.buy_nft(data['token_id'], data['buyer'], data['seller'])
    return jsonify({"success": success})

# DEX APIs
@app.route('/dex/order', methods=['POST'])
def dex_order():
    data = request.json
    dex.place_order(data['user'], data['token_id'], data['amount'], data['price'], data['is_buy'])
    return jsonify({"success": True})

@app.route('/dex/match/<token_id>', methods=['POST'])
def dex_match(token_id):
    dex.match_orders(token_id)
    return jsonify({"success": True})

# Liquidity Pool APIs
@app.route('/lp/add', methods=['POST'])
def add_liquidity():
    data = request.json
    liquidity_pool.add_liquidity(data['user'], data['token_a'], data['token_b'], data['amount_a'], data['amount_b'])
    return jsonify({"success": True})

@app.route('/lp/swap', methods=['POST'])
def swap():
    data = request.json
    output_amount = liquidity_pool.swap(data['user'], data['input_token'], data['output_token'], data['input_amount'])
    return jsonify({"output_amount": output_amount})

# OnRamp APIs
@app.route('/onramp/buy', methods=['POST'])
def buy_qfc():
    data = request.json
    success = onramp.buy_qfc(data['user'], data['amount'], data['currency'])
    return jsonify({"success": success})

if __name__ == '__main__':
    app.run(debug=True)
