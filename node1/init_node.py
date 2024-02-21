from block import Block
from blockchain import Blockchain
from transaction import Transaction
from my_wallet import MyWallet
import time
import requests

def init_node():
    # Create a wallet for the bootsrap
    public_key = 1  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 1 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    my_wallet = MyWallet(public_key, private_key, amount)

    def receive_id_from_bootstrap():
        url = "http://127.0.0.1"
        port = 3000
        public_key = my_wallet.get_public_key()

        try:
            payload = {
                "public_key": public_key
            }

            # send to bootstrap my public key
            response = requests.post(f"{url}:{port}/talkToBootstrap", json = payload)
            if response.status_code == 200:
                response_json = response.json()

                # receive from bootstrap my node id
                node_id = response_json.get("id")

                if node_id is not None:
                    print(f"Request successful. Node ID: {node_id}")
                else:
                    print("Node ID not found in the response.")
            else:
                print(f"Request failed with status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error making the request: {e}")

    receive_id_from_bootstrap()

if __name__ == '__main__':
    init_node()

