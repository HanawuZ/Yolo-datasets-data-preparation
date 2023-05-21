import os
import pathlib
from path import path
from tqdm import tqdm

def datasets_rename(src,name,dir_name):
    """ Function for renaming all images and label files in directory by input name.
    ### Parameters
    - src : source of file directory.
    - name : new name of file.
    - dir_name : ....
    """
    clean_file_count = 0
    error_file_count = 0

    images_path = os.path.join(src,"images")
    labels_path = os.path.join(src,"labels")
    ####################### Optimized Exception #######################
    # Write exception if file now found error then pass this file and continue renaming next file

    # Iterate though all file in folder
    for images_lst, labels_lst in tqdm(zip(enumerate(os.listdir(images_path)), enumerate(os.listdir(labels_path))), desc=name):
        """
        images_lst = (0, 'example_0.png')
        labels_lst = (0, 'example_0.txt')
        """
        try:
            # Get image and label file name.
            img_filename, label_filename, img_index, label_index = images_lst[1], labels_lst[1], images_lst[0], labels_lst[0]
            
            # Assign new names of image and label
            img_dst = f"{name}_{img_index}.jpg"
            label_dst = f"{name}_{label_index}.txt"

            # Get image and label path.
            img_src = os.path.join(images_path,img_filename)
            label_src = os.path.join(labels_path, label_filename)
            
            # Assign renamed image and label destination path
            rename_img_dst = os.path.join(images_path,img_dst)
            rename_label_dst = os.path.join(labels_path,label_dst)

            # Rename file
            os.rename(img_src, rename_img_dst)
            os.rename(label_src, rename_label_dst)

            if (os.path.exists(rename_img_dst)):
                clean_file_count+=1
                
        except (FileNotFoundError):
            error_file_count+=1
            continue

        except (FileExistsError):
            continue

    print(f"{dir_name} files rename completed!!!")
    print(f"Amount of clean file : {clean_file_count}")
    print(f"Amount of error file : {error_file_count}\n")


def main():
    # List all datasets directory
    # Iterate through all datasets
    for dataset_name in os.listdir(path["/datasets"]):

        # Get current dataset path
        target_dataset_path = os.path.join(path["/datasets"], dataset_name)

        for folder_name in ["train", "valid", "test", "export"]:

            # Rename image and label name. If there's no either `train`, `test` or `valid` then continue to next folder.
            try:
                datasets_rename(src=os.path.join(target_dataset_path, folder_name), 
                                name=f"{dataset_name}_{folder_name}",
                                dir_name=folder_name)
            except(FileNotFoundError):
                continue

if __name__=="__main__":
    main()

 

