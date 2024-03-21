
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

bbox1 = [588.002757, 340.123554, 606.371265, 370.737736]
bbox2 = [591.064175, 370.737736, 610.963393, 390.636954]

print(calculate_iou(bbox1, bbox2))