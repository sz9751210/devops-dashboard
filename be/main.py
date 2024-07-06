from flask import Flask
from flask_cors import CORS
from app.routes import setup_routes
from config.db import get_db

app = Flask(__name__)
CORS(app)

# set up MongoDB
db = get_db()

# set up routes
setup_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9090)
