import AssetCache, {StorageUnavailableError} from 'asset/AssetCache';

const supportedTagNames = ['style', 'script'];

export default class CacheableAsset extends HTMLElement {
    async connectedCallback(): Promise<void> {
        if (!this.isConnected) {
            return;
        }

        const asset = this.#getAssetElement();
        if (null === asset || !supportedTagNames.includes(asset.tagName.toLowerCase())) {
            return;
        }

        if (null === asset.textContent) {
            return;
        }

        const assetType = asset.tagName.toLowerCase() === 'style' ? 'css' : 'javascript';
        if (assetType === 'javascript' && asset.textContent === '') {
            return;
        }

        if (!this.hasAttribute('src') || !this.hasAttribute('bundle')) {
            return;
        }

        const url = <string> this.getAttribute('src');
        const bundle = <string> this.getAttribute('bundle');

        const assetCache = new AssetCache();
        try {
            await assetCache.cacheBundle(bundle, url, asset.textContent, assetType);
        } catch (error) {
            if (!(error instanceof StorageUnavailableError)) {
                throw error;
            }
        }
    }

    #getAssetElement(): Element | null {
        const element = this.getAttribute('element');
        if (null !== element) {
            return document.getElementById(element);
        }

        return this.firstElementChild;
    }
}
