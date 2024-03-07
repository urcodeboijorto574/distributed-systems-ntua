import os
from flask import Flask
from dotenv import load_dotenv

from utils.init_utils import init_bootstrap, init_node

from internal.home import home_bp
from internal.show_state import state_bp

from external.talk_to_bootstrap import talk_to_bootstrap_bp
from external.receive_init_from_bootstrap import receive_init_from_bootstap_bp


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
if app.config["is_bootstrap"] == "1":
    app.register_blueprint(talk_to_bootstrap_bp)
else:
    app.register_blueprint(receive_init_from_bootstap_bp)

if __name__ == "__main__":

    if app.config["is_bootstrap"] == "1":
        my_state, my_wallet = init_bootstrap(URL, PORT, app.config["node_num"])
        app.config["my_state"] = my_state
    else:
        app.config["my_state"] = None
        my_wallet = init_node(URL, PORT, app.config["bootstrap_addr"])

    app.config["my_wallet"] = my_wallet

    app.run(debug=False, port=PORT)
