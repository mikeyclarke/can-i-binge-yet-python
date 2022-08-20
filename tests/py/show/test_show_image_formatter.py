from src.py.show import ShowImageFormatter
from src.py.themoviedb import TheMovieDbConfiguration
from unittest.mock import create_autospec


class TestShowImageFormatter:
    def setup_method(self) -> None:
        self.__tmdb_config = create_autospec(TheMovieDbConfiguration)

        self.__show_image_formatter = ShowImageFormatter(
            self.__tmdb_config
        )

    def test_format(self) -> None:
        image_type = 'poster'
        image_path = '/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg'

        image_base_url = 'https://image.tmdb.org/t/p/'
        sizes = [
            'w92',
            'w154',
            'w185',
            'w342',
            'w500',
            'w780',
            'original',
        ]

        self.__tmdb_config.get_image_base_url.return_value = image_base_url
        self.__tmdb_config.get_image_sizes.return_value = sizes

        srcsets = [
            'https://image.tmdb.org/t/p/w92/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 92w',
            'https://image.tmdb.org/t/p/w154/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 154w',
            'https://image.tmdb.org/t/p/w185/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 185w',
            'https://image.tmdb.org/t/p/w342/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 342w',
            'https://image.tmdb.org/t/p/w500/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 500w',
            'https://image.tmdb.org/t/p/w780/bfxwMdQyJc0CL24m5VjtWAN30mt.jpg 780w',
        ]

        expected = {
            'default': srcsets[-1].split(' ')[0],
            'srcset': ', '.join(srcsets),
        }

        result = self.__show_image_formatter.format(image_type, image_path)

        self.__tmdb_config.get_image_base_url.assert_called_once()
        self.__tmdb_config.get_image_sizes.assert_called_once_with(image_type)

        assert expected == result
