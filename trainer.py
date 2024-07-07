from ultralytics import YOLO
import os

def main():
    model = YOLO("yolov8n.pt")

    dataset="car_front-rear"
    data_config_file=os.path.join("data_config_files", dataset+".yaml")
    
    results = model.train(data=data_config_file, epochs=100, imgsz=640)
    results = model.val()
    results = model.export()

if __name__ == '__main__':
    main()