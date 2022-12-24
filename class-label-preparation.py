# Import Module
import os
import yaml
import pathlib

"""
Class label indexes
    0 : bus
    1 : car
    2 : motorcycle
    3 : truck
    4 : person
    5 : crosswalk
"""
# Define root path
# It should be ..\Datasets-data-preparation\
ROOT = pathlib.Path(__file__).parent

# Define targeted data.yaml path.
# This yaml define targeted data classes label.
DATA_YAML_PATH = os.path.join(ROOT, "data")

# Define dataset directory path
DATASETS_PATH = os.path.join(ROOT, "datasets")

# Define list of data classes
data_classes = []

# Read data classes yaml file and get list of classes names.
with open(os.path.join(DATA_YAML_PATH, "pedestrian_data.yaml"), "r") as data:
    data_dict = yaml.safe_load(data) 
    data_classes = data_dict["names"]

def modify_labels(file, raw_classes):
    # Read label text file as readable mode.
    raw_label_txt = open(file, "r")

    # Create label list
    # ? Result of labels list must be something like
    # ? ['0 0.343435 0.455112 0.464223 0.54', '0 0.1234 0.45344 0.86532 0.136897', ... , '']
    label_list = raw_label_txt.read().split("\n")
    
    # Excluding empty string('') from labels_list
    label_list = [label for label in label_list if label != '']

    # Create list of new labels
    prepared_label_list = []

    # Iterate through all label for modifying class label index
    for label in label_list:

        # ? The split_label must be something like 
        # ? ['0', '0.5453335', '0.134654', '0.663211', '0.111111']
        split_label = label.split(" ")

        # Get target class index as integer. Ex. cls_i = 0
        cls_i = int(split_label[0])
        
        cls = raw_classes[cls_i]
        # Iterate through data labels list : ['bus', 'car', 'motorcycle', 'truck']
        for i in range(len(data_classes)):
            
            # If current class is equal to targeted class then change class label.
            if cls == data_classes[i]:
                split_label[0] = str(i)

        prepared_label_list.append(f'{split_label[0]} {split_label[1]} {split_label[2]} {split_label[3]} {split_label[4]}')
    raw_label_txt.close()

    # Open current text file as write mode then write new annotate point to this text file.
    with open(file,"w") as prepared_file:
        for prepared_label in prepared_label_list:
            if prepared_label == prepared_label_list[-1]:
                prepared_file.write(f"{prepared_label}")
            else :
                prepared_file.write(f"{prepared_label}\n")

def class_label_data_preparation(raw_data_label_path, raw_data_yaml_path):
    """ ### Parameters
        - raw_data_label_path ==> Unprepared datasets label directory path.
    """

    raw_data_classes = []

    with open(raw_data_yaml_path, "r") as raw_data_ymal:
        
        # Read raw data label yaml file
        raw_yaml = yaml.safe_load(raw_data_ymal)

        # Get names of class and convert name into lower case form.
        raw_data_classes = [cls.lower() for cls in raw_yaml["names"]]
     
    try:
        # Change current directory to raw data labels dir path.
        os.chdir(raw_data_label_path)
        
        # Iterate through all labels files in label folder.
        # Labels file should be something like 'name.txt', '3ewfwefw343--erwefwe.txt'
        for file in os.listdir():

            # Check whether file is in text format or not.
            if file.endswith(".txt"):
                file_path = f"{raw_data_label_path}\{file}"

                modify_labels(file_path, raw_data_classes)

    except FileNotFoundError:
        return

if __name__ == "__main__":
    # Path should be ../Datasets-data-preparation/datasets/<dataset_name>/
    targeted_dataset_path = os.path.join(DATASETS_PATH, "Vehicles")

    # Path should be ../Datasets-data-preparation/datasets/<dataset_name>/<sub-dataset-dir>/...
    sub_dataset_dir_path = os.path.join(targeted_dataset_path, "vehicle-dataset-3")

    # Get unprepared data.yaml path.
    sub_dataset_yaml_path = os.path.join(sub_dataset_dir_path,"data.yaml")

    for folder_name in ["train", "valid", "test"]:
        try:
            # Path should be ../datasets/<dataset_name>/<sub-dataset-dir/train/labels/...
            label_path = os.path.join(sub_dataset_dir_path,folder_name,"labels")

            class_label_data_preparation(label_path, sub_dataset_yaml_path)

        except(FileNotFoundError):
            continue
#//----------------------------------------------------------------------------------------------