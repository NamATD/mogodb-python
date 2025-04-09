from flask import Flask, jsonify
from services.mongo_service import get_latest_data
from services.data_analysis import get_weekly_stats
from detect.yolo_detector import detect_video_for_all
from config import MONGO_URI, VIDEO_SOURCES, CAMERA_LOCATIONS
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client['traffic_db']
collection = db['traffic_data']

@app.route("/api/live")
def api_live():
    return jsonify(get_latest_data(collection))

@app.route("/api/stats")
def api_stats():
    return jsonify(get_weekly_stats(collection))

@app.route("/run-detection")
def run_detection():
    detect_video_for_all(VIDEO_SOURCES, CAMERA_LOCATIONS, collection)
    return jsonify({"message": "Detection started!"})

if __name__ == '__main__':
    app.run(debug=True)
