from flask import Blueprint, request, jsonify, current_app
from utils.broadcast import broadcast

from models.transaction import Transaction

send_transaction_bp = Blueprint("send_transaction", __name__)


@send_transaction_bp.route("/send_transaction", methods=["POST"])
def send_transaction():
    my_state = current_app.config["my_state"]

    data = request.json
    type = data["type"]
    body = data["body"]
    recipient_id = int(data["recipient_id"])
    recipient_public_key = my_state.wallets[recipient_id].public_key

    if type == "message":
        amount = 0
        message = body
    else:
        amount = int(body)
        message = ""

    new_transaction = my_state.my_wallet.create_transaction(
        my_state.my_wallet.public_key, recipient_public_key, type, amount, message
    )

    validated = my_state.validate_transaction(new_transaction)

    if validated:
        success = broadcast(
            "validateTransaction",
            {"transaction": new_transaction.to_dict()},
            my_state.wallets,
            my_state.my_wallet.address,
        )
        if success:
            my_state.add_transaction(new_transaction)
        else:
            broadcast(
                "revokeTransaction",
                {"transaction": new_transaction.to_dict()},
                my_state.wallets,
                my_state.my_wallet.address,
            )

    return "Transaction broadcasted to all nodes"
