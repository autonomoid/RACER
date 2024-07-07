import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button
from PIL import Image, ImageTk

class VideoFrameExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Extractor")

        self.video_path = None
        self.cap = None
        self.total_frames = 0
        self.current_frame_number = 0
        self.current_frame = None

        # Widgets
        self.label_info = Label(self.root, text="Select a video file.")
        self.label_info.pack(pady=10)

        # Frame to hold the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.btn_load_video = Button(self.button_frame, text="Load Video", command=self.load_video)
        self.btn_load_video.pack(side=tk.LEFT, pady=5)

        self.btn_prev_frame = Button(self.button_frame, text="Previous Frame", command=self.prev_frame)
        self.btn_prev_frame.pack(side=tk.LEFT, padx=5)

        self.btn_next_frame = Button(self.button_frame, text="Next Frame", command=self.next_frame)
        self.btn_next_frame.pack(side=tk.LEFT, padx=5)
        
        self.btn_save_frame = Button(self.button_frame, text="Save Frame", command=self.save_frame)
        self.btn_save_frame.pack(side=tk.LEFT, padx=5)

        self.label_frame = Label(self.root)
        self.label_frame.pack()

        # Labels to display file counts 
        self.label_front_view_count = Label(self.root, text="Front View: 0")
        self.label_front_view_count.pack(pady=5)

        self.label_rear_view_count = Label(self.root, text="Rear View: 0")
        self.label_rear_view_count.pack(pady=5)

        self.label_left_view_count = Label(self.root, text="Left View: 0")
        self.label_left_view_count.pack(pady=5)

        self.label_right_view_count = Label(self.root, text="Right View: 0")
        self.label_right_view_count.pack(pady=5)

        self.label_top_view_count = Label(self.root, text="Top View: 0")
        self.label_top_view_count.pack()

        self.root.bind('<Up>', self.load_video)
        self.root.bind('<Right>', self.next_frame)
        self.root.bind('<Left>', self.prev_frame)
        self.root.bind('<Down>', self.save_frame)
        self.root.bind('<Escape>', self.quit)        

        self.root.bind('4', self.save_left_view)
        self.root.bind('6', self.save_right_view)
        self.root.bind('8', self.save_rear_view)
        self.root.bind('2', self.save_front_view)
        self.root.bind('5', self.save_top_view)

        # Update file counts initially
        self.update_file_counts()

    def update_file_counts(self):
        front_view_count = len(os.listdir("extracted_frames/front_view"))
        self.label_front_view_count.config(text=f"Front View: {front_view_count}")

        rear_view_count = len(os.listdir("extracted_frames/rear_view"))
        self.label_rear_view_count.config(text=f"Rear View: {rear_view_count}")

        left_view_count = len(os.listdir("extracted_frames/left_view"))
        self.label_left_view_count.config(text=f"Left View: {left_view_count}")

        right_view_count = len(os.listdir("extracted_frames/right_view"))
        self.label_right_view_count.config(text=f"Right View: {right_view_count}")

        top_view_count = len(os.listdir("extracted_frames/top_view"))
        self.label_top_view_count.config(text=f"Top View: {top_view_count}")

    def load_video(self, event=None):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.update_frame_display()

    def update_frame_display(self):
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_number)
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame = Image.fromarray(frame)
                self.current_frame.thumbnail((800, 600))
                imgtk = ImageTk.PhotoImage(image=self.current_frame)
                self.label_frame.imgtk = imgtk
                self.label_frame.config(image=imgtk)
            else:
                messagebox.showerror("Error", "Failed to read frame.")
        else:
            messagebox.showerror("Error", "Video capture is not open.")

    def next_frame(self, event=None):
        if self.cap:
            self.current_frame_number += 1
            if self.current_frame_number >= self.total_frames:
                self.current_frame_number = 0
            self.update_frame_display()

    def prev_frame(self, event=None):
        if self.cap:
            self.current_frame_number -= 1
            if self.current_frame_number < 0:
                self.current_frame_number = self.total_frames - 1
            self.update_frame_display()

    def save_frame(self, event=None):
        self.save_frame_to_folder("extracted_frames/mixed")

    def save_front_view(self, event=None):
        self.save_frame_to_folder("extracted_frames/front_view")

    def save_rear_view(self, event=None):
        self.save_frame_to_folder("extracted_frames/rear_view")

    def save_left_view(self, event=None):
        self.save_frame_to_folder("extracted_frames/left_view")

    def save_right_view(self, event=None):
        self.save_frame_to_folder("extracted_frames/right_view")

    def save_top_view(self, event=None):
        self.save_frame_to_folder("extracted_frames/top_view")

    def save_frame_to_folder(self, folder_name):
        if self.current_frame:
            os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
            save_path = os.path.join(folder_name, f"frame_{self.current_frame_number}.png")
            try:
                self.current_frame.save(save_path)
                self.update_file_counts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save frame: {str(e)}")
        else:
            messagebox.showerror("Error", "No frame to save.")

    def quit(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameExtractorApp(root)
    root.mainloop()
