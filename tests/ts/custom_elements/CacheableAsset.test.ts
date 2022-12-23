import CacheableAsset from 'custom_elements/CacheableAsset';
import AssetCache from 'asset/AssetCache';

const TAG_NAME: string = 'cacheable-asset';

const mockCacheBundle = jest.fn();
jest.mock('asset/AssetCache', () => {
    return {
        default: jest.fn().mockImplementation(() => {
            return {
                cacheBundle: mockCacheBundle,
            }
        })
    }
});

beforeAll(() => {
    customElements.define(TAG_NAME, CacheableAsset);
});

beforeEach(() => {
    (<jest.Mock> AssetCache).mockClear();
    mockCacheBundle.mockClear();
});

test('Can create with document.createElement', () => {
    const element = document.createElement(TAG_NAME);
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Can create from constructor', () => {
    const element = new CacheableAsset();
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Silently fails when no child element and no element attribute', () => {
    const container = document.createElement('div');
    container.innerHTML = `<${TAG_NAME} src="/foo/bar" bundle="bar.js"></${TAG_NAME}>`;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when element attribute references element that does not exist', () => {
    const container = document.createElement('div');
    container.innerHTML = `<${TAG_NAME} src="/foo/bar" bundle="bar.js" element="id-for-nothing"></${TAG_NAME}>`;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when child element is invalid type', () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <${TAG_NAME} src="/foo/bar" bundle="bar.js">
            <p>Not a style or script element</p>
        </${TAG_NAME}>
    `;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when element attribute references element of invalid type', () => {
    document.body.append('<p id="asset-element">Not a style or script element</p>');
    const container = document.createElement('div');
    container.innerHTML = `<${TAG_NAME} src="/foo/bar" bundle="bar.js" element="asset-element"></${TAG_NAME}>`;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when script asset element has no text content', () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <${TAG_NAME} src="/foo/bar" bundle="bar.js">
            <script></script>
        </${TAG_NAME}>
    `;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when asset element has no src attribute', () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <${TAG_NAME} bundle="bar.js">
            <script>alert('Foo');</script>
        </${TAG_NAME}>
    `;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Silently fails when asset element has no bundle attribute', () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <${TAG_NAME} src="/foo/bar">
            <script>alert('Foo');</script>
        </${TAG_NAME}>
    `;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = '';
});

test('Caches script asset', () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <${TAG_NAME} src="/foo/bar" bundle="bar.js">
            <script>alert('Foo');</script>
        </${TAG_NAME}>
    `;

    createAssetCacheCacheBundleExpectation();

    document.body.append(container);

    expect(mockCacheBundle).toBeCalledTimes(1);
    expect(mockCacheBundle).toBeCalledWith('bar.js', '/foo/bar', "alert('Foo');", 'javascript');

    document.body.innerHTML = '';
});

test('Caches style asset', () => {
    const stylesheet = document.createElement('style');
    stylesheet.id = 'inline-stylesheet';
    stylesheet.textContent = '.foo { color: red; }';
    document.head.appendChild(stylesheet);

    const container = document.createElement('div');
    container.innerHTML = `<${TAG_NAME} src="/foo/bar" bundle="bar.css" element="inline-stylesheet"></${TAG_NAME}>`;

    createAssetCacheCacheBundleExpectation();

    document.body.append(container);

    expect(mockCacheBundle).toBeCalledTimes(1);
    expect(mockCacheBundle).toBeCalledWith('bar.css', '/foo/bar', '.foo { color: red; }', 'css');

    document.body.innerHTML = '';
});

function createAssetCacheCacheBundleExpectation(): void {
    mockCacheBundle.mockImplementation(async () => {
        return Promise.resolve();
    });
}
