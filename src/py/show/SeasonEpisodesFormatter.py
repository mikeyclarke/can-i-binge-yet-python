from datetime import date
from typing import Any, Optional, TypedDict


class SeasonEpisode(TypedDict):
    name: str
    number: int
    air_date: Optional[date]
    has_aired: bool


class SeasonEpisodesFormatter:
    def format(self, episodes: list[dict[str, Any]]) -> list[SeasonEpisode]:
        today = date.today()
        formatted = []

        for episode in episodes:
            air_date = None
            if episode['air_date'] is not None:
                air_date = date.fromisoformat(episode['air_date'])

            formatted_episode: SeasonEpisode = {
                'name': episode['name'],
                'number': episode['episode_number'],
                'air_date': air_date,
                'has_aired': air_date < today if air_date is not None else False,
            }

            formatted.append(formatted_episode)

        return formatted
