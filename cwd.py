# get cwd, file paths and such
# note: for use in ONE dir

from pathlib import Path
import os 

def cwd():
    """
    Summary:
        Function parses cwd
    
    Returns:
        path: cwd
    """
    cwd = Path(__file__).absolute().parent
    return cwd

def file_path(file_name):
    file_path = os.path.join(cwd(), file_name)
    return file_path
    