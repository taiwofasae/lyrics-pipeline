import json
from common import log, env
import os
import shutil
from pathlib import Path


#storage_folder = os.path.join(Path(__file__).resolve().parent.parent, env.get_key('DATA_DIR'))

class File:
    
    def __init__(self, data_path : str) -> None:
        self.data_path = data_path
        
    def get_full_path(self, file_path : str) -> str:
        return os.path.join(self.data_path, file_path).replace("\\","/")
    
    def __call__(self, file_path : str) -> str:
        return self.get_full_path(file_path=file_path)
    
def upload_file(file_name, json_data):
    log.info("writing to file: {0}".format(file_name))

    with open(file_name, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False)

def download_file(file_name, json_deserialize=True):

    try:
        with open(file_name, 'r') as f:
            if json_deserialize:
                json_data = json.load(f)
                return json_data
            return f.read()
    except Exception as e:
        log.error(e)
        log.info("file reading failed.")
    
    return None

def copy(source, dest):
    shutil.copyfile(source, dest)

def file_exists(file_name):

    return os.path.exists(file_name)


def make_directory(folder):

    if not os.path.exists(folder):
        os.makedirs(folder)

def make_directory_from_filepath(filepath):

    dir_path = os.path.dirname(filepath)
    make_directory(dir_path)

def delete_file(filepath):
    log.info("deleting file {}".format(filepath))
    os.remove(filepath)