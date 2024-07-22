from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import setup_routes
from config.config import get_client
from app.services.cronjob_service import CronjobService
import logging

app = Flask(__name__)
CORS(app)

# set up MongoDB
client = get_client()

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Start the scheduler
scheduler.start()

# set up routes
setup_routes(app, client, scheduler)

@app.before_first_request
def load_jobs():
    cronjob_service = CronjobService(client, scheduler)
    cronjob_service.load_jobs(scheduler)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=9090)
    scheduler.print_jobs()