import os
import random
import shutil
from os.path import join as joinpath

import requests

FIRST_COMICS_NUMBER = 1
COMICS_DATA_URL = 'https://xkcd.com/{}/info.0.json'
TMP_IMAGE_PATH = 'tmp'


def fetch_comics_data(number):
    if number is not None:
        url = COMICS_DATA_URL.format(number)
    else:
        url = COMICS_DATA_URL.format('')

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_comics_quantity():
    return fetch_comics_data(None)['num']


def save_image(url):
    filename = 'tmp-image{}'.format(get_file_extension(url))
    save_path = joinpath(TMP_IMAGE_PATH, filename)
    os.makedirs(TMP_IMAGE_PATH, exist_ok=True)

    with open(save_path, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

    return save_path


def get_file_extension(path):
    return os.path.splitext(path)[1]


def get_comics_image_data():
    comics_number = random.randint(FIRST_COMICS_NUMBER, get_comics_quantity())
    comics_data = fetch_comics_data(comics_number)

    saved_image_path = save_image(comics_data['img'])

    return {'path': saved_image_path, 'comment': comics_data['alt']}


def delete_temp_dir():
    shutil.rmtree(TMP_IMAGE_PATH)
