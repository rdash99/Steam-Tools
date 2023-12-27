import shutil
import os


def setup(id):
    cleanup(id)
    if os.path.exists(str(id)):
        pass
    else:
        os.makedirs(str(id))


def cleanup(file_path):
    # delete the directory
    try:
        shutil.rmtree(str(file_path))
    except:
        pass
