import cv2
import torch
from ultralytics import YOLO
from datetime import datetime

vehicle_labels = ["car", "motorcycle", "bus", "truck", "bicycle"]
model = YOLO("yolov8n.pt")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

def get_congestion_status(total_vehicles):
    if total_vehicles <= 5:
        return "Thông thoáng"
    elif total_vehicles <= 15:
        return "Bình thường"
    elif total_vehicles <= 25:
        return "Đông đúc"
    else:
        return "Kẹt xe"

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

        congestion = get_congestion_status(total)

        data = {
            "camera_id": camera_id,
            "location": location,
            "datetime": datetime.now(),
            "vehicle_count": vehicle_count,
            "total_vehicles": total,
            "congestion_status": congestion  # Thêm tình trạng kẹt xe
        }

        # Gửi lên MongoDB
        collection.insert_one(data)

        print(f"[{camera_id}] {congestion} - {total} xe lúc {data['datetime'].strftime('%H:%M:%S')}")

        cv2.waitKey(2000)

    cap.release()

def detect_video_for_all(video_sources, camera_locations, collection):
    for cam_id, path in video_sources.items():
        location = camera_locations.get(cam_id, "Unknown")
        detect_video(path, cam_id, location, collection)
