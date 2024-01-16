import os
from .config import WEB_RUN_BASE_DIR

def createRunDir(run_dir_name):
    run_dir_path = os.path.join(WEB_RUN_BASE_DIR, run_dir_name)
    if not os.path.exists(run_dir_path):
        os.makedirs(run_dir_path)
        return run_dir_path
    else:
        return ""