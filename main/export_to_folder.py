import os
import shutil

def export_file(file_name, origin_folder, destination_folder):
    os.rename(f"{origin_folder}/{file_name}", f"{destination_folder}/{file_name}")
    shutil.move(f"{origin_folder}/{file_name}", f"{destination_folder}/{file_name}")
    os.replace(f"{origin_folder}/{file_name}", f"{destination_folder}/{file_name}")