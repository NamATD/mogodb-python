import cv2
import torch
from ultralytics import YOLO
from datetime import datetime

vehicle_labels = ["car", "motorcycle", "bus", "truck", "bicycle"]
model = YOLO("yolov8n.pt")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

def detect_video(video_path, camera_id, location, collection):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (960, 540))
        results = model(frame, conf=0.3, verbose=False)[0]

        vehicle_count = {label: 0 for label in vehicle_labels}
        total = 0
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label in vehicle_labels:
                vehicle_count[label] += 1
                total += 1

        data = {
            "camera_id": camera_id,
            "location": location,
            "datetime": datetime.now(),
            "vehicle_count": vehicle_count,
            "total_vehicles": total
        }
        collection.insert_one(data)
        cv2.waitKey(2000)
    cap.release()

def detect_video_for_all(video_sources, camera_locations, collection):
    for cam_id, path in video_sources.items():
        location = camera_locations.get(cam_id, "Unknown")
        detect_video(path, cam_id, location, collection)
