import * as localforage from 'localforage';

export default class CachedAssetsCatalog {
    #store: typeof localforage | null = null;
    #booted: boolean = false;

    async isAvailable(): Promise<boolean> {
        const store = await this.#getStore();
        return store !== null;
    }

    async set(bundleName: string, url: string): Promise<void> {
        const store = await this.#getStore();
        if (null === store) {
            throw new Error('Storage is currently unavailable');
        }

        await store.setItem(bundleName, url);
    }

    async get(bundleName: string): Promise<string | null> {
        const store = await this.#getStore();
        if (null === store) {
            throw new Error('Storage is currently unavailable');
        }

        return await store.getItem(bundleName);
    }

    async remove(bundleName: string): Promise<void> {
        const store = await this.#getStore();
        if (null === store) {
            throw new Error('Storage is currently unavailable');
        }

        await store.removeItem(bundleName);
    }

    async getAll(): Promise<Record<string, string>> {
        const store = await this.#getStore();
        if (null === store) {
            throw new Error('Storage is currently unavailable');
        }

        const result: Record<string, string> = {};
        await store.iterate((value: string, key: string, iterationNumber: number) => {
            result[key] = value;
        });

        return result;
    }

    async #getStore(): Promise<typeof localforage | null> {
        if (this.#booted) {
            return this.#store;
        }

        localforage.setDriver(localforage.INDEXEDDB);

        try {
            await localforage.ready();
        } catch (error) {
            this.#booted = true;
            return null;
        }

        if (localforage.driver() !== localforage.INDEXEDDB) {
            this.#booted = true;
            return null;
        }

        this.#store = localforage.createInstance({name: 'assetDigest'});
        this.#booted = true;

        return this.#store;
    }
}
