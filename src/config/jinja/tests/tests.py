import os


def file_exists(path):
    return os.path.exists(path)


def is_dir(path):
    return os.path.isdir(path)
