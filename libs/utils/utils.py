import os
from pathlib import Path


def validate_file_exists_and_is_not_empty(file_path):
    if os.path.exists(file_path) \
       and Path(file_path).is_file() \
       and Path(file_path).stat().st_size != 0:
        return True
    else:
        return False
