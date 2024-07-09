import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

class VideoEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Editor")
        
        # Define custom font
        self.custom_font = tkFont.Font(size=16)
        
        self.video_path = tk.StringVar(value=r"C:\\Users\\auton\\OneDrive\\Documents\\PycharmProjects\\RACER\\detection_results\\videos\\yolov8n\\car_front-rear\\run_20240707_212850\\yolov8n-car_front-rear-2023_London_Highlights.mp4")
        self.logo_path = tk.StringVar(value=r"C:\\Users\\auton\\OneDrive\\Pictures\\autonomoid.jpg")
        self.top_banner_color = tk.StringVar(value="77, 106, 0") #BGR  
        self.bottom_banner_color = tk.StringVar(value="77, 106, 0") #BGR
        self.transition_duration = tk.DoubleVar(value=1.0)
        self.top_banner_height = tk.IntVar(value=50)
        self.bottom_banner_height = tk.IntVar(value=50)
        self.logo_size = tk.IntVar(value=50)
        self.scroll_text = tk.StringVar(value="Scrolling text example")
        self.banner_position = tk.IntVar(value=0)
        self.logo_position_x = tk.IntVar(value=10)
        self.logo_position_y = tk.IntVar(value=10)
        self.scroll_position_y = tk.IntVar(value=10)

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, sticky=tk.N)

        tk.Label(control_frame, text="Video Path:", font=self.custom_font).grid(row=0, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.video_path, font=self.custom_font).grid(row=0, column=1)
        tk.Button(control_frame, text="Browse", command=self.browse_video, font=self.custom_font).grid(row=0, column=2)
        
        tk.Label(control_frame, text="Logo Path:", font=self.custom_font).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.logo_path, font=self.custom_font).grid(row=1, column=1)
        tk.Button(control_frame, text="Browse", command=self.browse_logo, font=self.custom_font).grid(row=1, column=2)
        
        tk.Label(control_frame, text="Top Banner Color (R,G,B):", font=self.custom_font).grid(row=2, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.top_banner_color, font=self.custom_font).grid(row=2, column=1)
        
        tk.Label(control_frame, text="Bottom Banner Color (R,G,B):", font=self.custom_font).grid(row=3, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.bottom_banner_color, font=self.custom_font).grid(row=3, column=1)
        
        tk.Label(control_frame, text="Transition Duration (s):", font=self.custom_font).grid(row=4, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.transition_duration, font=self.custom_font).grid(row=4, column=1)
        
        tk.Label(control_frame, text="Top Banner Height:", font=self.custom_font).grid(row=5, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.top_banner_height, font=self.custom_font).grid(row=5, column=1)
        
        tk.Label(control_frame, text="Bottom Banner Height:", font=self.custom_font).grid(row=6, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.bottom_banner_height, font=self.custom_font).grid(row=6, column=1)
        
        tk.Label(control_frame, text="Logo Size:", font=self.custom_font).grid(row=7, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.logo_size, font=self.custom_font).grid(row=7, column=1)

        tk.Label(control_frame, text="Scrolling Text:", font=self.custom_font).grid(row=8, column=0, sticky=tk.W)
        tk.Entry(control_frame, textvariable=self.scroll_text, font=self.custom_font).grid(row=8, column=1)
        
        tk.Label(control_frame, text="Banner Position:", font=self.custom_font).grid(row=9, column=0, sticky=tk.W)
        ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", variable=self.banner_position, command=self.update_preview).grid(row=9, column=1, sticky=tk.W+tk.E)

        tk.Label(control_frame, text="Logo Position X:", font=self.custom_font).grid(row=10, column=0, sticky=tk.W)
        ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", variable=self.logo_position_x, command=self.update_preview).grid(row=10, column=1, sticky=tk.W+tk.E)
        
        tk.Label(control_frame, text="Logo Position Y:", font=self.custom_font).grid(row=11, column=0, sticky=tk.W)
        ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", variable=self.logo_position_y, command=self.update_preview).grid(row=11, column=1, sticky=tk.W+tk.E)
        
        tk.Label(control_frame, text="Scroll Position Y:", font=self.custom_font).grid(row=12, column=0, sticky=tk.W)
        ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", variable=self.scroll_position_y, command=self.update_preview).grid(row=12, column=1, sticky=tk.W+tk.E)
        
        self.preview_label = tk.Label(self.root)
        self.preview_label.grid(row=0, column=1, rowspan=13, padx=10, pady=10)
        
        tk.Button(control_frame, text="Process Video", command=self.process_video, font=self.custom_font).grid(row=13, column=1)

    def browse_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        self.video_path.set(path)
        self.update_preview()

    def browse_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        self.logo_path.set(path)
        self.update_preview()

    def update_preview(self, event=None):
        if not self.video_path.get():
            return
        
        clip = VideoFileClip(self.video_path.get())
        frame = clip.get_frame(0)  # Get the first frame for preview
        
        frame = self.add_banners_and_logo(
            frame, 
            self.top_banner_height.get(), 
            self.bottom_banner_height.get(), 
            tuple(map(int, self.top_banner_color.get().split(','))), 
            tuple(map(int, self.bottom_banner_color.get().split(','))), 
            self.logo_path.get(), 
            (self.logo_size.get(), self.logo_size.get()), 
            self.scroll_text.get(), 
            0, 
            1  # Pass 1 to avoid scrolling in preview
        )
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.preview_label.imgtk = imgtk
        self.preview_label.config(image=imgtk)

    def process_video(self):
        video_path = self.video_path.get()
        logo_path = self.logo_path.get()
        top_banner_color = tuple(map(int, self.top_banner_color.get().split(',')))
        bottom_banner_color = tuple(map(int, self.bottom_banner_color.get().split(',')))
        transition_duration = self.transition_duration.get()
        top_banner_height = self.top_banner_height.get()
        bottom_banner_height = self.bottom_banner_height.get()
        logo_size = (self.logo_size.get(), self.logo_size.get())
        scroll_text = self.scroll_text.get()
        
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

            frame = self.add_banners_and_logo(
                frame, 
                top_banner_height, 
                bottom_banner_height, 
                top_banner_color, 
                bottom_banner_color, 
                logo_path, 
                logo_size, 
                scroll_text, 
                i, 
                total_frames
            )
            output_frames.append(frame)
        
        height, width, _ = output_frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (width, height))

        for frame in output_frames:
            out.write(frame)

        out.release()
        print("Video processing completed.")

    def add_banners_and_logo(self, frame, top_banner_height, bottom_banner_height, top_banner_color, bottom_banner_color, logo_path, logo_size, scroll_text, frame_idx, total_frames):
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

            logo_x = int(self.logo_position_x.get() / 100 * w)
            logo_y = int(self.logo_position_y.get() / 100 * h)

            if logo_c == 4:
                # If logo has alpha channel
                alpha_logo = logo[:, :, 3] / 255.0
                alpha_frame = 1.0 - alpha_logo

                for c in range(0, 3):
                    frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w, c] = (alpha_logo * logo[:, :, c] +
                                                            alpha_frame * frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w, c])
            else:
                # If logo does not have alpha channel
                frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w] = logo

        # Add scrolling text
        font_scale = 1
        font_thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(scroll_text, font, font_scale, font_thickness)[0]
        text_x = w - (frame_idx % (w + text_size[0]))
        text_y = h + bottom_banner_height - int(self.scroll_position_y.get() / 100 * bottom_banner_height)  # Adjust the text position vertically

        cv2.putText(frame, scroll_text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

        return frame

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorApp(root)
    root.mainloop()