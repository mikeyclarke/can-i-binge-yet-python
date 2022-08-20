from masonite.cache import Cache
from masonite.cache.drivers import RedisDriver
from src.py.show import ShowImageFormatter, TrendingShows
from src.py.themoviedb import TheMovieDbClient
from unittest.mock import create_autospec, call

shows = {
    'page': 1,
    'results': [
        {
            'adult': False,
            'backdrop_path': '/6KyJeOW7vTW0czdR0S6wzXAcfmw.jpg',
            'id': 90802,
            'name': 'The Sandman',
            'original_language': 'en',
            'original_name': 'The Sandman',
            'overview': 'After years of imprisonment, Morpheus — the King of Dreams — embarks on a journey …',
            'poster_path': '/q54qEgagGOYCq5D1903eBVMNkbo.jpg',
            'media_type': 'tv',
            'genre_ids': [
                10765,
                18
            ],
            'popularity': 2569.454,
            'first_air_date': '2022-08-05',
            'vote_average': 8.163,
            'vote_count': 315,
            'origin_country': [
                'US'
            ]
        },
        {
            'adult': False,
            'backdrop_path': '/56v2KjBlU4XaOv9rVYEQypROD7P.jpg',
            'id': 66732,
            'name': 'Stranger Things',
            'original_language': 'en',
            'original_name': 'Stranger Things',
            'overview': 'When a young boy vanishes, a small town uncovers a mystery involving secret …',
            'poster_path': '/49WJfeN0moxb9IPfGn8AIqMGskD.jpg',
            'media_type': 'tv',
            'genre_ids': [
                18,
                10765,
                9648
            ],
            'popularity': 1625.948,
            'first_air_date': '2016-07-15',
            'vote_average': 8.642,
            'vote_count': 12921,
            'origin_country': [
                'US'
            ]
        },
    ],
    'total_pages': 1000,
    'total_results': 20000
}

formatted_result = [
    {
        'tmdb_show_id': shows['results'][0]['id'],
        'title': shows['results'][0]['name'],
        'poster_image': f"{shows['results'][0]['id']}-poster",
    },
    {
        'tmdb_show_id': shows['results'][1]['id'],
        'title': shows['results'][1]['name'],
        'poster_image': f"{shows['results'][1]['id']}-poster",
    },
]


class TestTrendingShows:
    def setup_method(self) -> None:
        self.__cache = create_autospec(Cache)
        self.__show_image_formatter = create_autospec(ShowImageFormatter)
        self.__tmdb_client = create_autospec(TheMovieDbClient)

        self.__trending_shows = TrendingShows(
            self.__cache,
            self.__show_image_formatter,
            self.__tmdb_client
        )

        self.__redis_driver = create_autospec(RedisDriver)

    def test_get_all_with_populated_cache(self) -> None:
        self.__cache.get_driver.return_value = self.__redis_driver
        self.__cache.get_config_options.return_value = {}
        self.__cache.has.return_value = True
        self.__cache.get.return_value = shows
        self.__show_image_formatter.format.side_effect = [
            f"{shows['results'][0]['id']}-poster",
            f"{shows['results'][1]['id']}-poster",
        ]

        result = self.__trending_shows.get_all()

        self.__cache.get_driver.assert_called_once()
        self.__cache.get_config_options.assert_called_once()
        self.__redis_driver.set_options.assert_called_once_with({})
        self.__redis_driver.get_connection.assert_called_once()
        self.__cache.has.assert_called_once_with(TrendingShows.CACHE_KEY)
        self.__cache.get.assert_called_once_with(TrendingShows.CACHE_KEY)
        self.__show_image_formatter.format.assert_has_calls([
            call('poster', shows['results'][0]['poster_path']),
            call('poster', shows['results'][1]['poster_path']),
        ])

        assert formatted_result == result

    def test_get_all_with_empty_cache(self) -> None:
        self.__cache.get_driver.return_value = self.__redis_driver
        self.__cache.get_config_options.return_value = {}
        self.__cache.has.return_value = False
        self.__tmdb_client.get_trending_shows.return_value = shows
        self.__show_image_formatter.format.side_effect = [
            f"{shows['results'][0]['id']}-poster",
            f"{shows['results'][1]['id']}-poster",
        ]

        result = self.__trending_shows.get_all()

        self.__cache.get_driver.assert_called_once()
        self.__cache.get_config_options.assert_called_once()
        self.__redis_driver.set_options.assert_called_once_with({})
        self.__redis_driver.get_connection.assert_called_once()
        self.__cache.has.assert_called_once_with(TrendingShows.CACHE_KEY)
        self.__tmdb_client.get_trending_shows.assert_called_once()
        self.__cache.put.assert_called_once_with(TrendingShows.CACHE_KEY, shows, seconds=TrendingShows.CACHE_LIFETIME)
        self.__show_image_formatter.format.assert_has_calls([
            call('poster', shows['results'][0]['poster_path']),
            call('poster', shows['results'][1]['poster_path']),
        ])

        assert formatted_result == result
