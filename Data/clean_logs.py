import os
import shutil

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
shutil.rmtree(LOG_PATH)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)