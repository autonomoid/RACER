from ultralytics import YOLO
import torch
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained YOLO model
# Replace 'best.pt' with the path to your pre-trained YOLO model weights file
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/your/best.pt', source='local')
model = YOLO(r'runs\\detect\\train13\\weights\\best.pt')

# Prepare the input image
img_path = r'datasets\\cars\\test\\test1.png'  # Replace with the path to your input image
img = Image.open(img_path)

# Run inference
results = model(img_path)

# Run inference
results = model(img_path)

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

# Display the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(img_rgb)
plt.axis('off')
plt.show()
