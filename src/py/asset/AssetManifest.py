from masonite.configuration.Configuration import Configuration
from os import path
from .exceptions import AssetNotFoundError
import json


class AssetManifest:
    def __init__(self, config: Configuration) -> None:
        self.__config = config

    def get_asset_url(self, filename: str) -> str:
        return self.__get_from_manifest(filename)

    def __get_from_manifest(self, filename: str) -> str:
        manifest_path = self.__config.get('application.asset_manifest_path')
        if not isinstance(manifest_path, str):
            raise TypeError('Application configuration entry `ASSET_MANIFEST_PATH` must be a string')

        if not path.exists(manifest_path):
            raise RuntimeError(f'Asset manifest does not exist at {manifest_path}')

        manifest_data: dict[str, str] = {}
        with open(manifest_path, 'r') as file:
            manifest_data = json.load(file)

        if filename not in manifest_data:
            raise AssetNotFoundError()

        return manifest_data[filename]
