import os
from ultralytics import YOLO

def evaluate_model(weights, data_config, img_size=640, conf_thres=0.25, iou_thres=0.45):
    model = YOLO(weights)
    results = model.val(data=data_config, imgsz=img_size, conf=conf_thres, iou=iou_thres)
    return results

def main(models_dir, dataset, img_size=640, conf_thres=0.25, iou_thres=0.45):
    models = [os.path.join(models_dir, f, dataset, "train", "weights", "best.pt") for f in os.listdir(models_dir)]
    results_list = []

    data_config = os.path.join("data_config_files", dataset + ".yaml")
    for model in models:
        print(f"Evaluating model: {model}")
        results = evaluate_model(model, data_config, img_size, conf_thres, iou_thres)
        results_list.append((model, results))
    
    # Extract and print relevant metrics
    print("\nModel Evaluation Results:")
    for model, results in results_list:
        # Add debug information to understand the structure of results
        print(f"Results object structure for model {model}: {dir(results)}")

        # Attempt to extract known metrics
        try:
            map50_95 = results.box.map50_95
            map50 = results.box.map50
            precision = results.box.precision
            recall = results.box.recall
        except AttributeError:
            print(f"Error accessing metrics for model {model}.")
            map50_95, map50, precision, recall = 'N/A', 'N/A', 'N/A', 'N/A'

        # Check if the metrics are numeric before formatting
        if isinstance(map50_95, (int, float)):
            map50_95_str = f"{map50_95:.4f}"
        else:
            map50_95_str = map50_95
        
        if isinstance(map50, (int, float)):
            map50_str = f"{map50:.4f}"
        else:
            map50_str = map50
        
        if isinstance(precision, (int, float)):
            precision_str = f"{precision:.4f}"
        else:
            precision_str = precision
        
        if isinstance(recall, (int, float)):
            recall_str = f"{recall:.4f}"
        else:
            recall_str = recall

        print(f"Model: {model}")
        print(f"mAP_50-95: {map50_95_str}")
        print(f"mAP_50: {map50_str}")
        print(f"Precision: {precision_str}")
        print(f"Recall: {recall_str}")
        print("-" * 30)

    # Sort results based on mAP_50-95
    results_list.sort(key=lambda x: x[1].box.map50_95 if hasattr(x[1].box, 'map50_95') else 0, reverse=True)
    
    best_model = results_list[0][0]
    if hasattr(results_list[0][1].box, 'map50_95'):
        best_map50_95 = f"{results_list[0][1].box.map50_95:.4f}"
    else:
        best_map50_95 = 'N/A'
    print(f"\nBest Model: {best_model} with mAP_50-95: {best_map50_95}")



if __name__ == "__main__":
    models_dir = 'trained_models'  # Directory containing your trained models
    dataset = 'car_front-rear'  # Path to your dataset configuration file
    main(models_dir, dataset)
