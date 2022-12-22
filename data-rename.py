import os
import pathlib

# Define root path
# It should be => ..\Datasets-data-preparation\
ROOT = pathlib.Path(__file__).parent 

# Define datasets directory path
DATASETS_PATH = os.path.join(ROOT,"datasets")


def datasets_rename(src,name="example"):
    """ Function for renaming all images and label files in directory by input name.
    ### Parameters
    - src : source of file directory.
    - name : new name of file.
    """
    images_path = os.path.join(src,"images")
    labels_path = os.path.join(src,"labels")

    
    try:
        # Iterated all images files
        for count, filename in enumerate(os.listdir(images_path)):
            img_dst = f"{name}_{str(count)}.png"
            img_src = f"{images_path}/{filename}"
            rename_img_dst = f"{images_path}/{img_dst}"

            # Rename images file
            os.rename(img_src, rename_img_dst)

        for count, filename in enumerate(os.listdir(labels_path)):
            label_dst = f"{name}_{str(count)}.txt"
            label_src = f"{labels_path}/{filename}"
            rename_label_dst = f"{labels_path}/{label_dst}"

            # Rename images file
            os.rename(label_src, rename_label_dst)
    
    # Declare exception FileNotFoundError. Occur when there's no either 'train', 'test' or 'valid' folder in dataset directory.
    # This exception will break function execution, returning none.
    except (FileNotFoundError):
        return

# Declare target dataset path.
target_dataset_path = os.path.join(DATASETS_PATH,"Crosswalk")

# Iterate through dataset directory if there're subdatasets.
for dataset_dir_name in os.listdir(target_dataset_path):
    
    # Get path of current sub-dataset
    sub_dataset_path = os.path.join(target_dataset_path,dataset_dir_name)

    # Call function datasets_rename to rename all images and labels file name in either folder 'train', 'test' or 'valid'
    # new file names are depend on sub-dataset folder's name.
    # Ex. person-dataset-3, file name will be 'person-dataset-3_train.png', 'person-dataset-3_train.txt'
    for folder_name in ["train", "valid", "test"]:
        datasets_rename(src=os.path.join(sub_dataset_path, folder_name), name=f"{dataset_dir_name}_{folder_name}")
