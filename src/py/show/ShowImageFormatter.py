from src.py.themoviedb import TheMovieDbConfiguration
from typing import TypedDict


class ShowImage(TypedDict):
    default: str
    srcset: str


class ShowImageFormatter:
    def __init__(self, tmdb_config: TheMovieDbConfiguration):
        self.__tmdb_config = tmdb_config

    def format(self, image_type: str, image_path: str) -> ShowImage:
        images_base_url = self.__tmdb_config.get_image_base_url()

        default = ''
        srcsets = []

        sizes = self.__tmdb_config.get_image_sizes(image_type)
        for size in sizes:
            if size.startswith('w'):
                src = f'{images_base_url}{size}{image_path}'
                size_pixels = size[1::]
                srcsets.append(f'{src} {size_pixels}w')
                default = src

        result: ShowImage = {
            'default': default,
            'srcset': ', '.join(srcsets),
        }

        return result
