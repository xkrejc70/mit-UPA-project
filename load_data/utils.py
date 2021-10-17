import os, io, shutil

def curr_dir():
    return os.path.dirname(os.path.realpath(__file__))

def project_dir():
    return os.path.dirname(curr_dir())

def data_dir():
    return os.path.join(project_dir(), "data")

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