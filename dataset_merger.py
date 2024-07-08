import os
import shutil

# Define the source directories
source_dirs = [
    os.path.join('datasets', 'car_front'),
    os.path.join('datasets', 'car_rear'),
    os.path.join('datasets', 'car_left')
]

# Define the target directory
target_dir = os.path.join('datasets', 'car_front-rear-left')

# Define the subfolders to be merged
subfolders = [
    os.path.join('train', 'images'),
    os.path.join('train', 'labels'),
    os.path.join('val', 'images'),
    os.path.join('val', 'labels'),
    os.path.join('test', 'images'),
    os.path.join('test', 'labels'),
]

# Create the target subfolders if they don't exist
for subfolder in subfolders:
    os.makedirs(os.path.join(target_dir, subfolder), exist_ok=True)

# Function to merge contents of source subfolders into the target subfolder
def merge_subfolders(source_dirs, target_dir, subfolder):
    target_subfolder = os.path.join(target_dir, subfolder)
    for source_dir in source_dirs:
        source_subfolder = os.path.join(source_dir, subfolder)
        for filename in os.listdir(source_subfolder):
            source_file = os.path.join(source_subfolder, filename)
            target_file = os.path.join(target_subfolder, filename)
            shutil.copy(source_file, target_file)

# Merge each subfolder
for subfolder in subfolders:
    merge_subfolders(source_dirs, target_dir, subfolder)

print('Merging completed successfully.')