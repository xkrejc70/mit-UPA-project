import os, io, shutil

def curr_dir():
    return os.path.dirname(os.path.realpath(__file__))

def project_dir():
    return os.path.dirname(curr_dir())

def data_dir():
    return os.path.join(project_dir(), "data")

def static_data_dir():
    return os.path.join(project_dir(), "data_static")

def delete_dir_content(dir_path):
    for filename in os.listdir(dir_path):
        if filename != ".gitkeep":
            file_path = os.path.join(dir_path, filename)
            try:
                os.unlink(file_path)
            except:
                pass

def write_stringio(output : io.StringIO, filename):
    with open(os.path.join(data_dir(), f"{filename}.csv"), 'w') as f:
        output.seek(0)
        shutil.copyfileobj(output, f)

#EXAMPLE of a function that makes selected column look better
def all_before_bracket(text):
    if text is None or text.strip() == "":
        return text
    text = text.split('(')[0].replace("až", "-").replace(" ", "").replace("Od95", "95+")
    if text.startswith("5-"):
        text = "0"+text
    return text
