from ultralytics import YOLO
import torch
from PIL import Image
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

###########################################################

model_name = "yolov10b"
dataset = "car_front-rear"
#input_video = r'datasets\\raw_data\\videos\\epic_moments.mp4'
input_video = r'datasets\\raw_data\\videos\\2023_London_Highlights.mp4'

confidence_threshold = 0.85

###########################################################

# Load the trained YOLO model
trained_model = os.path.join("trained_models", model_name, dataset, "train", "weights", "best.pt")
model = YOLO(trained_model)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = os.path.join("detection_results", "videos", model_name, dataset, f"run_{timestamp}")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.basename(input_video)
output_path = os.path.join(output_dir, output_file)
output_path = os.path.join(output_dir)

# Open the video file
cap = cv2.VideoCapture(input_video)

# Get video details
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Create VideoWriter object to save processed video
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Process each frame in the video
frame_count = 0
frames_to_process = 10000
while frame_count < frames_to_process:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame)

    # Use the original image from results
    img = results[0].orig_img

    # Convert the image from BGR to RGB (since OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Extract bounding box coordinates, confidence scores, and class labels from results.boxes
    boxes = results[0].boxes

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0]
        cls = box.cls[0]
        class_name = results[0].names[int(cls)]
        label = f"{class_name} {conf:.2f}"

        # Filter out low confidence matches
        if conf >= confidence_threshold:

            if class_name == "car_front":
                bounding_box_color = (0, 0, 255)
            elif class_name == "car_rear":
                bounding_box_color = (255, 0, 0)
            elif class_name == "car_left":
                bounding_box_color = (0, 255, 0)
            elif class_name == "car_right":
                bounding_box_color = (255, 0, 255)
            else:
                bounding_box_color = (255, 255, 255)

            # Draw the bounding box
            cv2.rectangle(img_rgb, (x1, y1), (x2, y2), bounding_box_color, 2)

            # Put the label near the bounding box
            cv2.putText(img_rgb, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Convert back to BGR for saving with OpenCV
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Write the frame to the output video file
    out.write(img_bgr)

    frame_count += 1
    print(f"Processed frame {frame_count}/{total_frames}")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print("Processing complete.")
