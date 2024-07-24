from flask import Flask, request, g
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import setup_routes
from config.config import Config, get_client
from app.services.cronjob_service import CronjobService
import logging
from datetime import datetime
import requests
import pytz

app = Flask(__name__)
CORS(app)

# set up MongoDB
client = get_client()
operation_logs = Config.get_operation_logs_from_db()

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

@app.before_request
def before_request():
    g.start_time = datetime.utcnow()
    g.user = {"username": "admin"}

def get_geo_location(ip):
    # 使用 ip-api.com 查找地理位置
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('city', 'Unknown City')}, {data.get('regionName', 'Unknown Region')}, {data.get('country', 'Unknown Country')}"
        else:
            return "Location Unknown"
    except Exception as e:
        return f"Error: {str(e)}"


@app.after_request
def after_request(response):
    if 'user' in g:
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.remote_addr
        
        location = get_geo_location(ip)
        
        # 轉換 UTC 時間為 Asia/Taipei 時間
        taipei_tz = pytz.timezone('Asia/Taipei')
        timestamp_utc = g.start_time.replace(tzinfo=pytz.utc)
        timestamp_taipei = timestamp_utc.astimezone(taipei_tz)
        timestamp_str = timestamp_taipei.strftime('%Y-%m-%d %H:%M:%S')
        
        log = {
            "username": g.user['username'],  # 假設你有用戶資訊儲存在 g.user 中
            "method": request.method,
            "path": request.path,
            "ip": ip,
            "location": location,
            "timestamp": timestamp_str
        }
        operation_logs.insert_one(log)
    return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=9090)
    scheduler.print_jobs()
