from PIL import Image
from tempfile import NamedTemporaryFile
import os

def is_image_compressable(path):
    ACCEPTABLE = [".jpg", ".png"]
    ext = os.path.splitext(path)[1].lower()
    return ext in ACCEPTABLE

def _detect_valid_format(path):
    ext = os.path.splitext(path)[1].lower()
    return {".jpg" : "jpeg", ".png" : "png"}.get(ext)

def compress(path):
    im = Image.open(path)
    size = (1024, 1024)
    im.thumbnail(size, Image.ANTIALIAS)
    with NamedTemporaryFile(delete=False) as temp:
        im.save(temp, _detect_valid_format(path))
        return temp
