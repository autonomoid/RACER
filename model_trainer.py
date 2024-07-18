from ultralytics import YOLO
import os

def main():

    ###########################################################

    model_name = "yolov8n"
    #model_name = "yolov10b"

    dataset = "car_front-rear-left-right-top"

    ###########################################################

    model = YOLO(model_name + ".pt")
    project_path = os.path.join("trained_models", model_name, dataset)
    data_config_file=os.path.join("data_config_files", dataset+".yaml") 

    results = model.train(data=data_config_file, epochs=100, imgsz=640, project=project_path)
    results = model.val()
    results = model.export()

if __name__ == '__main__':
    main()