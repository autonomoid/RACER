from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from moviepy.editor import VideoFileClip
import cv2
import numpy as np
import os
import threading
import imageio
import logging
import json
import base64

app = Flask(__name__)
socketio = SocketIO(app)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
SETTINGS_FOLDER = 'settings'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['SETTINGS_FOLDER'] = SETTINGS_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

if not os.path.exists(SETTINGS_FOLDER):
    os.makedirs(SETTINGS_FOLDER)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

@app.route('/')
def index():
    logging.info(f'Function: {index.__name__} at line {index.__code__.co_firstlineno}')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info(f'Function: {upload_file.__name__} at line {upload_file.__code__.co_firstlineno}')
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

@app.route('/settings', methods=['POST'])
def update_settings():
    logging.info(f'Function: {update_settings.__name__} at line {update_settings.__code__.co_firstlineno}')
    save_settings(request.form, request.files)
    return jsonify({'status': 'success'})

@app.route('/preview', methods=['POST'])
def generate_preview():
    logging.info(f'Function: {generate_preview.__name__} at line {generate_preview.__code__.co_firstlineno}')
    save_settings(request.form, request.files)
    settings = load_settings()

    # Use the first frame of the first video in the upload folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return jsonify({'status': 'error', 'message': 'No uploaded videos found'})
    first_video = os.path.join(app.config['UPLOAD_FOLDER'], files[0])
    clip = VideoFileClip(first_video)
    frame = clip.get_frame(0)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = add_banners_and_logo(frame, 0, settings)
    _, buffer = cv2.imencode('.jpg', frame)
    preview_image = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'status': 'success', 'image': preview_image})

@app.route('/preview/<filename>')
def preview_video(filename):
    logging.info(f'Function: {preview_video.__name__} at line {preview_video.__code__.co_firstlineno}')
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, mimetype='video/mp4')

def save_settings(form, files):
    settings = {
        'logo_x': form.get('logoX', default=10, type=int),
        'logo_y': form.get('logoY', default=10, type=int),
        'top_banner_color': form.get('topBannerColor', default='#006a4d'),
        'bottom_banner_color': form.get('bottomBannerColor', default='#006a4d'),
        'scrolling_text': form.get('scrollingText', default='Rootkit Racers'),
    }
    logo_file = files.get('logoFile')
    if logo_file:
        logo_filepath = os.path.join(app.config['SETTINGS_FOLDER'], 'logo.jpg')
        logo_file.save(logo_filepath)
        settings['logo_path'] = logo_filepath
    settings_path = os.path.join(app.config['SETTINGS_FOLDER'], 'settings.json')
    with open(settings_path, 'w') as f:
        json.dump(settings, f)

def load_settings():
    settings_path = os.path.join(app.config['SETTINGS_FOLDER'], 'settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    else:
        settings = {
            'logo_x': 10,
            'logo_y': 10,
            'top_banner_color': '#006a4d',
            'bottom_banner_color': '#006a4d',
            'logo_path': 'logo.jpg',
            'scrolling_text': 'Rootkit Racers'
        }
    return settings

def process_video(filepath):
    logging.info(f'Function: {process_video.__name__} at line {process_video.__code__.co_firstlineno}')
    try:
        socketio.emit('status', {'message': 'Processing frames...'})

        clip = VideoFileClip(filepath)
        fps = clip.fps
        duration = clip.duration
        total_frames = int(duration * fps)
        frames = []

        settings = load_settings()

        for frame_idx, t in enumerate(np.arange(0, duration, 1/fps)):
            frame = clip.get_frame(t)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = add_banners_and_logo(frame, frame_idx, settings)
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
        logging.error(f'Error during processing: {str(e)} at line {process_video.__code__.co_firstlineno + e.__traceback__.tb_lineno}')
        socketio.emit('status', {'message': f'Error during processing: {str(e)}'})


def hex_to_bgr(hex_color):
    # Remove the '#' character if present
    hex_color = hex_color.lstrip('#')
    
    # Extract RGB components
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Return BGR tuple
    return (b, g, r)

def add_banners_and_logo(frame, frame_idx, settings):
    logging.info(f'Function: {add_banners_and_logo.__name__} at line {add_banners_and_logo.__code__.co_firstlineno}')
    top_banner_height = 50
    bottom_banner_height = 50

    top_banner_color = hex_to_bgr(settings['top_banner_color'])
    bottom_banner_color = hex_to_bgr(settings['bottom_banner_color'])

    logo_path = settings.get('logo_path', 'logo.jpg')
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

        logo_x = settings.get('logo_x', 10)
        logo_y = settings.get('logo_y', 10)

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
    text_size = cv2.getTextSize(settings.get('scrolling_text', 'Rootkit Racers'), font, font_scale, font_thickness)[0]

    # Adjust scrolling speed for preview
    scroll_speed = 5
    horizontal_shift = (scroll_speed * frame_idx) % (w + text_size[0])

    text_x = int(w - horizontal_shift)
    text_y = int(h + 1.75 * bottom_banner_height) # Adjust the text position vertically

    cv2.putText(frame, settings.get('scrolling_text', 'Rootkit Racers'), (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    return frame

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
