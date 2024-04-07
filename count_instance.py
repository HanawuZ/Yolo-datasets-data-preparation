import os
import yaml
from path import path
from tqdm import tqdm

def count_instances(class_index, labels_path):
    os.chdir(labels_path)
    count = 0
    for file in tqdm(os.listdir(), desc=labels_path):
        # Check whether file is in text format or not.
        if file.endswith(".txt"):
            label_txt_file_path = os.path.join(labels_path, file)
            
            # Read label file
            with open(label_txt_file_path, "r") as label_file:
                label_list = label_file.read().split("\n")

                # Excluding empty string('') from labels_list
                label_list = [label for label in label_list if label != '']

                prepared_label_list = []
                # Iterate through all label for modifying class label index and ignore class label that not in our class label
                for label in label_list:

                    # ? The split_label must be something like 
                    # ? ['0', '0.5453335', '0.134654', '0.663211', '0.111111']
                    split_label = label.split(" ")
                    
                    if split_label[0] == str(class_index):
                        count+=1
    print("Number of instances: {}".format(count))
def main():
    # List all datasets directory
    # Iterate through all datasets
    for dataset_name in os.listdir(path["/datasets"]):

        # Get current dataset path
        target_dataset_path = os.path.join(path["/datasets"], dataset_name)
    
        # for folder_name in ["train", "valid", "test",]:
        for folder_name in ["train"]:
            
            # Path should be ../datasets/<dataset_name>/<sub-dataset-dir>/train/labels/...
            labels_path = os.path.join(target_dataset_path,folder_name,"labels")
            count_instances(15, labels_path)

if __name__ == "__main__":
    main()