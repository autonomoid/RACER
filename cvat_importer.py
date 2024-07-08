import os
import shutil
import random

###########################################################

dataset = 'car_left'
source_dir = r'C:\\Users\\auton\\Downloads\\car_left\\obj_train_data'

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

# Function to copy files to the target directory
def copy_files(file_pairs, image_target_dir, label_target_dir):
    for img_file, txt_file in file_pairs:
        # Copy the image file
        shutil.copy(os.path.join(source_dir, img_file), os.path.join(image_target_dir, img_file))
        # Copy the text file
        shutil.copy(os.path.join(source_dir, txt_file), os.path.join(label_target_dir, txt_file))

# Copy the training files
copy_files(training_files, training_images_dir, training_labels_dir)

# Copy the validation files
copy_files(val_files, val_images_dir, val_labels_dir)

print("Files have been successfully copied to the training and validation folders.")
