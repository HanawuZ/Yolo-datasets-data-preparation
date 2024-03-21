import json
import os
from tqdm import tqdm
from bdd100k_config import categories, img_size
from pprint import pprint
import math

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

def generate_yolo_labels(img_labels, fname_prefix=None, fname_postfix=None):
    img_w, img_h = img_size
    ignore_categories = ["drivable area", "lane"]
    
    rider_labels = [label for label in img_labels if label['category'] == "rider"]
    bike_labels = [label for label in img_labels if label['category'] == "bike"]
    motor_labels = [label for label in img_labels if label['category'] == "motor"]
    
    # Merge list bike_labels and motor_lables
    small_vehicle_labels = bike_labels + motor_labels
    
    # Case 3: If there're no rider and has bike(s)
    if (len(rider_labels) == 0) and (len(small_vehicle_labels) > 0):
        for small_vehicle in small_vehicle_labels:
            class_name = small_vehicle['category']
            x1 = small_vehicle['box2d']['x1']
            y1 = small_vehicle['box2d']['y1']
            x2 = small_vehicle['box2d']['x2']
            y2 = small_vehicle['box2d']['y2']
                        
            bbox_x = (x1 + x2)/2
            bbox_y = (y1 + y2)/2

            bbox_width = x2-x1
            bbox_height = y2-y1

            bbox_x_norm = bbox_x / img_w
            bbox_y_norm = bbox_y / img_h

            bbox_width_norm = bbox_width / img_w
            bbox_height_norm = bbox_height / img_h

            line_to_write = '{} {} {} {} {}'.format(class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)

    # TODO case critcal:
    # Rider and small vehicle are paired but it's not intersect
    # Solution: use nearest centroid between rider and small vehicle

    # elif len(rider_labels) == len(small_vehicle_labels):
    #     pass
               
    else:
        for small_vehicle in small_vehicle_labels:
            class_name = small_vehicle['category']
            small_vehicle_X1 = small_vehicle['box2d']['x1']
            small_vehicle_Y1 = small_vehicle['box2d']['y1']
            small_vehicle_X2 = small_vehicle['box2d']['x2']
            small_vehicle_Y2 = small_vehicle['box2d']['y2']
            small_vehicle_bbox = [small_vehicle_X1, small_vehicle_Y1, small_vehicle_X2, small_vehicle_Y2]
            
            # Calculate centroid of small vehicle bbox
            small_vehicle_centroid_x = (small_vehicle_X1 + small_vehicle_X2)/2
            small_vehicle_centroid_y = (small_vehicle_Y1 + small_vehicle_Y2)/2
            
            match_rider_labels = []
            if len(rider_labels) > 0:
                for i in range(0, len(rider_labels)):
                    rider_y1 = rider_labels[i]['box2d']['y1']
                    rider_x2 = rider_labels[i]['box2d']['x2']
                    rider_x1 = rider_labels[i]['box2d']['x1']
                    rider_y2 = rider_labels[i]['box2d']['y2']
                    rider_bbox = [rider_x1, rider_y1, rider_x2, rider_y2]
                    
                    # Calculate centroid of rider bbox
                    rider_centroid_x = (rider_x1 + rider_x2)/2
                    rider_centroid_y = (rider_y1 + rider_y2)/2
                    
                    dist = math.dist((small_vehicle_centroid_x, small_vehicle_centroid_y), (rider_centroid_x, rider_centroid_y))
                    
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
                
                print(class_id, lowest_x1, lowest_y1, highest_x2, highest_y2)
            for match_rider_label in match_rider_labels:
                
                rider_labels.remove(list(match_rider_label.values())[0])

            # TODO use euclidean distance to match rider and small vehicle
            # if len(match_rider_labels) == 0:
            #     nearest_rider = None
            #     nearest_dist = float('inf')
            #     for i in range(0, len(rider_labels)):
            #         rider_y1 = rider_labels[i]['box2d']['y1']
            #         rider_x2 = rider_labels[i]['box2d']['x2']
            #         rider_x1 = rider_labels[i]['box2d']['x1']
            #         rider_y2 = rider_labels[i]['box2d']['y2']
            #         rider_bbox = [rider_x1, rider_y1, rider_x2, rider_y2]
                    
            #         # Calculate centroid of rider bbox
            #         rider_centroid_x = (rider_x1 + rider_x2)/2
            #         rider_centroid_y = (rider_y1 + rider_y2)/2
                    
            #         dist = math.dist((small_vehicle_centroid_x, small_vehicle_centroid_y), (rider_centroid_x, rider_centroid_y))

            
        if len(rider_labels) > 0:
            for rider in rider_labels:
                class_id = categories['bicyclist']
                x1 = rider['box2d']['x1']
                y1 = rider['box2d']['y1']
                x2 = rider['box2d']['x2']
                y2 = rider['box2d']['y2']
                
                print("Bicyclist", x1, y1, x2, y2)
            
    # if len(rider_labels) > 1 and len(small_vehicle_labels) == 1:
                    
    #                 for small_vehicle in small_vehicle_labels:
    #                     class_name = small_vehicle['category']
                        
    #                     small_vehicle_X1 = small_vehicle['box2d']['x1']
    #                     small_vehicle_Y1 = small_vehicle['box2d']['y1']
    #                     small_vehicle_X2 = small_vehicle['box2d']['x2']
    #                     small_vehicle_Y2 = small_vehicle['box2d']['y2']
    #                     small_vehicle_bbox = [small_vehicle_X1, small_vehicle_Y1, small_vehicle_X2, small_vehicle_Y2]
                        
    #                     match_rider_labels = []
    #                     for rider in rider_labels:
    #                         rider_y1 = rider['box2d']['y1']
    #                         rider_x2 = rider['box2d']['x2']
    #                         rider_x1 = rider['box2d']['x1']
    #                         rider_y2 = rider['box2d']['y2']
    #                         rider_bbox = [rider_x1, rider_y1, rider_x2, rider_y2]
                            
    #                         iou = calculate_iou(rider_bbox, small_vehicle_bbox)
                            
    #                         if iou > 0.1:
    #                             match_rider_labels.append(rider)                               
                            
    #                     if len(match_rider_labels) > 1:
    #                         if class_name == 'bike':
    #                             class_id = categories['bicyclist']
    #                         elif class_name == 'motor':
    #                             class_id = categories['motorcyclist']
                            
    #                         x1s = [rider['box2d']['x1'] for rider in match_rider_labels]
    #                         y1s = [rider['box2d']['y1'] for rider in match_rider_labels]
    #                         x2s = [rider['box2d']['x2'] for rider in match_rider_labels]
    #                         y2s = [rider['box2d']['y2'] for rider in match_rider_labels]
                            
    #                         lowest_x1, lowest_y1 = min(x1s), min(y1s)
    #                         highest_x2, highest_y2 = max(x2s), max(y2s)
                            
    #                         bbox_x = (lowest_x1 + highest_x2)/2
    #                         bbox_y = (lowest_y1 + highest_y2)/2

    #                         bbox_width = highest_x2-lowest_x1
    #                         bbox_height = highest_y2-lowest_y1

    #                         bbox_x_norm = bbox_x / img_w
    #                         bbox_y_norm = bbox_y / img_h

    #                         bbox_width_norm = bbox_width / img_w
    #                         bbox_height_norm = bbox_height / img_h

    #                         line_to_write = '{} {} {} {} {}'.format(class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)
                    
                        
                # If the number of rider_labels is equal to the number of small_vehicle_labels
                # Match pair of rider and motor or bicycle
    # if len(small_vehicle_labels) == len(rider_labels):
    #     for rider in rider_labels:
    #         rider_y1 = rider['box2d']['y1']
    #         rider_x2 = rider['box2d']['x2']
    #         rider_x1 = rider['box2d']['x1']
    #         rider_y2 = rider['box2d']['y2']
    #         rider_bbox = [rider_x1, rider_y1, rider_x2, rider_y2]
                        
    #         match_small_vehicle_label = None
    #         current_iou = 0
                        
    #         for small_vehicle in small_vehicle_labels:
    #             small_vehicle_X1 = small_vehicle['box2d']['x1']
    #             small_vehicle_Y1 = small_vehicle['box2d']['y1']
    #             small_vehicle_X2 = small_vehicle['box2d']['x2']
    #             small_vehicle_Y2 = small_vehicle['box2d']['y2']
    #             small_vehicle_bbox = [small_vehicle_X1, small_vehicle_Y1, small_vehicle_X2, small_vehicle_Y2]
    #             iou = calculate_iou(rider_bbox, small_vehicle_bbox)

    #             if iou > current_iou:
    #                 current_iou = iou
    #                 match_small_vehicle_label = small_vehicle
                                
    #             if match_small_vehicle_label is not None:
    #                 match_small_vehicle_label_X1 = match_small_vehicle_label['box2d']['x1']
    #                 match_small_vehicle_label_Y1 = match_small_vehicle_label['box2d']['y1']
    #                 match_small_vehicle_label_X2 = match_small_vehicle_label['box2d']['x2']
    #                 match_small_vehicle_label_Y2 = match_small_vehicle_label['box2d']['y2']
                            
    #                 lowest_x1, lowest_y1 = min(match_small_vehicle_label_X1, rider_x1), min(match_small_vehicle_label_Y1, rider_y1)
    #                 highest_x2, highest_y2 = max(match_small_vehicle_label_X2, rider_x2), max(match_small_vehicle_label_Y2, rider_y2)

    #                 class_name = match_small_vehicle_label['category']
                            
    #                 if class_name == 'bike':
    #                     class_id = categories['bicyclist']
                                
    #                 elif class_name == 'motor':
    #                     class_id = categories['motorcyclist']
                            
    #                 print(lowest_x1, lowest_y1, highest_x2, highest_y2)
    #                 bbox_x = (lowest_x1 + highest_x2)/2
    #                 bbox_y = (lowest_y1 + highest_y2)/2

    #                 bbox_width = highest_x2-lowest_x1
    #                 bbox_height = highest_y2-lowest_y1

    #                 bbox_x_norm = bbox_x / img_w
    #                 bbox_y_norm = bbox_y / img_h

    #                 bbox_width_norm = bbox_width / img_w
    #                 bbox_height_norm = bbox_height / img_h

    #                 line_to_write = '{} {} {} {} {}'.format(class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)
                    
                    
                
                # Case 1.2: If there're > 1 riders and 1 motor
                #       If all rider bbox are intersecting with motor bbox
                #           Merge all rider and motor into one bbox
                #           Write class name as 'motorcyclist'
                #       Else
                #           Match one rider to one motor with best iou
                #           Define other rider as 'motorcyclist'
                #       Define other rider as 'bicyclist'
                
 
                            

    for label in img_labels:
        class_name = label['category']
        if class_name in ['rider',]:    
            continue
        y1 = label['box2d']['y1']
        x2 = label['box2d']['x2']
        x1 = label['box2d']['x1']
        y2 = label['box2d']['y2']
        print(class_name, x1, y1, x2, y2)
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

        line_to_write = '{} {} {} {} {}'.format(class_id, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)


# * ok
# 1 rider-bike and 1 bike
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 831.759191,
#             "y1": 214.368235,
#             "x2": 862.44585,
#             "y2": 283.413221
#         },
#         "id": 59215
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 829.457715,
#             "y1": 234.314564,
#             "x2": 866.281707,
#             "y2": 286.481885
#         },
#         "id": 59216
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 977.520826,
#             "y1": 242.753396,
#             "x2": 1056.538976,
#             "y2": 299.523716
#         },
#         "id": 59217
#     }
# ]

# Rider and small vehicle are paired but it's not intersect
# Solution: use nearest centroid between rider and small vehicle
# data = [
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 591.064175,
#             "y1": 370.737736,
#             "x2": 610.963393,
#             "y2": 390.636954
#         },
#         "id": 63935
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 588.002757,
#             "y1": 340.123554,
#             "x2": 606.371265,
#             "y2": 370.737736
#         },
#         "id": 63936
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 623.209066,
#             "y1": 340.123554,
#             "x2": 656.884666,
#             "y2": 364.6149
#         },
#         "id": 63937
#     },
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 627.801193,
#             "y1": 370.737736,
#             "x2": 656.884666,
#             "y2": 393.698371
#         },
#         "id": 63938
#     }
# ]

# * ok
# Two or more rider on same small vehicle
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 447.581183,
#             "y1": 336.513244,
#             "x2": 499.029216,
#             "y2": 487.182482
#         },
#         "id": 73208
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 399.80801,
#             "y1": 344.781678,
#             "x2": 491.679498,
#             "y2": 510.150353
#         },
#         "id": 73209
#     },
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 386.027287,
#             "y1": 391.636136,
#             "x2": 498.1105,
#             "y2": 547.817663
#         },
#         "id": 73210
#     }
# ]

# * ok
# 3 rider 3 bike
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 680.025953,
#             "y1": 360.600918,
#             "x2": 692.503495,
#             "y2": 384.308246
#         },
#         "id": 89918
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 701.237772,
#             "y1": 361.848672,
#             "x2": 716.210821,
#             "y2": 390.547015
#         },
#         "id": 89919
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 736.174885,
#             "y1": 359.353164,
#             "x2": 753.643442,
#             "y2": 388.051507
#         },
#         "id": 89920
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 678.7782,
#             "y1": 369.335196,
#             "x2": 692.503495,
#             "y2": 391.79477
#         },
#         "id": 89921
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 702.485526,
#             "y1": 375.573967,
#             "x2": 716.210821,
#             "y2": 399.281295
#         },
#         "id": 89922
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 737.422639,
#             "y1": 378.069475,
#             "x2": 751.147934,
#             "y2": 400.529048
#         },
#         "id": 89923
#     }
# ]

# # 1 rider with 1 bike and another 1 rider
# # 1 rider-bike is not intersect
# data = [
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": True,
#             "truncated": True,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 0.734691,
#             "y1": 292.775639,
#             "x2": 47.020426,
#             "y2": 357.796077
#         },
#         "id": 57242
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": True,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 0.734691,
#             "y1": 266.326647,
#             "x2": 10.653063,
#             "y2": 309.306258
#         },
#         "id": 57243
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": True,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 400.734691,
#             "y1": 266.326647,
#             "x2": 410.653063,
#             "y2": 309.306258
#         },
#         "id": 57243
#     }
# ]

# * ok
# 1 bike-rider and 1 motor-bike
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 132.945896,
#             "y1": 314.86405,
#             "x2": 323.999979,
#             "y2": 520.76312
#         },
#         "id": 94618
#     },
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 40.933816,
#             "y1": 337.717813,
#             "x2": 328.716277,
#             "y2": 555.022935
#         },
#         "id": 94619
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 847.062841,
#             "y1": 349.464035,
#             "x2": 873.491842,
#             "y2": 401.343189
#         },
#         "id": 94620
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 848.041691,
#             "y1": 361.47721,
#             "x2": 878.386102,
#             "y2": 403.567843
#         },
#         "id": 94621
#     }
# ]

# * ok
# 1 motor-rider and 1 lonely rider
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": False,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 1119.942421,
#             "y1": 275.217068,
#             "x2": 1235.32381,
#             "y2": 437.799933
#         },
#         "id": 95449
#     },
#     {
#         "category": "motor",
#         "attributes": {
#             "occluded": False,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 1102.067077,
#             "y1": 329.361416,
#             "x2": 1271.642753,
#             "y2": 443.044543
#         },
#         "id": 95450
#     },
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": False,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 600.942421,
#             "y1": 275.217068,
#             "x2": 620.32381,
#             "y2": 437.799933
#         },
#         "id": 95449
#     },
# ]

# * ok
# There are rider(s) but no small vehicle
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 1057.493958,
#             "y1": 349.080329,
#             "x2": 1086.669293,
#             "y2": 395.146649
#         },
#         "id": 108266
#     }
# ]

# 1 rider-bike
# data = [
#     {
#         "category": "rider",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 548.113347,
#             "y1": 288.369109,
#             "x2": 597.925005,
#             "y2": 381.261119
#         },
#         "id": 1612521
#     },
#     {
#         "category": "bike",
#         "attributes": {
#             "occluded": True,
#             "truncated": False,
#             "trafficLightColor": "none"
#         },
#         "manualShape": True,
#         "manualAttributes": True,
#         "box2d": {
#             "x1": 541.38204,
#             "y1": 331.449461,
#             "x2": 604.656307,
#             "y2": 393.377469
#         },
#         "id": 1612522
#     }
# ]

# rider-motors and numerous bikes
data = [
    {
        "category": "rider",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 568.780889,
            "y1": 167.364232,
            "x2": 639.588834,
            "y2": 293.531115
        },
        "id": 1616031
    },
    {
        "category": "rider",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 573.930559,
            "y1": 184.100655,
            "x2": 635.726582,
            "y2": 289.668864
        },
        "id": 1616032
    },
    {
        "category": "motor",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 572.643142,
            "y1": 221.435753,
            "x2": 634.439166,
            "y2": 315.417207
        },
        "id": 1616033
    },
    {
        "category": "motor",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 768.330553,
            "y1": 189.250324,
            "x2": 840.425913,
            "y2": 276.794692
        },
        "id": 1616034
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 818.539821,
            "y1": 198.262244,
            "x2": 973.029881,
            "y2": 301.255619
        },
        "id": 1616035
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 732.282871,
            "y1": 212.423833,
            "x2": 783.779558,
            "y2": 266.495355
        },
        "id": 1616036
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 711.684196,
            "y1": 207.274164,
            "x2": 763.180883,
            "y2": 254.9086
        },
        "id": 1616037
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 683.361019,
            "y1": 203.411914,
            "x2": 736.145123,
            "y2": 245.896681
        },
        "id": 1616038
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 732.282871,
            "y1": 218.860919,
            "x2": 779.917306,
            "y2": 252.333765
        },
        "id": 1616039
    },
    {
        "category": "bike",
        "attributes": {
            "occluded": True,
            "truncated": False,
            "trafficLightColor": "none"
        },
        "manualShape": True,
        "manualAttributes": True,
        "box2d": {
            "x1": 716.833865,
            "y1": 209.848999,
            "x2": 754.168963,
            "y2": 240.747012
        },
        "id": 1616040
    }
]

generate_yolo_labels(data)