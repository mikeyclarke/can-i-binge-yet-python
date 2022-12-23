import AssetCache, {StorageUnavailableError} from 'asset/AssetCache';
import CachedAssetsCatalog from 'asset/CachedAssetsCatalog';

const mockIsAvailable = jest.fn();
const mockSet = jest.fn();
const mockGet = jest.fn();
jest.mock('asset/CachedAssetsCatalog', () => {
    return {
        default: jest.fn().mockImplementation(() => {
            return {
                isAvailable: mockIsAvailable,
                set: mockSet,
                get: mockGet,
            }
        })
    }
});

const mockCachesOpen = jest.fn();
window.caches = {
    delete: jest.fn(),
    has: jest.fn(),
    keys: jest.fn(),
    match: jest.fn(),
    open: mockCachesOpen,
};

const mockCachePut = jest.fn();
const mockCacheDelete = jest.fn();
const cacheMock = {
    put: mockCachePut,
    delete: mockCacheDelete,
}

beforeEach(() => {
    (<jest.Mock> CachedAssetsCatalog).mockClear();
    mockIsAvailable.mockClear();
    mockSet.mockClear();
    mockGet.mockClear();
});

test('Storage unavailable throws error', () => {
    const assetCache = new AssetCache();

    createCatalogIsAvailableExpectation(false);

    expect(async () => {
        await assetCache.cacheBundle('bar.css', '/foo/bar', '.foo { color: red; }', 'css');
    }).rejects.toThrow(StorageUnavailableError);
    expect(mockIsAvailable).toBeCalledTimes(1);
});

test('Does nothing if asset URL already cached', async () => {
    const bundle = 'bar.css';
    const url = '/foo/bar';
    const content = '.foo { color: red; }';
    const assetType = 'css';

    const assetCache = new AssetCache();

    createCatalogIsAvailableExpectation(true);
    createCatalogGetExpectation(url);

    await assetCache.cacheBundle(bundle, url, content, assetType);

    expect(mockIsAvailable).toBeCalledTimes(1);
    expect(mockGet).toBeCalledTimes(1);
    expect(mockGet).toBeCalledWith(bundle);
});

test('New version of asset is cached', async () => {
    const bundle = 'bar.css';
    const url = '/foo/bar.def456.css';
    const content = '.foo { color: red; }';
    const assetType = 'css';
    const bundlePreviousUrl = '/foo/bar.abc123.css';

    const assetCache = new AssetCache();
    const response = new Response(content, {
        status: 200,
        statusText: 'OK',
        headers: {
            'Content-Type': `text/css; charset="utf-8"`,
        },
    });

    createCatalogIsAvailableExpectation(true);
    createCatalogGetExpectation(bundlePreviousUrl);
    createCachesOpenExpectation(cacheMock);

    await assetCache.cacheBundle(bundle, url, content, assetType);

    expect(mockIsAvailable).toBeCalledTimes(1);
    expect(mockGet).toBeCalledTimes(1);
    expect(mockGet).toBeCalledWith(bundle);
    expect(mockCachesOpen).toBeCalledTimes(1);
    expect(mockCachesOpen).toBeCalledWith('assets-v1');
    expect(mockCacheDelete).toBeCalledTimes(1);
    expect(mockCacheDelete).toBeCalledWith(bundlePreviousUrl);
    expect(mockCachePut).toBeCalledTimes(1);
    expect(mockCachePut).toBeCalledWith(url, response);
    expect(mockSet).toBeCalledTimes(1);
    expect(mockSet).toBeCalledWith(bundle, url);
});

function createCatalogIsAvailableExpectation(value: boolean): void {
    mockIsAvailable.mockImplementation(async () => {
        return Promise.resolve(value);
    });
}

function createCatalogGetExpectation(value: null | string): void {
    mockGet.mockImplementation(async () => {
        return Promise.resolve(value);
    });
}

function createCachesOpenExpectation(value: any): void {
    mockCachesOpen.mockImplementation(async () => {
        return Promise.resolve(value);
    });
}
