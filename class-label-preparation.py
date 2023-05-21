# Import Module
import os
import yaml
from path import path
from tqdm import tqdm

"""
Class label indexes
    car : 0
    bus : 1
    person : 2
    bike : 3
    truck : 4
    motorcycle : 5
    train : 6
    rider : 7
    traffic sign 8
    traffic light(red) : 9
    traffic light(yellow) : 10
    traffic light(green) : 11
    cyclist : 12
"""

# Define list of data classes
data_classes = []

# Read data classes yaml file and get list of classes names.
with open(path["/config/data.yml"], "r") as data:
    data_dict = yaml.safe_load(data) 
    data_classes = data_dict["names"]

def read_labels(file, raw_classes):
     # Read label text file as readable mode.
    raw_label_txt = open(file, "r")

    # Create label list
    # ? Result of labels list must be something like
    # ? ['0 0.343435 0.455112 0.464223 0.54', '0 0.1234 0.45344 0.86532 0.136897', ... , '']
    label_list = raw_label_txt.read().split("\n")

    # Excluding empty string('') from labels_list
    label_list = [label for label in label_list if label != '']

    prepared_label_list = []
    # Iterate through all label for modifying class label index and ignore class label that not in our class label
    for label in label_list:

        # ? The split_label must be something like 
        # ? ['0', '0.5453335', '0.134654', '0.663211', '0.111111']
        split_label = label.split(" ")
        # Get target class index as integer. Ex. cls_i = 0
        cls_i = int(split_label[0])
        
        cls = raw_classes[cls_i]

        # * Change class label
        # Iterate through data labels list : ['bus', 'car', 'motorcycle', 'truck', ....]
        for i in range(len(data_classes)):
            
            # If current class is equal to targeted class then change class label.
            if cls == data_classes[i]:
                split_label[0] = str(i)
                prepared_label_list.append(f'{split_label[0]} {split_label[1]} {split_label[2]} {split_label[3]} {split_label[4]}')
                break

    print(f"Before = {label_list}\n\n")
    print(f"After = {prepared_label_list}")

# //-------------------------------------------------------------------------------------------------------
def modify_labels(file, raw_classes):
    # Read label text file as readable mode.
    raw_label_txt = open(file, "r")

    # Create label list
    # ? Result of labels list must be something like
    # ? [   '0 0.343435 0.455112 0.464223 0.54', 
    # ?     '0 0.1234 0.45344 0.86532 0.136897',
    # ?     '1 0.54456 0.9545 0.86532 0.136897',
    # ?     ......................................
    label_list = raw_label_txt.read().split("\n")
    
    # Excluding empty string('') from labels_list
    label_list = [label for label in label_list if label != '']

    # Create list of new labels
    prepared_label_list = []

    # Iterate through all label for modifying class label index
    # Iterate through this list
    # ? [   '0 0.343435 0.455112 0.464223 0.54', 
    # ?     '0 0.1234 0.45344 0.86532 0.136897',
    # ?     '1 0.54456 0.9545 0.86532 0.136897',
    # ?     ....................................  ]
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
                break

    raw_label_txt.close()

    # Open current text file as write mode then write new annotate point to this text file.
    with open(file,"w") as prepared_file:
        for prepared_label in prepared_label_list:
            prepared_file.write(f"{prepared_label}\n")

def class_label_data_preparation(raw_data_label_path, raw_data_yaml_path):
    """ ### Parameters
        - raw_data_label_path   : Unprepared datasets label directory path.
        - raw_data_yaml_path    : Unprepared data.yaml path.
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
        for file in tqdm(os.listdir(), desc=raw_data_label_path):

            # Check whether file is in text format or not.
            if file.endswith(".txt"):
                file_path = f"{raw_data_label_path}\{file}"

                modify_labels(file_path, raw_data_classes)

    except FileNotFoundError:
        return

def main():
    # List all datasets directory
    # Iterate through all datasets
    for dataset_name in os.listdir(path["/datasets"]):

        # Get current dataset path
        target_dataset_path = os.path.join(path["/datasets"], dataset_name)
        
        # Get unprepared data.yaml path.
        target_dataset_data_yaml = os.path.join(target_dataset_path,"data.yaml")

        for folder_name in ["train", "valid", "test", "export"]:
            try:
                # Path should be ../datasets/<dataset_name>/<sub-dataset-dir>/train/labels/...
                labels_path = os.path.join(target_dataset_path,folder_name,"labels")

                class_label_data_preparation(labels_path, target_dataset_data_yaml)

            except(FileNotFoundError):
                continue

if __name__ == "__main__":
    main()
#//----------------------------------------------------------------------------------------------