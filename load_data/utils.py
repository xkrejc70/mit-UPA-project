# utils.py
# Proj: UPA 2021
# Authors: Matěj Sojka (xsojka04), Matěj Kudera (xkuder04), Honza Krejčí (xkrejc70)
# Path and data manipulation utils

import os

# Current program path
def curr_dir():
    return os.path.dirname(os.path.realpath(__file__))

# Project folder path
def project_dir():
    return os.path.dirname(curr_dir())

# Path to save folder
def data_dir():
    return os.path.join(project_dir(), "data")

# Path to save folder
def extracted_data_dir():
    return os.path.join(project_dir(), "extracted_data")
    
# Path to save folder
def graphs_dir():
    return os.path.join(project_dir(), "graphs")

# Path to static data sert
def static_data_dir():
    return os.path.join(project_dir(), "data_static")

# Delete all old data files in data folder
def delete_dir_content(dir_path):
    for filename in os.listdir(dir_path):
        if filename != ".gitkeep":
            file_path = os.path.join(dir_path, filename)
            try:
                os.unlink(file_path)
            except:
                pass

################  Column transformation functions ##############

# Replace data in format 55 až 60 (více nebo rovno 55 a méně než 60) to frendlier format 55-59 
def all_before_bracket(text):
    if text is None or text.strip() == "":
        return text
    text = text.split('(')[0].replace("až", "-").replace(" ", "").replace("Od95", "95+")
    if text.startswith("5-"):
        text = "0"+text
    return text

# Replace gender descriptor: 1 - M (male), 2 - Z (female)
def rename_gender(text):
    if text == "1":
        return "M"
    elif text == "2":
        return "Z"

def path_extracted_data(name):
    return os.path.join(extracted_data_dir(), f"{name}.csv")

def path_part1(name):
    suffix = "part1"
    return os.path.join(extracted_data_dir(), f"{name}_{suffix}.csv")

def path_part2(name):
    suffix = "part2"
    return os.path.join(extracted_data_dir(), f"{name}_{suffix}.csv")

# END utils.py