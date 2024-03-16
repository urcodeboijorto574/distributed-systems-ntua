from flask import Blueprint, request, jsonify, current_app

from models.blockchain import Blockchain
from models.transaction import Transaction
from models.state import State
import traceback

receive_init_from_bootstap_bp = Blueprint("receiveInitFromBootstrap", __name__)


# bootstrap sends to every new inserted node the blockchain and all the wallets. The node must validate the blockchain
@receive_init_from_bootstap_bp.route("/receiveInitFromBootstrap", methods=["POST"])
def receive_init_from_bootstap():
    node_num = current_app.config["node_num"]
    my_wallet = current_app.config["my_wallet"]

    try:

        data = request.json

        blockchain = Blockchain.from_dict(data["blockchain"], capacity=node_num)
        wallets = State.wallets_deserialization(data["wallets"])
        transactions = data["blockchain"]["transactions"]
        state = State(blockchain, wallets, node_num, my_wallet)

        for transaction in transactions:
            state.add_transaction(Transaction.from_dict(transaction))

        breakpoint()
        current_app.config["my_state"] = state

        response_data = {"status": "success"}
        response = jsonify(response_data)

        print("Blockchat initalization succesfull - all nodes online.")

        return response, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
