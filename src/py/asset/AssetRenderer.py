from masonite.configuration.Configuration import Configuration
from masonite.request import Request
from .AssetDigest import AssetDigest
from .AssetManifest import AssetManifest
from src.py.file import FileReader
from src.py.id_generator import AlphaNumericIdGenerator


class AssetRenderer:
    def __init__(
        self,
        asset_manifest: AssetManifest,
        config: Configuration,
        file_reader: FileReader,
        id_generator: AlphaNumericIdGenerator
    ) -> None:
        self.__asset_manifest = asset_manifest
        self.__config = config
        self.__file_reader = file_reader
        self.__id_generator = id_generator

    def get_asset_html(self, request: Request, filename: str, asset_type: str) -> str:
        asset_digest = AssetDigest.create_from_request(request)

        asset_url = self.__asset_manifest.get_asset_url(filename)

        if asset_digest.has(filename) and asset_digest.get(filename) == asset_url:
            return self.__format_external_resource_html(asset_url, asset_type)

        asset_directory = self.__config.get('application.asset_directory')
        asset_path = f'{asset_directory}{asset_url}'
        content = self.__file_reader.read(asset_path)

        return self.__format_inline_html(request, filename, asset_url, content, asset_type)

    def __format_inline_html(self, request: Request, filename: str, url: str, content: str, asset_type: str) -> str:
        match asset_type:
            case 'css':
                stylesheet_id = self.__id_generator.generate(8)
                request.load_params({'cacheable_stylesheets': {
                    stylesheet_id: {
                        'bundle': filename,
                        'src': url,
                    }
                }})
                return f'<style id="{stylesheet_id}">{content}</style>'
            case 'js':
                enclosing_tags = (f'<cacheable-asset src="{url}" bundle="{filename}">', '</cacheable-asset>')
                return f'{enclosing_tags[0]}<script>{content}</script>{enclosing_tags[1]}'
            case _:
                raise RuntimeError('Unsupported asset type')

    def __format_external_resource_html(self, url: str, asset_type: str) -> str:
        match asset_type:
            case 'css':
                return f'<link rel="stylesheet" href="{url}">'
            case 'js':
                return f'<script src="{url}"></script>'
            case _:
                raise RuntimeError('Unsupported asset type')
