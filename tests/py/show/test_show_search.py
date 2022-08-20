from datetime import datetime
from src.py.show import ShowImageFormatter, ShowSearch
from src.py.themoviedb import TheMovieDbClient
from unittest.mock import create_autospec, call
from flag import flag


class TestShowSearch:
    def setup_method(self) -> None:
        self.__show_image_formatter = create_autospec(ShowImageFormatter)
        self.__tmdb_client = create_autospec(TheMovieDbClient)

        self.__show_search = ShowSearch(
            self.__show_image_formatter,
            self.__tmdb_client
        )

    def test_search(self) -> None:
        search_token = 'loot'

        response_body = {
            'results': [
                {
                    'backdrop_path': '/15boPorcwy0wOZKFwQtCBdYdaB2.jpg',
                    'first_air_date': '2022-06-23',
                    'genre_ids': [
                        35
                    ],
                    'id': 197449,
                    'name': 'Loot',
                    'origin_country': [
                        'US'
                    ],
                    'original_language': 'en',
                    'original_name': 'Loot',
                    'overview': 'After divorcing her husband of 20 years, Molly Novak must figure out what to do …',
                    'popularity': 34.733,
                    'poster_path': '/jf9EyK7KgHIAzpOEVujAFScUkcW.jpg',
                    'vote_average': 7.4,
                    'vote_count': 15
                },
                {
                    'backdrop_path': '/r3U05Qw2TUIDOpdwlt1SKcYL9v9.jpg',
                    'first_air_date': '2022-05-15',
                    'genre_ids': [
                        99
                    ],
                    'id': 204039,
                    'name': 'Loot - Blood Treasure',
                    'origin_country': [
                        'AU'
                    ],
                    'original_language': 'en',
                    'original_name': 'Loot - Blood Treasure',
                    'overview': 'This series documents how the trade in stolen antiquities and art has become a …',
                    'popularity': 0.801,
                    'poster_path': None,
                    'vote_average': 0,
                    'vote_count': 0
                },
                {
                    'backdrop_path': '/zXO6w3OGTBUhwSkF1GFu0j5JuNM.jpg',
                    'first_air_date': '2018-12-25',
                    'genre_ids': [
                        99
                    ],
                    'id': 156200,
                    'name': 'Hard Looters',
                    'origin_country': [
                        'FR'
                    ],
                    'original_language': 'fr',
                    'original_name': 'Hard Looters',
                    'overview': '',
                    'popularity': 0.6,
                    'poster_path': '/4XU5Jr49lXhz0sTdttfphs52WY5.jpg',
                    'vote_average': 0,
                    'vote_count': 0
                },
                {
                    'backdrop_path': None,
                    'first_air_date': '',
                    'genre_ids': [],
                    'id': 38900,
                    'name': 'Looteri Dulhan',
                    'origin_country': [
                        'IO'
                    ],
                    'original_language': 'en',
                    'original_name': 'Looteri Dulhan',
                    'overview': 'Looteri Dulhan was a unique fiction serial in Imagine TV. It is basically the …',
                    'popularity': 0.6,
                    'poster_path': None,
                    'vote_average': 0,
                    'vote_count': 0
                }
            ],
            'page': 1,
            'total_pages': 1,
            'total_results': 4,
        }

        self.__tmdb_client.search_shows.return_value = response_body
        self.__show_image_formatter.format.side_effect = [
            '197449-poster',
            '156200-poster',
        ]

        expected = {
            'page': response_body['page'],
            'shows': [
                {
                    'tmdb_show_id': response_body['results'][0]['id'],
                    'title': response_body['results'][0]['name'],
                    'countries_emoji': [flag(code) for code in response_body['results'][0]['origin_country']],
                    'year': datetime.strptime(response_body['results'][0]['first_air_date'], '%Y-%m-%d').year,
                    'overview': response_body['results'][0]['overview'],
                    'poster_image': '197449-poster',
                },
                {
                    'tmdb_show_id': response_body['results'][1]['id'],
                    'title': response_body['results'][1]['name'],
                    'countries_emoji': [flag(code) for code in response_body['results'][1]['origin_country']],
                    'year': datetime.strptime(response_body['results'][1]['first_air_date'], '%Y-%m-%d').year,
                    'overview': response_body['results'][1]['overview'],
                    'poster_image': None,
                },
                {
                    'tmdb_show_id': response_body['results'][2]['id'],
                    'title': response_body['results'][2]['name'],
                    'countries_emoji': [flag(code) for code in response_body['results'][2]['origin_country']],
                    'year': datetime.strptime(response_body['results'][2]['first_air_date'], '%Y-%m-%d').year,
                    'overview': response_body['results'][2]['overview'],
                    'poster_image': '156200-poster',
                },
                {
                    'tmdb_show_id': response_body['results'][3]['id'],
                    'title': response_body['results'][3]['name'],
                    'countries_emoji': [flag(code) for code in response_body['results'][3]['origin_country']],
                    'year': None,
                    'overview': response_body['results'][3]['overview'],
                    'poster_image': None,
                },
            ],
            'total_results': response_body['total_results'],
            'total_pages': response_body['total_pages'],
        }

        result = self.__show_search.search(search_token)

        self.__tmdb_client.search_shows.assert_called_once_with(search_token, 1)
        self.__show_image_formatter.format.assert_has_calls([
            call('poster', response_body['results'][0]['poster_path']),
            call('poster', response_body['results'][2]['poster_path']),
        ])

        assert expected == result
