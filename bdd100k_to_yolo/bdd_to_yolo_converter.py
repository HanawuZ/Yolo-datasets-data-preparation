import json
import os
from tqdm import tqdm
from bdd100k_config import PATHS, categories, img_size


def calculate_iou(actual_bbox, predicted_bbox):
    # Extract coordinates
    x1_a, y1_a, x2_a, y2_a = actual_bbox
    x1_p, y1_p, x2_p, y2_p = predicted_bbox
    
    # Calculate the area of actual and predicted bounding boxes
    area_a = (x2_a - x1_a + 1) * (y2_a - y1_a + 1)
    area_p = (x2_p - x1_p + 1) * (y2_p - y1_p + 1)

    # Calculate the intersection coordinates
    inter_x1 = max(x1_a, x1_p)
    inter_y1 = max(y1_a, y1_p)
    inter_x2 = min(x2_a, x2_p)
    inter_y2 = min(y2_a, y2_p)
    

    # Check if there is an intersection
    if inter_x1 < inter_x2 and inter_y1 < inter_y2:
        # Calculate the area of intersection
        intersection = (inter_x2 - inter_x1 + 1) * (inter_y2 - inter_y1 + 1)
    else:
        # No intersection, set intersection area to 0
        intersection = 0

    # Calculate Union
    union = area_a + area_p - intersection

    # Calculate IoU
    iou = intersection / union

    return iou

def generate_yolo_labels(json_path, save_path, fname_prefix=None, fname_postfix=None):
    img_w, img_h = img_size
    ignore_categories = ["drivable area", "lane"]

    with open(json_path) as json_file:
        data = json.load(json_file)

        for img in tqdm(data):
            img_name = str(img['name'][:-4])
            img_label_txt = (fname_prefix if fname_prefix is not None else '') + img_name
            img_label_txt += (fname_postfix if fname_postfix is not None else '') + ".txt"
            img_labels = [l for l in img['labels'] if l['category'] not in ignore_categories]
            
            file_path = os.path.join(save_path,img_label_txt)
            
            with open(file_path, 'w+') as f_label:
                
                rider_labels = [label for label in img_labels if label['category'] == "rider"]
                bike_labels = [label for label in img_labels if label['category'] == "bike"]
                motor_labels = [label for label in img_labels if label['category'] == "motor"]

                # Merge list bike_labels and motor_lables
                small_vehicle_labels = bike_labels + motor_labels
                
                for small_vehicle in small_vehicle_labels:
                    class_name = small_vehicle['category']
                    small_vehicle_X1 = small_vehicle['box2d']['x1']
                    small_vehicle_Y1 = small_vehicle['box2d']['y1']
                    small_vehicle_X2 = small_vehicle['box2d']['x2']
                    small_vehicle_Y2 = small_vehicle['box2d']['y2']
                    small_vehicle_bbox = [small_vehicle_X1, small_vehicle_Y1, small_vehicle_X2, small_vehicle_Y2]
                    
                    match_rider_labels = []
                    if len(rider_labels) > 0:
                        for i in range(0, len(rider_labels)):
                            rider_y1 = rider_labels[i]['box2d']['y1']
                            rider_x2 = rider_labels[i]['box2d']['x2']
                            rider_x1 = rider_labels[i]['box2d']['x1']
                            rider_y2 = rider_labels[i]['box2d']['y2']
                            rider_bbox = [rider_x1, rider_y1, rider_x2, rider_y2]
                            
                            iou = calculate_iou(rider_bbox, small_vehicle_bbox)
                            # Append rider object that intersect with small vehicle
                            if iou > 0.1:
                                match_rider_labels.append({i:rider_labels[i]}) 


                    if len(match_rider_labels) > 0:
                        if class_name == 'bike':
                            class_id = categories['bicyclist']
                        elif class_name == 'motor':
                            class_id = categories['motorcyclist']
                                    
                        x1s = [list(rider.values())[0]['box2d']['x1'] for rider in match_rider_labels]
                        y1s = [list(rider.values())[0]['box2d']['y1'] for rider in match_rider_labels]
                        x2s = [list(rider.values())[0]['box2d']['x2'] for rider in match_rider_labels]
                        y2s = [list(rider.values())[0]['box2d']['y2'] for rider in match_rider_labels]
                        
                        x1s = x1s + [small_vehicle_X1]
                        y1s = y1s + [small_vehicle_Y1]
                        x2s = x2s + [small_vehicle_X2]
                        y2s = y2s + [small_vehicle_Y2]
                        
                        lowest_x1, lowest_y1 = min(x1s), min(y1s)
                        highest_x2, highest_y2 = max(x2s), max(y2s)
                        
                        bbox_x = (lowest_x1 + highest_x2)/2
                        bbox_y = (lowest_y1 + highest_y2)/2

                        bbox_width = highest_x2-lowest_x1
                        bbox_height = highest_y2-lowest_y1

                        bbox_x_norm = bbox_x / img_w
                        bbox_y_norm = bbox_y / img_h

                        bbox_width_norm = bbox_width / img_w
                        bbox_height_norm = bbox_height / img_h

                        line_to_write = '{} {} {} {} {}'.format(
                            class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)
                        f_label.write(line_to_write + "\n")
                        
                    for match_rider_label in match_rider_labels:
                        rider_labels.remove(list(match_rider_label.values())[0])
                        
                for label in img_labels:
                    if label['category'] == 'rider':    
                        continue
                    
                    class_name = label['category']
                    y1 = label['box2d']['y1']
                    x2 = label['box2d']['x2']
                    x1 = label['box2d']['x1']
                    y2 = label['box2d']['y2']
                    
                    # If class name is traffic light, then need to specify what color a traffic light is
                    if class_name == "traffic light":

                        # Get traffic light attributes
                        attributes = label["attributes"]

                        # Get color of traffic light
                        traffic_light_color = attributes["trafficLightColor"] if attributes["trafficLightColor"] in ["red", "yellow", "green"] else None
                        
                        class_id = categories[f"{class_name}({traffic_light_color})"] if traffic_light_color is not None else categories[class_name] 
                            
                    else :
                        class_id = categories[class_name]

                    bbox_x = (x1 + x2)/2
                    bbox_y = (y1 + y2)/2

                    bbox_width = x2-x1
                    bbox_height = y2-y1

                    bbox_x_norm = bbox_x / img_w
                    bbox_y_norm = bbox_y / img_h

                    bbox_width_norm = bbox_width / img_w
                    bbox_height_norm = bbox_height / img_h

                    line_to_write = '{} {} {} {} {}'.format(
                        class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)
                    f_label.write(line_to_write + "\n")


def generate_yolo_filenames(imgs_path, labels_path, output_file_path):
    os.makedirs(PATHS['save_path'] , exist_ok=True)
    count = 0
    with open(output_file_path, 'w+') as f:
        for dirpath, dirs, files in os.walk(imgs_path):
            for filename in tqdm(files):
                is_exist = os.path.isfile(labels_path+filename[:-4] + '.txt')
                if is_exist:
                    if filename.endswith(".jpg"):
                        file_path = os.path.join(
                            PATHS['owner_prefix'], dirpath, filename)
                        f.write(file_path + "\n")
                else:
                    count += 1
    print('number of skipped files: {}'.format(count))


def generate_names_file(filename='bdd100k.names'):
    os.makedirs(PATHS['save_path'] , exist_ok=True)
    output_file_path = PATHS['save_path'] + filename
    with open(output_file_path, 'w+') as f:
        for key, _ in categories.items():
            f.write(key + "\n")
    print('{} created'.format(filename))


def generate_data_file(filename='bdd100k.data'):
    os.makedirs(PATHS['save_path'] , exist_ok=True)
    output_file_path = PATHS['save_path'] + filename
    with open(output_file_path, 'w+') as f:
        f.write('classes = 10' + '\n')
        f.write('train = {}train.txt'.format(PATHS['save_path']) + '\n')
        f.write('valid = {}val.txt'.format(PATHS['save_path']) + '\n')
        f.write('test = {}test.txt'.format(PATHS['save_path']) + '\n')
        f.write('names = {}bdd100k.names'.format(PATHS['save_path']) + '\n')
        f.write('backup = {}backup'.format(PATHS['save_path']) + '\n')
    print('{} created'.format(filename))


def main():
    print('start YOLO labels creation')

    # Start converting bdd100k labels format into YOLO format
    generate_yolo_labels(json_path = PATHS["/bdd100k/train/labels/bdd100k_labels_images_train.json"], 
                         save_path = PATHS["/preprocessed_bdd100k/train/labels"],
                         fname_prefix=None, fname_postfix=None)

if __name__ == '__main__':
    main()

