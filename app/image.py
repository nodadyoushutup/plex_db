import os
import mimetypes
import requests
from PIL import Image as PILImage
import io

from app.utils import create_dir, get_extension
from .config import static

class Image:
    def __init__(self, url, path) -> None:
        self._set_response(url)
        self._set_img()
        self._set_extension()
        self._set_path(path)

    def _set_img(self, max_width=None, max_height=None):
        self.img = PILImage.open(io.BytesIO(self.response.content))
        if self.img.mode != 'RGB':
            self.img = self.img.convert('RGB')
    
    def _set_response(self, url):
        self.response = requests.get(url)

    def _set_extension(self):
        self.extension = get_extension(self.response)

    def _set_path(self, path):
        self.path = static + path + self.extension

    def _resize(self, max_width=None, max_height=None):
        original_width, original_height = self.img.size
        if max_width and max_height:
            self.img = self.img.resize((max_width, max_height))
        elif max_width:
            new_height = int((max_width / original_width) * original_height)
            self.img = self.img.resize((max_width, new_height))
        elif max_height:
            new_width = int((max_height / original_height) * original_width)
            self.img = self.img.resize((new_width, max_height))
    
    def _save(self, force_ext=None, quality=None):
        if force_ext:
            if force_ext.lower() in ['jpg', 'jpeg']:
                format = 'JPEG'
                new_extension = ".jpg"
            else:
                format = force_ext.upper()
                new_extension = f".{force_ext.lower()}"
            self.path = self.path.rsplit('.', 1)[0] + new_extension
        else:
            format = self.extension.strip('.').upper()
        save_params = {}
        if format == 'JPEG':
            if quality and quality <= 95:
                save_params['quality'] = quality
            else:
                save_params['quality'] = 75
        self.img.save(self.path, format=format, **save_params)
        print(f"Image saved to {self.path}")

    def download(self, max_width=None, max_height=None, force_ext=None, quality=None):
        if self.response.status_code == 200:
            if max_width or max_height:
                self._resize(max_width, max_height)
            create_dir(self.path)
            self._save(force_ext, quality)
        else:
            print(f"Failed to download image, status code: {self.response.status_code}")

    