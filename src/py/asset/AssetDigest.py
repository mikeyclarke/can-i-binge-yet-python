from masonite.request import Request
from typing import Type, TypeVar
import json

T = TypeVar('T', bound='AssetDigest')


class AssetDigest:
    def __init__(self, digest: dict[str, str]) -> None:
        self.__digest = digest

    @classmethod
    def create_from_request(cls: Type[T], request: Request) -> T:
        header = request.header('X-Asset-Digest')
        if header is None:
            return cls({})

        decoded = json.loads(header)
        digest = decoded if isinstance(decoded, dict) else {}
        return cls(digest)

    def has(self, filename: str) -> bool:
        return filename in self.__digest

    def get(self, filename: str) -> str:
        return self.__digest[filename]
