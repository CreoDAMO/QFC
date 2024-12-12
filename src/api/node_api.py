from flask import Flask, request, jsonify
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from services.onramp import QFCOnRamp

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
onramp = QFCOnRamp(blockchain)

@app.route('/balance', methods=['GET'])
def get_balance():
    address = wallet.get_address()
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance})

@app.route('/transaction', methods=['POST'])
def send_transaction():
    data = request.json
    try:
        tx = wallet.create_transaction(data['recipient'], data['amount'], blockchain)
        blockchain.add_transaction(tx)
        return jsonify({"message": "Transaction added!"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block(wallet.get_address())
    return jsonify({"block_hash": block.hash})

@app.route('/buy_qfc', methods=['POST'])
def buy_qfc():
    data = request.json
    response = onramp.buy_qfc(wallet.get_address(), data['fiat_amount'], data['fiat_currency'])
    return jsonify({"message": response})
