import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

class VideoEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Editor")
        
        self.video_path = tk.StringVar()
        self.logo_path = tk.StringVar()
        self.top_banner_color = tk.StringVar(value="77, 106, 0") #BGR  
        self.bottom_banner_color = tk.StringVar(value="77, 106, 0") #BGR
        self.transition_duration = tk.DoubleVar(value=2.0)
        self.top_banner_height = tk.IntVar(value=50)
        self.bottom_banner_height = tk.IntVar(value=50)
        self.logo_size = tk.IntVar(value=50)
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Video Path:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.video_path).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_video).grid(row=0, column=2)
        
        tk.Label(self.root, text="Logo Path:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.logo_path).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_logo).grid(row=1, column=2)
        
        tk.Label(self.root, text="Top Banner Color (R,G,B):").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.top_banner_color).grid(row=2, column=1)
        
        tk.Label(self.root, text="Bottom Banner Color (R,G,B):").grid(row=3, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.bottom_banner_color).grid(row=3, column=1)
        
        tk.Label(self.root, text="Transition Duration (s):").grid(row=4, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.transition_duration).grid(row=4, column=1)
        
        tk.Label(self.root, text="Top Banner Height:").grid(row=5, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.top_banner_height).grid(row=5, column=1)
        
        tk.Label(self.root, text="Bottom Banner Height:").grid(row=6, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.bottom_banner_height).grid(row=6, column=1)
        
        tk.Label(self.root, text="Logo Size:").grid(row=7, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.logo_size).grid(row=7, column=1)
        
        tk.Button(self.root, text="Process Video", command=self.process_video).grid(row=8, column=1)

    def browse_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        self.video_path.set(path)

    def browse_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        self.logo_path.set(path)

    def process_video(self):
        video_path = self.video_path.get()
        logo_path = self.logo_path.get()
        top_banner_color = tuple(map(int, self.top_banner_color.get().split(',')))
        bottom_banner_color = tuple(map(int, self.bottom_banner_color.get().split(',')))
        transition_duration = self.transition_duration.get()
        top_banner_height = self.top_banner_height.get()
        bottom_banner_height = self.bottom_banner_height.get()
        logo_size = (self.logo_size.get(), self.logo_size.get())
        
        clip = VideoFileClip(video_path)
        fps = clip.fps

        total_frames = int(clip.duration * fps)
        fade_frames = int(transition_duration * fps)
        
        output_frames = []
        for i, t in enumerate(np.linspace(0, clip.duration, total_frames)):
            frame = clip.get_frame(t)
            
            # Apply fade-in
            if i < fade_frames:
                alpha = i / fade_frames
                frame = (frame * alpha).astype(np.uint8)
            
            # Apply fade-out
            if i >= total_frames - fade_frames:
                alpha = (total_frames - i) / fade_frames
                frame = (frame * alpha).astype(np.uint8)

            frame = self.add_banners_and_logo(frame, top_banner_height, bottom_banner_height, top_banner_color, bottom_banner_color, logo_path, logo_size)
            output_frames.append(frame)
        
        height, width, _ = output_frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (width, height))

        for frame in output_frames:
            out.write(frame)

        out.release()
        print("Video processing completed.")

    def add_banners_and_logo(self, frame, top_banner_height, bottom_banner_height, top_banner_color, bottom_banner_color, logo_path, logo_size):
        h, w, _ = frame.shape

        # Add top banner
        top_banner = np.zeros((top_banner_height, w, 3), dtype=np.uint8)
        top_banner[:] = top_banner_color
        frame = np.vstack((top_banner, frame))

        # Add bottom banner
        bottom_banner = np.zeros((bottom_banner_height, w, 3), dtype=np.uint8)
        bottom_banner[:] = bottom_banner_color
        frame = np.vstack((frame, bottom_banner))

        # Add logo
        if logo_path:
            logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
            logo = cv2.resize(logo, logo_size)
            logo_h, logo_w, logo_c = logo.shape

            if logo_c == 4:
                # If logo has alpha channel
                alpha_logo = logo[:, :, 3] / 255.0
                alpha_frame = 1.0 - alpha_logo

                for c in range(0, 3):
                    frame[10:10+logo_h, 10:10+logo_w, c] = (alpha_logo * logo[:, :, c] +
                                                            alpha_frame * frame[10:10+logo_h, 10:10+logo_w, c])
            else:
                # If logo does not have alpha channel
                frame[10:10+logo_h, 10:10+logo_w] = logo

        return frame

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorApp(root)
    root.mainloop()