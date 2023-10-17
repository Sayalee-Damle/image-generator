import uuid
import requests
from asyncer import asyncify

from image_generator_bot.config import cfg

def download_image_file(image_url, image_name):
    img_data = requests.get(image_url).content
    path = cfg.image_path / uuid.uuid5(name = f"{image_name}.jpg")
    with open(path, 'wb') as handler:
        handler.write(img_data)

async def download_image_dalle(image_url, image_name):
    return await asyncify(download_image_file)(image_url, image_name)