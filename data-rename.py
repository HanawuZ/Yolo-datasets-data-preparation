import os
import pathlib

# Define root path
# It should be => ..\coco-datasets-data-preparation
root = pathlib.Path(__file__).parent 

# Define datasets directory path
path_datasets = root/"datasets"


def image_rename(src,name):
    """ Function for renaming all images and label files in directory by input name.
    ### Parameters
    - src : source of file directory.
    - name : new name of file.

    
    """
    images_path = src/"images"
    labels_path = src/"labels"
    print(os.listdir(images_path))
    # Iterated all files



    pass

datasets_name = input("Enter datasets directory's name: ")
if datasets_name not in os.listdir():
    print(f"There is no directory name {datasets_name} in {root}")
    pass