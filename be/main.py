from flask import Flask
from flask_cors import CORS
from app.routes import setup_routes
from config.config import get_client
import logging

app = Flask(__name__)
CORS(app)

# set up MongoDB
client = get_client()

# set up routes
setup_routes(app, client)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=9090)
