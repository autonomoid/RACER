from ultralytics import YOLO
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

###########################################################

model_name = "yolov10b"
dataset = "car_front-rear"
input_image_dir = r'datasets\\cars\\test'

###########################################################

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = os.path.join("detection_results", "images", model_name, dataset, f"run_{timestamp}")
os.makedirs(output_dir, exist_ok=True)

# Load the trained YOLO model
trained_model = os.path.join("trained_models", model_name, dataset, "train", "weights", "best.pt")
model = YOLO(trained_model)

# Loop through all images in the input directory
for filename in os.listdir(input_image_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_image_dir, filename)

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
            class_name = results[0].names[int(cls)]
            label = f"{results[0].names[int(cls)]} {conf:.2f}"

            # Filter out low confidence matches
            if conf >= 0.85:

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

        # Save the result to the output directory
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img_bgr)

        print(f"Processed and saved {filename}")

print("Processing complete.")
