import os


def current_path(filename=__file__):
    pth, _ = os.path.split(os.path.abspath(filename))
    return pth


def stream_data(filepath):
    path_to_data = filepath + "/data.txt"
    with open(path_to_data, 'r') as data_file:
        lines = data_file.read().splitlines()
        for line in lines:
            yield line
