import os
from bdd100k_config import PATHS, image_name_prefixes
from shutil import move
from tqdm import tqdm

def partition_images():

    # Iterate to get all images.
    for image_name in tqdm(os.listdir(PATHS["/preprocessed_bdd100k/train/images"])):
        
        # Get current image path
        image_path = os.path.join(PATHS["/preprocessed_bdd100k/train/images"],image_name)

        # Get image name prefix
        image_prefix = image_name[0]

        # Iterate all prefix
        for prefix in image_name_prefixes:
            
            # Define current prefixed train directory
            current_image_dir_name = f"train_{prefix}"

            # A path will be like "preprocessed_bdd100k\train_0\images"
            current_image_dir_path = os.path.join(PATHS["/preprocessed_bdd100k/train"],current_image_dir_name,"images")

            # If image's prefix match current prefix
            if image_prefix == prefix:
                
                # Defien image source path
                src_image_path = image_path

                # Define image destination path
                dst_image_path = os.path.join(current_image_dir_path,image_name)
                
                # Move file
                move(src_image_path, dst_image_path)


def partition_labels():

    # Iterate to get all label files.
    for label_name in tqdm(os.listdir(PATHS["/preprocessed_bdd100k/train/labels"])):
        
        # Get current label file path
        label_file_path = os.path.join(PATHS["/preprocessed_bdd100k/train/labels"],label_name)

        # Get label name prefix
        label_prefix = label_name[0]

        # Iterate all prefix
        for prefix in image_name_prefixes:
            
            # Define current prefixed train directory
            current_label_dir_name = f"train_{prefix}"

            # A path will be like "preprocessed_bdd100k\train_0\labels"
            current_label_dir_path = os.path.join(PATHS["/preprocessed_bdd100k/train"],current_label_dir_name,"labels")

            # If current label's prefix match current prefix
            if label_prefix == prefix:
                
                # Defien sources label file path
                src_label_path = label_file_path

                # Define destination label file path
                dst_label_path = os.path.join(current_label_dir_path,label_name)
                
                # Move file
                move(src_label_path, dst_label_path)

def create_partition_folder():
    
    for prefix in image_name_prefixes:

        # Define name of train dataset directory with prefix
        train_dir_name = f"train_{prefix}"

        # Get current train directory path
        train_dir_path = os.path.join(PATHS["/preprocessed_bdd100k/train"],train_dir_name)

        # Create directory
        os.makedirs(train_dir_path)

        # Change current directory
        os.chdir(train_dir_path)

        # Create folders "images" and "labels"
        os.makedirs("images")
        os.makedirs("labels")


def main():
    partition_images()
    # create_partition_folder()

if __name__ == "__main__":
    main()