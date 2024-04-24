import os
import yaml
from path import path
from tqdm import tqdm

# Define list of data classes
data_classes = []

# Read data classes yaml file and get list of classes names.
with open(path["/config/data.yml"], "r") as data:
    data_dict = yaml.safe_load(data) 
    data_classes = data_dict["names"]

categories_map = {data_classes[i]: i for i in range(len(data_classes))}


def class_label_data_preparation(overwrite_all_label = False, class_index = None):
    
    """
    Parameters
    ----------
    * overwrite_all_label : bool  (If True, all label files will be modified.)
    * class_index : int           (A number of class index that you want to write into all label files.)
    """
    if not overwrite_all_label:
        class_index = None
    # List all datasets directory
    # Iterate through all datasets
    for dataset_name in os.listdir(path["/datasets"]):

        # Get path of current dataset directory
        dataset_path = os.path.join(path["/datasets"], dataset_name)
        
        # Define array to store category names from data.yaml
        raw_data_classes = []

        if not overwrite_all_label:
            # Get path of data.yaml from current dataset
            dataset_data_yaml = os.path.join(dataset_path,"data.yaml")

            # Open data.yaml and store all category names into array raw_data_classes
            with open(dataset_data_yaml, "r") as raw_data_ymal:
                    
                # Read raw data label yaml file
                raw_yaml = yaml.safe_load(raw_data_ymal)

                # Get names of class and convert name into lower case form.
                raw_data_classes = [cls.lower() for cls in raw_yaml["names"]]

        # Get all sub-directories in current dataset
        subdirectories = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

        # Iterate through all sub-directories
        for folder_name in subdirectories:
            # Within each sub-directory, it should has directory images and labels
            # Get path of labels directory
            # Path should be ../datasets/<dataset_name>/<sub-dataset-dir>/train/labels/...
            labels_path = os.path.join(dataset_path,folder_name,"labels")

            # Change current directory to label directory path.
            os.chdir(labels_path)

            # Iterate through all labels files in label folder.
            # Labels file should be something like 'name.txt', '3ewfwefw343--erwefwe.txt'
            for file in tqdm(os.listdir(), desc=labels_path):
                    
                # Check whether file is in text format or not.
                if file.endswith(".txt"):
                    label_txt_file_path = os.path.join(labels_path, file)
                     
                    # Normalize path
                    label_txt_file = os.path.normpath(label_txt_file_path)
                    label_txt_file = open(label_txt_file, "r")
                    
                    # Create label list
                    # ? Result of labels list must be something like
                    # ? [   '0 0.343435 0.455112 0.464223 0.54', 
                    # ?     '0 0.1234 0.45344 0.86532 0.136897',
                    # ?     '1 0.54456 0.9545 0.86532 0.136897',
                    # ?     ......................................
                    label_list = label_txt_file.read().split("\n")
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
                        
                        # Get target class index as integer. Ex. cls_i = 0 and get value from raw_classes with key cls_i    
                        cls_i = int(split_label[0])
                        if not overwrite_all_label:
                            cls : str = raw_data_classes[cls_i]
                            class_index = None
                            if cls in ['cow', 'buffalo', 'gaur']:
                                class_index = 19
                            elif cls in ['dog', 'wolf']:
                                class_index = 20
                            elif cls in ['buck','doe','deer']:
                                class_index = 17
                            elif cls in data_classes:
                                class_index = categories_map[cls]
                        if class_index is not None:
                            prepared_label_list.append(f'{str(class_index)} {split_label[1]} {split_label[2]} {split_label[3]} {split_label[4]}')
                        
                    label_txt_file.close()
                    path_elements = [element for element in label_txt_file.name.split("\\")]
                    # Add backslash after the drive letter
                    path_elements[0] += '\\'
                    name = path_elements[-1].rsplit('.',1)[0]

                    if len(prepared_label_list) > 0:
                        # Open current text file as write mode then write new annotate point to this text file.
                        # print(prepared_label_list)
                        with open(label_txt_file.name,"w") as prepared_file:
                            for prepared_label in prepared_label_list:
                                prepared_file.write(f"{prepared_label}\n")
                    else:
                        path_elements_without_name = path_elements[:-2]
                        image_path = os.path.join(*path_elements_without_name, "images", name + ".jpg")
                        label_path = os.path.join(*path_elements_without_name, "labels", name + ".txt")
                        os.remove(image_path)
                        os.remove(label_path)

def main():
    class_label_data_preparation(overwrite_all_label = True, class_index = 21)

if __name__ == "__main__":
    main()
# #//----------------------------------------------------------------------------------------------