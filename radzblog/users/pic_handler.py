"""
------------------------------------------ Imports ------------------------------------------
"""
import os

from flask import current_app
from PIL import Image


"""
-------------------------------------- Picture Handler --------------------------------------
"""
def add_profile_pic(username, pic_data):
    ext = pic_data.filename.split(".")[-1]
    filename = str(username) + "." + ext

    filepath = os.path.join(current_app.root_path, 'static/pictures', filename)

    pic_size = (200, 200)

    pic = Image.open(pic_data)
    pic.thumbnail(pic_size)
    pic.save(filepath)

    return filename