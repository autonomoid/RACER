from ultralytics import YOLO
import torch
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

###########################################################

model_name = "yolov10b"
dataset = "car_front-rear"
input_image = r'datasets\\cars\\test\\test1.png'

###########################################################

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = os.path.join("detection_results", "images", model_name, dataset, f"run_{timestamp}")
os.makedirs(output_dir, exist_ok=True)

# Load the trained YOLO model
trained_model = os.path.join("trained_models", model_name, dataset, "train", "weights", "best.pt")
model = YOLO(trained_model)

# Prepare the input image
img = Image.open(input_image)

# Run inference
results = model(input_image)

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
    label = f"{results[0].names[int(cls)]} {conf:.2f}"

    # Draw the bounding box
    cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Put the label near the bounding box
    cv2.putText(img_rgb, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Convert back to BGR for saving with OpenCV
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Save the result to the output directory
    output_file = os.path.basename(input_image)
    output_path = os.path.join(output_dir, output_file)
    cv2.imwrite(output_path, img_bgr)

# Display the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(img_rgb)
plt.axis('off')
plt.show()
