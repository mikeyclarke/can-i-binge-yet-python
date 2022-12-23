import CachedAssetsCatalog from 'asset/CachedAssetsCatalog';

type AssetType = 'css' | 'javascript';

const CACHE_VERSION = 1;
const CACHE_NAME = 'assets-v' + CACHE_VERSION;

export class AssetCacheError extends Error {}

export class StorageUnavailableError extends AssetCacheError {
    constructor() {
        const message = 'Asset catalog storage is not available. This is likely because the browser is in private ' +
            'browsing mode and does not support the storage driver in this mode.';
        super(message);
    }
}

export default class AssetCache {
    #cachedAssetsCatalog: CachedAssetsCatalog;

    constructor() {
        this.#cachedAssetsCatalog = new CachedAssetsCatalog();
    }

    async cacheBundle(bundleName: string, url: string, content: string, assetType: AssetType): Promise<void> {
        if (await this.#cachedAssetsCatalog.isAvailable() === false) {
            throw new StorageUnavailableError();
        }

        const bundlePreviousUrl = await this.#cachedAssetsCatalog.get(bundleName);
        if (bundlePreviousUrl === url) {
            return;
        }

        const cache = await this.getCache();

        if (null !== bundlePreviousUrl) {
            await cache.delete(bundlePreviousUrl);
        }

        const response = this.#createResponse(content, assetType);
        await cache.put(url, response);

        await this.#cachedAssetsCatalog.set(bundleName, url);
    }

    async getCache(): Promise<Cache> {
        return await caches.open(CACHE_NAME);
    }

    #createResponse(content: string, assetType: AssetType): Response {
        return new Response(content, {
            status: 200,
            statusText: 'OK',
            headers: {
                'Content-Type': `text/${assetType}; charset="utf-8"`,
            },
        });
    }
}
