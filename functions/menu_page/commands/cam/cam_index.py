import os


def read_cam_index():
    file_path = 'save_config_txt/chosen_cam.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            cam_index = int(file.read().strip())
        return cam_index
    else:
        return None