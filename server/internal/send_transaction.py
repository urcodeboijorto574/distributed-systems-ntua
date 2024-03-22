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
        my_state.my_wallet.public_key,
        recipient_public_key,
        type,
        amount,
        message,
        my_state.get_my_nonce(),
    )

    validated = my_state.validate_transaction(new_transaction)

    if validated:
        success = broadcast(
            "validateTransaction",
            {"transaction": new_transaction.to_dict()},
            my_state.wallets,
            my_state.my_wallet.node_address,
        )
        # breakpoint()
        # a transaction is added only if all nodes know that is has been validated from everyone
        if success:
            transaction_key = my_state.transaction_unique_id(new_transaction)
            broadcast(
                "addTransaction",
                {"transaction_key": list(transaction_key)},
                my_state.wallets,
                my_state.my_wallet.node_address,
            )
            my_state.add_transaction(transaction_key)
            return "Transaction validated from all nodes"
        # else:
        #     broadcast(
        #         "revokeTransaction",
        #         {"transaction": new_transaction.to_dict()},
        #         my_state.wallets,
        #         my_state.my_wallet.address,
        #     )
        #     return "Transaction broadcasted but then was revoked"
    else:
        return "Transaction was not valid and was not broadcasted"
