import os
import shutil
import random

###########################################################

source_video = '2023_London_Highlights' # Where the images originated from.
dataset = 'car_right' # Where the new files will be copied to.

#source_dir = r'C:\\Users\\auton\\Downloads\\task_left_view_dataset_2024_07_13_12_46_03_yolo_1.1\\obj_train_data'
#source_dir = r'C:\\Users\\auton\\Downloads\\task_rear_view_dataset_2024_07_13_15_36_01_yolo_1.1\\obj_train_data'
#source_dir = r'C:\\Users\\auton\\Downloads\\task_top_view_dataset_2024_07_12_14_29_26_yolo_1.1\\obj_train_data'
source_dir = r'C:\\Users\\auton\\Downloads\\task_right_view_dataset_2024_07_13_12_17_51_yolo_1.1\\obj_train_data'


###########################################################

training_dir = os.path.join('datasets', dataset, 'train')
val_dir = os.path.join('datasets', dataset, 'val')

# Define the subdirectories for images and labels
training_images_dir = os.path.join(training_dir, 'images')
training_labels_dir = os.path.join(training_dir, 'labels')
val_images_dir = os.path.join(val_dir, 'images')
val_labels_dir = os.path.join(val_dir, 'labels')

# Create the target directories if they don't exist
os.makedirs(training_images_dir, exist_ok=True)
os.makedirs(training_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Get a list of all the image files and corresponding text files
files = [f for f in os.listdir(source_dir) if f.endswith('.png')]
paired_files = [(f, f.replace('.png', '.txt')) for f in files]

print(f'Image files found: {len(files)}')
print(f'Label files found: {len(paired_files)}')

# Shuffle the list to ensure random distribution
random.shuffle(paired_files)

# Calculate the split index
split_index = int(len(paired_files) * 0.8)

# Split the list into training and validation sets
training_files = paired_files[:split_index]
val_files = paired_files[split_index:]

print(f'Training files: {len(training_files)}')
print(f'Validation files: {len(val_files)}')

# Function to copy files to the target directory with source_video prepended to the file names
def copy_files(file_pairs, image_target_dir, label_target_dir):
    for img_file, txt_file in file_pairs:
        # Prepend the source_video to the file names
        new_img_file = f"{source_video}_{os.path.basename(img_file)}"
        new_txt_file = f"{source_video}_{os.path.basename(txt_file)}"
        
        # Copy the image file
        shutil.copy(os.path.join(source_dir, img_file), os.path.join(image_target_dir, new_img_file))
        # Copy the text file
        shutil.copy(os.path.join(source_dir, txt_file), os.path.join(label_target_dir, new_txt_file))

# Copy the training files
copy_files(training_files, training_images_dir, training_labels_dir)

# Copy the validation files
copy_files(val_files, val_images_dir, val_labels_dir)

print("Files have been successfully copied to the training and validation folders.")
