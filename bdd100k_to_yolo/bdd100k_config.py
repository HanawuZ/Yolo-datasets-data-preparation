import os
from pathlib import Path

ROOT = Path(__file__).parent 
BDD100K_PATH = os.path.join(ROOT,"bdd100k")

BDD100K_TRAIN_DIR = os.path.join(BDD100K_PATH,"train")
BDD100K_TRAIN_IMAGES_DIR = os.path.join(BDD100K_TRAIN_DIR,"images")
BDD100K_TRAIN_LABELS_DIR = os.path.join(BDD100K_TRAIN_DIR,"labels")
BDD100K_TRAIN_LABELS_JSON = os.path.join(BDD100K_TRAIN_LABELS_DIR,"bdd100k_labels_images_train.json")

BDD100K_VALID_DIR = os.path.join(BDD100K_PATH,"valid")
BDD100K_VALID_IMAGES_DIR = os.path.join(BDD100K_VALID_DIR,"images")
BDD100K_VALID_LABELS_DIR = os.path.join(BDD100K_VALID_DIR,"labels")
BDD100K_VALID_LABELS_JSON = os.path.join(BDD100K_VALID_LABELS_DIR,"bdd100k_labels_images_val.json")

PREPROCESSED_BDD100K_PATH = os.path.join(ROOT,"preprocessed_bdd100k")
PREPROCESSED_BDD100K_VALID_DIR = os.path.join(PREPROCESSED_BDD100K_PATH, "valid")
PREPROCESSED_BDD100K_VALID_IMAGES_DIR = os.path.join(PREPROCESSED_BDD100K_VALID_DIR, "images")
PREPROCESSED_BDD100K_VALID_LABELS_DIR = os.path.join(PREPROCESSED_BDD100K_VALID_DIR, "labels")

PREPROCESSED_BDD100K_TRAIN_DIR = os.path.join(PREPROCESSED_BDD100K_PATH, "train")
PREPROCESSED_BDD100K_TRAIN_IMAGES_DIR = os.path.join(PREPROCESSED_BDD100K_TRAIN_DIR, "images")
PREPROCESSED_BDD100K_TRAIN_LABELS_DIR = os.path.join(PREPROCESSED_BDD100K_TRAIN_DIR, "labels")

# BDD100K_TRAIN_PATH = os.path.join(BDD100K_PATH,"train")
# BDD100K_TRAIN_IMAGE_PATH = os.path.join(BDD100K_TRAIN_PATH, "images")
# BDD100K_TRAIN_LABEL_PATH = os.path.join(BDD100K_TRAIN_PATH, "labels")
# BDD100K_JSON_TRAIN_LABEL_PATH = os.path.join(BDD100K_TRAIN_LABEL_PATH, "bdd100k_labels_images_train.json")

# BDD100K_VAL_PATH = os.path.join(BDD100K_PATH,"val")
# BDD100K_VAL_IMAGE_PATH = os.path.join(BDD100K_VAL_PATH, "images")
# BDD100K_VAL_LABEL_PATH = os.path.join(BDD100K_VAL_PATH, "labels")
# BDD100K_JSON_VAL_LABEL_PATH = os.path.join(BDD100K_VAL_LABEL_PATH, "bdd100k_labels_images_val.json")

# SAVE_PATH = os.path.join(ROOT_PATH,"result")

# BDD100K_VAL_LABEL_SAVE_PATH = os.path.join(SAVE_PATH,"val","labels")
# BDD100K_VAL_TRAIN_SAVE_PATH = os.path.join(SAVE_PATH,"train","labels")

"""
# 1: occluded car 
# 2: truncated car
# 3: occluded-truncated car

"""
img_size = (1280, 720)
categories = {'car': 0,
              'occluded car': 1,
              'truncated car':2,
              'occluded-truncated car':3,
              'bus': 4,
              'person': 5,
              'bike': 6,
              'truck': 7,
              'motor': 8,
              'train': 9,
              'bicyclist': 10,
              'motorcyclist': 11,
              'traffic sign': 12,
              'traffic light(red)': 13,
              'traffic light(yellow)': 14,
              'traffic light(green)': 15,
              'traffic light':16,
              }

image_name_prefixes = ("0","1","2","3","4","5","6","7","8","9","a","b","f")
img_size = (1280,720)

PATHS = {
    "/": ROOT,
    "/bdd100k": BDD100K_PATH,
    "/bdd100k/train" : BDD100K_TRAIN_DIR,
    "/bdd100k/train/images" : BDD100K_TRAIN_IMAGES_DIR,
    "/bdd100k/train/labels" : BDD100K_TRAIN_LABELS_DIR,
    "/bdd100k/train/labels/bdd100k_labels_images_train.json" : BDD100K_TRAIN_LABELS_JSON,
    
    "/bdd100k/valid" : BDD100K_VALID_DIR,
    "/bdd100k/valid/images" : BDD100K_VALID_IMAGES_DIR,
    "/bdd100k/valid/labels" : BDD100K_VALID_LABELS_DIR,
    "/bdd100k/valid/labels/bdd100k_labels_images_val.json" : BDD100K_VALID_LABELS_JSON,

    "/preprocessed_bdd100k" : PREPROCESSED_BDD100K_PATH,
    "/preprocessed_bdd100k/valid" : PREPROCESSED_BDD100K_VALID_DIR,
    "/preprocessed_bdd100k/valid/images" : PREPROCESSED_BDD100K_VALID_IMAGES_DIR,
    "/preprocessed_bdd100k/valid/labels" : PREPROCESSED_BDD100K_VALID_LABELS_DIR,

    "/preprocessed_bdd100k/train" : PREPROCESSED_BDD100K_TRAIN_DIR,
    "/preprocessed_bdd100k/train/images" : PREPROCESSED_BDD100K_TRAIN_IMAGES_DIR,
    "/preprocessed_bdd100k/train/labels" : PREPROCESSED_BDD100K_TRAIN_LABELS_DIR,

}
