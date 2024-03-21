import os

def rename_files(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            
            # Check if the folder has 'images' and 'labels' subfolders
            if 'images' in os.listdir(folder_path) and 'labels' in os.listdir(folder_path):
                image_folder = os.path.join(folder_path, 'images')
                label_folder = os.path.join(folder_path, 'labels')
                
                # Get the list of image and label files
                image_files = os.listdir(image_folder)
                label_files = os.listdir(label_folder)
                
                # Pair and rename image and text files
                for i, (image_file, label_file) in enumerate(zip(image_files, label_files), 1):
                    print(image_file, label_file)
                    # # Generate new name
                    # new_name = f'{root}_{folder}_{i}'
                    
                    # # Get absolute paths
                    # image_src = os.path.join(image_folder, image_file)
                    # label_src = os.path.join(label_folder, label_file)
                    
                    # # Extract file extensions
                    # image_ext = os.path.splitext(image_file)[1]
                    # label_ext = os.path.splitext(label_file)[1]
                    
                    # # Construct new absolute paths
                    # image_dst = os.path.join(image_folder, f'{new_name}{image_ext}')
                    # label_dst = os.path.join(label_folder, f'{new_name}{label_ext}')
                    
                    # # Rename image file
                    # os.rename(image_src, image_dst)
                    
                    # # Rename label file
                    # os.rename(label_src, label_dst)

if __name__ == "__main__":
    root_folder = r'datasets\Elephants_14.v1-v20.yolov7pytorch'  # Replace with the actual root folder name
    rename_files(os.path.abspath(root_folder))
