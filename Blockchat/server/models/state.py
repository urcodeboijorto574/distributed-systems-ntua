from models.wallet import Wallet
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.block import Block
from utils.proof_of_stake import proof_of_stake
import time


class State:
    def __init__(
        self,
        blockchain: Blockchain,
        wallets: list[Wallet],
        node_num: int,
        my_wallet: MyWallet,
    ):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = [0] * node_num
        self.current_fees = 0  # total fees corresponding to transactions of one block
        self.test = "state"
        self.my_wallet = my_wallet

    def wallets_serialization(self):
        wallets_list = []
        for wallet in self.wallets:
            wallets_list.append(wallet.to_dict())
        return wallets_list

    def wallets_deserialization(wallets_list):
        wallets = []
        for wallet_data in wallets_list:
            wallets.append(Wallet(**wallet_data))
        return wallets

    def add_transaction(self, transaction: Transaction):
        sender_address = tuple(transaction.sender_address)
        nonce = transaction.nonce
        key = (sender_address, nonce)
        self.blockchain.transaction_inbox[key] = transaction

        # if capacity is full, a new block must be created
        if len(self.blockchain.transaction_inbox) == self.blockchain.capacity:
            seed = self.blockchain.block_list[-1].current_hash
            seed = int(seed, 16)
            validator_id = proof_of_stake(self.stakes, seed)

            # if current node is validator, he mints the new block
            if validator_id == self.my_wallet.node_id:
                minted_block = self.mint_block()
                success = self.broadcast_block(minted_block)
                if success:
                    # add block to blockchain if everyone validated it
                    self.add_block(minted_block)

    def mint_block(self):
        transactions_list = list(self.blockchain.transaction_inbox.values())
        validator_public_key = self.my_wallet.public_key
        new_block = Block(
            # TODO, must fix index
            1,
            time.time(),
            transactions_list,
            validator_public_key,
            self.blockchain.create_block_hash(),
            self.blockchain.block_list[-1].current_hash,
        )
        return new_block

    def broadcast_block(self):
        # TODO
        pass

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def add_block(self, block):
        self.blockchain.add_block(block)

    def add_node(self, node):
        self.nodes.append(node)

    def perform_transaction(self):
        pass

    def validate_transaction(self):
        pass
