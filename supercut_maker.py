import cv2
from datetime import datetime

def timestamp_to_seconds(timestamp):
    time_obj = datetime.strptime(timestamp, "%H:%M:%S")
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

def create_supercut(input_video, output_filename, start_times, clip_length):
    # Open the input video
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the frames per second (fps) of the input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create the VideoWriter object for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    
    # Process each start time
    for clip_num, clip_midpoint in enumerate(start_times):
        print(f"Processing clip {clip_num + 1}...")
        
        clip_midpoint = timestamp_to_seconds(clip_midpoint)
        start_seconds = clip_midpoint - clip_length/2.0
        end_seconds = clip_midpoint + clip_length/2.0
        
        cap.set(cv2.CAP_PROP_POS_MSEC, start_seconds * 1000)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if current_time > end_seconds:
                break

            out.write(frame)

    # Release everything when the job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Supercut created successfully.")

if __name__ == '__main__':
    input_video = "input_video.mp4"
    output_filename = "supercut.mp4"

    clip_midpoints = [
        "00:10:00",
        "00:20:00",
        "00:30:00",
        "00:40:00",
        "00:50:00",
    ]

    clip_length = 4 # Duration of each clip in seconds

    create_supercut(input_video, output_filename, clip_midpoints, clip_length)
