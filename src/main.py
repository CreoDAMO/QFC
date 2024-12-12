from api.node_api import app

if __name__ == "__main__":
    print("Starting QuantumFuse Blockchain Node-Wallet...")
    app.run(port=5000)
