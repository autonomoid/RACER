from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from moviepy.editor import VideoFileClip
import cv2
import numpy as np
import os
import threading
import imageio

app = Flask(__name__)
socketio = SocketIO(app)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        thread = threading.Thread(target=process_video, args=(filepath,))
        thread.start()
        return jsonify({'status': 'processing'})

@app.route('/preview/<filename>')
def preview_video(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, mimetype='video/mp4')

def process_video(filepath):
    try:
        socketio.emit('status', {'message': 'Processing frames...'})

        clip = VideoFileClip(filepath)
        fps = clip.fps
        duration = clip.duration
        total_frames = int(duration * fps)
        frames = []

        for frame_idx, t in enumerate(np.arange(0, duration, 1/fps)):
            frame = clip.get_frame(t)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = add_banners_and_logo(frame, frame_idx)
            frames.append(frame)
            progress = int((frame_idx / total_frames) * 100)
            socketio.emit('progress', {'progress': progress})

        socketio.emit('status', {'message': 'Saving video...'})

        output_filename = 'output_video.mp4'
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        out = imageio.get_writer(uri=output_path, fps=fps, codec='libx264', format='mp4')

        for frame in frames:
            out.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        out.close()
        socketio.emit('progress', {'progress': 100})
        socketio.emit('status', {'message': 'Processing complete.'})
        socketio.emit('processing_done', {'filename': output_filename})
    except Exception as e:
        socketio.emit('status', {'message': f'Error during processing: {str(e)}'})

def add_banners_and_logo(frame, frame_idx):
    top_banner_height = 50
    bottom_banner_height = 50
    top_banner_color = (77, 106, 0)
    bottom_banner_color = (77, 106, 0)
    logo_path = 'logo.jpg'
    logo_size = (50, 50)

    h, w, _ = frame.shape
    top_banner = np.zeros((top_banner_height, w, 3), dtype=np.uint8)
    top_banner[:] = top_banner_color
    frame = np.vstack((top_banner, frame))

    bottom_banner = np.zeros((bottom_banner_height, w, 3), dtype=np.uint8)
    bottom_banner[:] = bottom_banner_color
    frame = np.vstack((frame, bottom_banner))

    if logo_path:
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        logo = cv2.resize(logo, logo_size)
        logo_h, logo_w, logo_c = logo.shape

        logo_x = 10
        logo_y = 10

        if logo_c == 4:
            alpha_logo = logo[:, :, 3] / 255.0
            alpha_frame = 1.0 - alpha_logo

            for c in range(0, 3):
                frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w, c] = (alpha_logo * logo[:, :, c] +
                                                    alpha_frame * frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w, c])
        else:
            frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w] = logo

    # Add scrolling text
    font_scale = 1
    font_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize("Rootkit Racers", font, font_scale, font_thickness)[0]
    
    # Adjust scrolling speed for preview
    scroll_speed = 5
    horizontal_shift = (scroll_speed * frame_idx) % (w + text_size[0])
   
    text_x = int(w - horizontal_shift)
    text_y = int(h + 1.75 * bottom_banner_height) # Adjust the text position vertically

    cv2.putText(frame, "Rootkit Racers", (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    return frame

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
