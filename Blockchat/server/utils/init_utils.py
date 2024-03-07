import time
import requests

from models.block import Block
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.wallet import Wallet
from models.state import State
from models.node import Node


def init_bootstrap(url, port, node_num):
    # Create a wallet for the bootsrap
    node_id = 0
    address = url + ":" + port
    my_wallet = MyWallet(node_id, address)
    amount = 1000 * node_num

    new_transaction = my_wallet.create_transaction(
        [0, 0], my_wallet.public_key, "coins", amount, "Genesis transaction"
    )

    # Create genesis_block
    index = 0
    timestamp = time.time()
    transactions = [new_transaction]
    validator = 0
    current_hash = 0  # TODO must use a hash function eg SHA256
    previous_hash = 1
    new_block = Block(
        index, timestamp, transactions, validator, current_hash, previous_hash
    )

    # Initiate the blockchain
    my_blockchain = Blockchain([new_block])

    # Create the State
    my_wallet_for_state = Wallet(node_id, address, my_wallet.public_key, amount)

    # TODO add a stake
    my_state = State(
        my_blockchain, {tuple(my_wallet.public_key): my_wallet_for_state}, node_num
    )

    return my_state, my_wallet


def init_node(url, port, bootstrap):
    # Create a wallet for the bootsrap
    address = url + ":" + port

    my_wallet = MyWallet(None, address)

    # send a request to the bootsrap, giving him your public key and receive your unique node_id
    try:
        payload = {"address": address, "public_key": my_wallet.public_key}

        # send to bootstrap my public key
        response = requests.post(f"http://{bootstrap}/talkToBootstrap", json=payload)
        if response.status_code == 200:
            response_json = response.json()

            # receive from bootstrap my node id
            node_id = response_json.get("id")

            print(f"Request successful. Node ID: {node_id}")
            my_wallet.node_id = node_id

        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")

    return my_wallet
