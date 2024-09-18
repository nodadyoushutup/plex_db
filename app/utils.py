import os
import mimetypes
import requests
from PIL import Image
import io
from .config import static, baseurl, token

def build_url(key):
    return f"{baseurl}{key}?X-Plex-Token={token}"

def download_image(url, path, max_width=None, max_height=None):
    response = requests.get(url)
    if response.status_code == 200:
        create_dir(path)    
        save(response, path, max_width=250)
    else:
        print(f"Failed to download image, status code: {response.status_code}")

def create_dir(path):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)

def get_extension(response):
    content_type = response.headers.get('Content-Type')
    if not content_type:
        print("Could not determine content type.")
        return
    extension = mimetypes.guess_extension(content_type)
    if not extension:
        print("Could not guess extension from content type.")
        return 
    return extension

def resize(img, max_width=None, max_height=None):
    original_width, original_height = img.size
    if max_width and max_height:
        return img.resize((max_width, max_height))
    elif max_width:
        new_height = int((max_width / original_width) * original_height)
        return img.resize((max_width, new_height))
    elif max_height:
        new_width = int((max_height / original_height) * original_width)
        return img.resize((new_width, max_height))
    return img
    
def save(response, path, max_width=None, max_height=None):
    extension = get_extension(response)
    if extension:
        img = Image.open(io.BytesIO(response.content))
        img = resize(img, max_width, max_height)
        file_path = static + path + extension
        img.save(file_path)
        print(f"Image saved to {file_path}")
    print("Could not save image")
    return 