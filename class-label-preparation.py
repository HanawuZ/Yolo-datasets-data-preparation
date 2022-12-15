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
# Define data.yaml path
data_yaml_path = pathlib.Path(__file__).parent / "datasets"/"vehicle-datasets"/"data.yaml"

# Define list of data classes
data_classes = []

# Read data classes yaml file and get list of classes names.
with open(data_yaml_path, 'r') as data:
    data_dict = yaml.safe_load(data) 
    data_classes = data_dict["names"]

def fix_modify_labels(file):
    # Read label text file as readable mode.
    raw_label_txt = open(file, "r")
    label_list = raw_label_txt.read().split("\n")
    
    # Excluding empty string('') from labels_list
    label_list = [label for label in label_list if label != '']
    prepared_label_list = []
    for label in label_list:

        # ? The split_label must be something like 
        # ? ['0', '0.5453335', '0.134654', '0.663211', '0.111111']
        split_label = label.split(" ")
        split_label[0] = "4"
        prepared_label_list.append(f'{split_label[0]} {split_label[1]} {split_label[2]} {split_label[3]} {split_label[4]}')
    
    raw_label_txt.close()

    # Open current text file as write mode then write new annotate point to this text file.
    with open(file,'w') as prepared_file:
        for prepared_label in prepared_label_list:
            if prepared_label == prepared_label_list[-1]:
                prepared_file.write(f"{prepared_label}")
            else :
                prepared_file.write(f"{prepared_label}\n")

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
            if cls == data_classes[i]:
                split_label[0] = str(i)
        prepared_label_list.append(f'{split_label[0]} {split_label[1]} {split_label[2]} {split_label[3]} {split_label[4]}')
    raw_label_txt.close()

    # Open current text file as write mode then write new annotate point to this text file.
    with open(file,'w') as prepared_file:
        for prepared_label in prepared_label_list:
            if prepared_label == prepared_label_list[-1]:
                prepared_file.write(f"{prepared_label}")
            else :
                prepared_file.write(f"{prepared_label}\n")

                
def class_label_data_preparation(raw_data_label_path, raw_data_yaml_path):
    """ Parameters:
        - raw_data_label_path => Unprepared datasets label directory path.
        - raw_data_yaml_path => Path of raw datasets yaml file
    """

    raw_data_classes = []

    with open(raw_data_yaml_path, 'r') as raw_data_ymal:
        
        # Read raw data label yaml file
        raw_yaml = yaml.safe_load(raw_data_ymal)
        raw_data_classes = [cls.lower() for cls in raw_yaml["names"]]
    # print(raw_data_classes)

    # Change directory to raw data labels dir path.
    os.chdir(raw_data_label_path)
    
    # iterate through all labels file in label folder.
    for file in os.listdir():

        # Check whether file is in text format or not.
        if file.endswith(".txt"):
            file_path = f"{raw_data_label_path}\{file}"
    
            # call modify label file function.
            # modify_labels(file_path, raw_data_classes)

            fix_modify_labels(file_path)
# Define motocycle data yaml file path and label directory path.
# selected_data_yaml_path = r'C:\Users\asus\Desktop\PYTHON\Object-Detection-New\data-preparation\datasets\Motorcycle-datasets-1\data.yaml'
# selected_label_path = r'C:\Users\asus\Desktop\PYTHON\Object-Detection-New\data-preparation\datasets\Motorcycle-datasets-1\train\labels'

selected_data_yaml_path = data_yaml_path.parent/"person-7"/"data.yaml"
selected_label_dir_path = data_yaml_path.parent/"person-7"/"valid"/"labels"
class_label_data_preparation(selected_label_dir_path, selected_data_yaml_path)

