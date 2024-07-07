import os

# Define paths
#text_folder = r'C:\\Users\\auton\\Downloads\\cars\\obj_train_data'
text_folder = r"C:\\Users\\auton\\OneDrive\\Documents\\PycharmProjects\\RACER\\datasets\\car_front-110\\obj_train_data"

image_folder = text_folder

# Function to get the file name without extension
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

# List all text files and check for empty ones
empty_text_files = []
for text_file in os.listdir(text_folder):
    text_file_path = os.path.join(text_folder, text_file)
    if os.path.isfile(text_file_path) and os.path.getsize(text_file_path) == 0:
        empty_text_files.append(get_file_name(text_file))
        # Delete the empty text file
        os.remove(text_file_path)
        print(f'Deleted empty text file: {text_file_path}')

# Delete corresponding image files
for image_file in os.listdir(image_folder):
    image_file_path = os.path.join(image_folder, image_file)
    if os.path.isfile(image_file_path) and get_file_name(image_file) in empty_text_files:
        os.remove(image_file_path)
        print(f'Deleted corresponding image file: {image_file_path}')

print('Deletion process completed.')
