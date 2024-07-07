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

        self.root.bind('<Up>', self.load_video)
        self.root.bind('<Right>', self.next_frame)
        self.root.bind('<Left>', self.prev_frame)
        self.root.bind('<Down>', self.save_frame)
        self.root.bind('<Escape>', self.quit)

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
        if self.current_frame:
            save_folder = "saved_frames"
            os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist
            save_path = os.path.join(save_folder, f"frame_{self.current_frame_number}.png")
            try:
                self.current_frame.save(save_path)
                #messagebox.showinfo("Success", f"Frame saved as {save_path}")
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
