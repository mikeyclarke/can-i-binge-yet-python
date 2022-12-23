from masonite.configuration.Configuration import Configuration
from masonite.request import Request
from src.py.asset import AssetManifest, AssetRenderer
from src.py.file import FileReader
from src.py.id_generator import AlphaNumericIdGenerator
from unittest.mock import create_autospec, call


class TestAssetRenderer:
    def setup_method(self) -> None:
        self.__asset_manifest = create_autospec(AssetManifest)
        self.__config = create_autospec(Configuration)
        self.__file_reader = create_autospec(FileReader)
        self.__id_generator = create_autospec(AlphaNumericIdGenerator)

        self.__asset_renderer = AssetRenderer(
            self.__asset_manifest,
            self.__config,
            self.__file_reader,
            self.__id_generator
        )

    def test_get_asset_html_with_css_asset_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"app.css": "/compiled/app.abcd1234.css"}'})
        filename = 'app.css'
        asset_type = 'css'

        url = '/compiled/app.abcd1234.css'

        self.__asset_manifest.get_asset_url.return_value = url

        expected = f'<link rel="stylesheet" href="{url}">'

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)

        assert expected == result

    def test_get_asset_html_with_css_asset_not_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"foo.css": "/compiled/foo.abcd1234.css"}'})
        filename = 'app.css'
        asset_type = 'css'

        url = '/compiled/app.abcd1234.css'
        asset_directory = 'public'
        content = '.foo { color: red; }'
        stylesheet_id = 'h4mEg08q'

        self.__asset_manifest.get_asset_url.return_value = url
        self.__config.get.return_value = asset_directory
        self.__file_reader.read.return_value = content
        self.__id_generator.generate.return_value = stylesheet_id

        expected = f'<style id="{stylesheet_id}">{content}</style>'
        expected_request_param = {
            stylesheet_id: {
                'bundle': filename,
                'src': url,
            }
        }

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)
        self.__config.get.assert_called_once_with('application.asset_directory')
        self.__file_reader.read.assert_called_once_with(f'{asset_directory}{url}')
        self.__id_generator.generate.assert_called_once_with(8)

        assert expected == result
        assert expected_request_param == request.param('cacheable_stylesheets')

    def test_get_asset_html_with_outdated_css_asset_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"app.css": "/compiled/app.abcd1234.css"}'})
        filename = 'app.css'
        asset_type = 'css'

        url = '/compiled/app.efgh5678.css'
        asset_directory = 'public'
        content = '.foo { color: red; }'
        stylesheet_id = 'h4mEg08q'

        self.__asset_manifest.get_asset_url.return_value = url
        self.__config.get.return_value = asset_directory
        self.__file_reader.read.return_value = content
        self.__id_generator.generate.return_value = stylesheet_id

        expected = f'<style id="{stylesheet_id}">{content}</style>'
        expected_request_param = {
            stylesheet_id: {
                'bundle': filename,
                'src': url,
            }
        }

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)
        self.__config.get.assert_called_once_with('application.asset_directory')
        self.__file_reader.read.assert_called_once_with(f'{asset_directory}{url}')
        self.__id_generator.generate.assert_called_once_with(8)

        assert expected == result
        assert expected_request_param == request.param('cacheable_stylesheets')

    def test_get_asset_html_with_js_asset_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"app.js": "/compiled/app.abcd1234.js"}'})
        filename = 'app.js'
        asset_type = 'js'

        url = '/compiled/app.abcd1234.js'

        self.__asset_manifest.get_asset_url.return_value = url

        expected = f'<script src="{url}"></script>'

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)

        assert expected == result

    def test_get_asset_html_with_js_asset_not_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"foo.js": "/compiled/foo.abcd1234.js"}'})
        filename = 'app.js'
        asset_type = 'js'

        url = '/compiled/app.abcd1234.js'
        asset_directory = 'public'
        content = 'alert("Foo");'

        self.__asset_manifest.get_asset_url.return_value = url
        self.__config.get.return_value = asset_directory
        self.__file_reader.read.return_value = content

        expected = f'<cacheable-asset src="{url}" bundle="{filename}"><script>{content}</script></cacheable-asset>'

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)
        self.__config.get.assert_called_once_with('application.asset_directory')
        self.__file_reader.read.assert_called_once_with(f'{asset_directory}{url}')

        assert expected == result

    def test_get_asset_html_with_outdated_js_asset_in_request_header(self) -> None:
        request = Request({'HTTP_X_ASSET_DIGEST': '{"app.js": "/compiled/app.abcd1234.js"}'})
        filename = 'app.js'
        asset_type = 'js'

        url = '/compiled/app.efgh5678.js'
        asset_directory = 'public'
        content = 'alert("Foo");'

        self.__asset_manifest.get_asset_url.return_value = url
        self.__config.get.return_value = asset_directory
        self.__file_reader.read.return_value = content

        expected = f'<cacheable-asset src="{url}" bundle="{filename}"><script>{content}</script></cacheable-asset>'

        result = self.__asset_renderer.get_asset_html(request, filename, asset_type)

        self.__asset_manifest.get_asset_url.assert_called_once_with(filename)
        self.__config.get.assert_called_once_with('application.asset_directory')
        self.__file_reader.read.assert_called_once_with(f'{asset_directory}{url}')

        assert expected == result
