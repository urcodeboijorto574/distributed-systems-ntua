import os
from flask import Flask
from dotenv import load_dotenv

from models.my_wallet import MyWallet
from models.wallet import Wallet
from models.state import State
from models.node import Node
from models.init_utils import init_bootstrap, init_node

from internal.home import home_bp
from internal.show_state import state_bp

from external.talk_to_bootstrap import talk_to_bootstrap_bp


app = Flask(__name__)

load_dotenv("../config.env")

URL = os.environ.get("URL")
PORT = os.environ.get("PORT")
app.config["bootstrap_addr"] = os.environ.get("BOOTSTRAP_ADDR")                           
app.config["node_num"] = int(os.environ.get("NODE_NUM"))
app.config["is_bootstrap"] = os.environ.get("IS_BOOTSTRAP")
app.config["node_count"] = 0

# Internal Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(state_bp)

# External Blueprints
app.register_blueprint(talk_to_bootstrap_bp)

if __name__ == '__main__':

    if app.config["is_bootstrap"]=="1":
        my_state, my_wallet = init_bootstrap(URL, PORT, app.config["node_num"])
        app.config['my_state'] = my_state
        app.config['my_wallet'] =my_wallet
    else:
        my_state = None
        my_wallet = init_node(URL, PORT, app.config["bootstrap_addr"])
    app.run(debug=True, port=PORT)