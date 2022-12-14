from datetime import date, timedelta
from html import escape
from babel.dates import format_date
from functools import reduce
from src.py.url import SlugGenerator
from .SeasonEpisodesFormatter import SeasonEpisodesFormatter, SeasonEpisode
from .ShowImageFormatter import ShowImageFormatter, ShowImage
from flag import flag
from typing import Any, Optional, TypedDict
import re


class Season(TypedDict):
    name: str
    air_date: Optional[date]
    year: Optional[int]
    episode_count: int
    episodes: Optional[list[SeasonEpisode]]
    season_number: int
    has_started: bool


class Network(TypedDict):
    logo: Optional[ShowImage]
    name: str


class ShowPageResult(TypedDict):
    tmdb_id: int
    title: str
    tagline: Optional[str]
    countries_emoji: list[str]
    overview: Optional[str]
    poster_image: Optional[ShowImage]
    backdrop_image: Optional[ShowImage]
    slug: str
    url_path: str
    status_text: str
    networks: list[Network]
    seasons: list[Season]
    air_dates_display: Optional[str]
    has_ended: bool


def format_friendly_date(air_date: date) -> str:
    week_from_now = date.today() + timedelta(days=7)

    if air_date < week_from_now:
        pattern = "'|start_strong|'EEEE'|end_strong|'"
    else:
        pattern = 'EEEE'

    pattern += ', MMMM d'

    if air_date.year != date.today().year:
        pattern += ', yyyy'

    return escape(format_date(air_date, pattern))


class ShowPageFormatter:
    SHOW_ENDED_STATUSES = ['Cancelled', 'Canceled', 'Ended']

    def __init__(
        self,
        season_episodes_formatter: SeasonEpisodesFormatter,
        show_image_formatter: ShowImageFormatter,
        slug_generator: SlugGenerator
    ) -> None:
        self.__season_episodes_formatter = season_episodes_formatter
        self.__show_image_formatter = show_image_formatter
        self.__slug_generator = slug_generator

    def format(self, show: dict[str, Any]) -> ShowPageResult:
        tmdb_id = show['id']
        slug = self.__slug_generator.generate(show['name'])

        seasons: list[Season] = []
        today = date.today()
        if show['seasons'] is not None:
            for season in show['seasons']:
                episodes = None
                if show['last_season'] is not None and show['last_season']['season_number'] == season['season_number']:
                    episodes = self.__season_episodes_formatter.format(show['last_season']['episodes'])

                air_date = None
                has_started = False
                if season['air_date'] is not None and season['air_date'] != '':
                    air_date = date.fromisoformat(season['air_date'])
                    has_started = air_date < today

                seasons.append({
                    'name': season['name'],
                    'air_date': air_date,
                    'year': air_date.year if air_date is not None else None,
                    'episodes': episodes,
                    'episode_count': season['episode_count'],
                    'season_number': season['season_number'],
                    'has_started': has_started,
                })

            seasons.reverse()

        networks: list[Network] = []
        for network in show['networks']:
            logo_image = None
            if network['logo_path'] is not None and network['logo_path'] != '':
                logo_image = self.__show_image_formatter.format('logo', network['logo_path'], 'smallest')
                logo_image['default'] = re.sub(r'/w[0-9]+/', '/h60/', logo_image['default'])

            networks.append({
                'name': network['name'],
                'logo': logo_image,
            })

        has_ended = self.__has_ended(show)
        last_season = seasons[0] if seasons else None

        last_episode = None
        if last_season is not None and last_season['episodes'] is not None:
            last_episode = last_season['episodes'][-1]

        formatted: ShowPageResult = {
            'tmdb_id': tmdb_id,
            'title': show['name'],
            'tagline': show['tagline'],
            'countries_emoji': [flag(code) for code in show['origin_country']],
            'overview': show['overview'] or None,
            'poster_image': None,
            'backdrop_image': None,
            'slug': slug,
            'url_path': f'{tmdb_id}-{slug}',
            'status_text': self.__get_status_text(last_season, last_episode),
            'networks': networks,
            'seasons': seasons,
            'air_dates_display': self.__get_air_dates(show, last_episode, has_ended),
            'has_ended': has_ended,
        }

        if show['poster_path'] is not None:
            formatted['poster_image'] = self.__show_image_formatter.format('poster', show['poster_path'])

        if show['backdrop_path'] is not None:
            formatted['backdrop_image'] = self.__show_image_formatter.format('backdrop', show['backdrop_path'])

        return formatted

    def __has_ended(self, show: dict[str, Any]) -> bool:
        return 'status' in show and show['status'] in self.SHOW_ENDED_STATUSES

    def __get_air_dates(
        self,
        show: dict[str, Any],
        last_episode: Optional[SeasonEpisode],
        has_ended: bool
    ) -> Optional[str]:
        start_year = None
        if show['first_air_date'] is not None and show['first_air_date'] != '':
            start_year = date.fromisoformat(show['first_air_date']).year

        if start_year is None:
            return None

        if not has_ended:
            return f'{start_year} - present'

        if last_episode is None or last_episode['air_date'] is None:
            return f'{start_year} -'

        end_year = last_episode['air_date'].year
        if start_year == end_year:
            return str(start_year)

        return f'{start_year} - {end_year}'

    def __get_status_text(self, last_season: Optional[Season], last_episode: Optional[SeasonEpisode]) -> str:
        if last_season is None or last_episode is None or last_season['air_date'] is None:
            return 'We’re unable to obtain the air dates of this show right now'

        season_number = last_season['season_number']
        premiere_date = format_friendly_date(last_season['air_date'])

        last_episode_date = None
        if last_episode['air_date'] is not None:
            last_episode_date = format_friendly_date(last_episode['air_date'])

        unaired_episodes = reduce(
            lambda carry, episode: carry + 1 if not episode['has_aired'] else carry,
            last_season['episodes'] if last_season['episodes'] is not None else [],
            0
        )

        if last_episode['has_aired']:
            return f'Season {season_number} has concluded and all episodes have aired'

        if last_season['has_started']:
            episodes_label = 'episodes' if unaired_episodes != 1 else 'episode'

            if last_episode_date is None:
                return (
                    f'Season {season_number} has {unaired_episodes} {episodes_label} left but its '
                    'conclusion date is currently unknown'
                )

            return f'Season {season_number} has {unaired_episodes} {episodes_label} left and concludes {last_episode_date}'

        if last_episode_date is None:
            return f'Season {season_number} premieres {premiere_date} but its conclusion date is currently unknown'

        return f'Season {season_number} premieres {premiere_date} and concludes {last_episode_date}'
