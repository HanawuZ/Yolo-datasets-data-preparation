import os
import pathlib

# Define root path
# It should be => ..\coco-datasets-data-preparation
root = pathlib.Path(__file__).parent 

# Define datasets directory path
path_datasets = root/"datasets"


def datasets_rename(src,name="example"):
    """ Function for renaming all images and label files in directory by input name.
    ### Parameters
    - src : source of file directory.
    - name : new name of file.

    
    """
    images_path = src/"images"
    labels_path = src/"labels"

    # Iterated all images files
    for count, filename in enumerate(os.listdir(images_path)):
        img_dst = f"{name}_{str(count)}.png"
        img_src = f"{images_path}/{filename}"
        rename_img_dst = f"{images_path}/{img_dst}"

        # Rename images file
        os.rename(img_src, rename_img_dst)


while True:
    datasets_name = input("Enter datasets directory's name: ")
    if datasets_name not in os.listdir(path_datasets):
        print(f"There is no directory name {datasets_name} in {root}")
    else :
        datasets_rename(path_datasets/datasets_name)
        break