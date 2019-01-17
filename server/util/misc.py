import os
import uuid

from PIL import Image

def generate_random_filename():
    temp = uuid.uuid4().urn
    return temp[9:]

def create_thumbnail(filename, size):
    file, ext = os.path.splitext(filename)

    image = Image.open(filename)
    image.thumbnail((size, size))
    image.save(file + "_thumbnail" + ext, ext[1:])
