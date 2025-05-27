import os

def get_image_paths(directory="./clipsearch/images"):
    supported_exts = [".jpg", ".jpeg", ".png"]
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.splitext(f)[1].lower() in supported_exts
    ]
