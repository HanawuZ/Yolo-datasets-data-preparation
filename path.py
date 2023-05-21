import os
from pathlib import Path

ROOT = Path(__file__).parent

DATASETS_PATH = os.path.join(ROOT,"datasets")

DATA_CONFIG = os.path.join(ROOT,"config","data.yaml")

path = {
    "/": ROOT,
    "/datasets": DATASETS_PATH,
    "/config/data.yml": DATA_CONFIG
}