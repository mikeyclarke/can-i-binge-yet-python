import timeout from 'helpers/timeout';
import LazyDetails from 'custom_elements/LazyDetails';
import HttpClient from 'http/HttpClient';

const TAG_NAME: string = 'lazy-details';
const INITIAL_ATTRS: string = 'aria-live="polite" aria-busy="false"';

const mockGet = jest.fn();
jest.mock('http/HttpClient', () => {
    return {
        default: jest.fn().mockImplementation(() => {
            return {
                get: mockGet,
            }
        })
    }
});

beforeAll(() => {
    customElements.define(TAG_NAME, LazyDetails);
});

beforeEach(() => {
    (<jest.Mock> HttpClient).mockClear();
    mockGet.mockClear();
});

test('Can create with document.createElement', () => {
    const element = document.createElement(TAG_NAME);
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Can create from constructor', () => {
    const element = new LazyDetails();
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Silently fails when parent element is not <details>', () => {
    const container = document.createElement('div');
    container.innerHTML = `<div><${TAG_NAME} ${INITIAL_ATTRS}><p>Not inside a details element</p></${TAG_NAME}></div>`;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = ''
});

test('Loads when connected if <details> is already open', async () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <details open>
            <summary>Some label</summary>
            <${TAG_NAME} src="/foo/bar" ${INITIAL_ATTRS}>
                <p>Some placeholder content</p>
            </${TAG_NAME}>
        </details>
    `;
    const lazyDetails = <LazyDetails> container.querySelector(TAG_NAME);

    createHttpGetExpectation({"html": "<h1>Hello</h1><p>I am the lazy loaded content.</p>"});

    document.body.append(container);
    expect(lazyDetails.getAttribute('aria-busy')).toBe('true');

    await waitForElementToChange(lazyDetails);

    expect(mockGet).toBeCalledTimes(1);
    expect(mockGet.mock.calls[0][0]).toBe('/foo/bar');
    expect(mockGet.mock.calls[0][1]).toBe(null);
    expect(mockGet.mock.calls[0][2]).toBeInstanceOf(AbortSignal);
    expect(lazyDetails.getAttribute('aria-busy')).toBe('false');
    expect(lazyDetails.children.length).toBe(2);
    expect(lazyDetails.children[0].nodeName).toBe('H1');
    expect(lazyDetails.children[0].textContent).toBe('Hello');
    expect(lazyDetails.children[1].nodeName).toBe('P');
    expect(lazyDetails.children[1].textContent).toBe('I am the lazy loaded content.');

    document.body.innerHTML = ''
});

test('Does not Load when connected if <details> is not already open', async () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <details>
            <summary>Some label</summary>
            <${TAG_NAME} src="/foo/bar" ${INITIAL_ATTRS}>
                <p>Some placeholder content</p>
            </${TAG_NAME}>
        </details>
    `;
    const lazyDetails = <LazyDetails> container.querySelector(TAG_NAME);

    createHttpGetExpectation({"html": "<h1>Hello</h1><p>I am the lazy loaded content.</p>"});

    document.body.append(container);

    expect(mockGet).toBeCalledTimes(0);
    expect(lazyDetails.children.length).toBe(1);
    expect(lazyDetails.children[0].nodeName).toBe('P');
    expect(lazyDetails.children[0].textContent).toBe('Some placeholder content');

    document.body.innerHTML = ''
});

test('Loads when <details> toggle event fires if <details> is not already open', async () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <details>
            <summary>Some label</summary>
            <${TAG_NAME} src="/foo/bar" ${INITIAL_ATTRS}>
                <p>Some placeholder content</p>
            </${TAG_NAME}>
        </details>
    `;
    const details = <HTMLDetailsElement> container.querySelector('details');
    const lazyDetails = <LazyDetails> container.querySelector(TAG_NAME);

    createHttpGetExpectation({"html": "<h1>Hello</h1><p>I am the lazy loaded content.</p>"});

    document.body.append(container);

    details.open = true;
    triggerToggleEvent(details);
    expect(lazyDetails.getAttribute('aria-busy')).toBe('true');

    await waitForElementToChange(lazyDetails);

    expect(mockGet).toBeCalledTimes(1);
    expect(mockGet.mock.calls[0][0]).toBe('/foo/bar');
    expect(mockGet.mock.calls[0][1]).toBe(null);
    expect(mockGet.mock.calls[0][2]).toBeInstanceOf(AbortSignal);
    expect(lazyDetails.getAttribute('aria-busy')).toBe('false');
    expect(lazyDetails.children.length).toBe(2);
    expect(lazyDetails.children[0].nodeName).toBe('H1');
    expect(lazyDetails.children[0].textContent).toBe('Hello');
    expect(lazyDetails.children[1].nodeName).toBe('P');
    expect(lazyDetails.children[1].textContent).toBe('I am the lazy loaded content.');

    document.body.innerHTML = ''
});

test('Whilst request is in progress further <details> toggle events do not trigger duplicate requests', async () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <details>
            <summary>Some label</summary>
            <${TAG_NAME} src="/foo/bar" ${INITIAL_ATTRS}>
                <p>Some placeholder content</p>
            </${TAG_NAME}>
        </details>
    `;
    const details = <HTMLDetailsElement> container.querySelector('details');
    const lazyDetails = <LazyDetails> container.querySelector(TAG_NAME);

    createHttpGetExpectation({"html": "<h1>Hello</h1><p>I am the lazy loaded content.</p>"});

    document.body.append(container);

    details.open = true;
    triggerToggleEvent(details);

    details.open = false;
    triggerToggleEvent(details);

    details.open = true;
    triggerToggleEvent(details);

    expect(mockGet).toBeCalledTimes(1);

    document.body.innerHTML = ''
});

test('Once loaded it does not load again when further <details> toggle events fire', async () => {
    const container = document.createElement('div');
    container.innerHTML = `
        <details>
            <summary>Some label</summary>
            <${TAG_NAME} src="/foo/bar" ${INITIAL_ATTRS}>
                <p>Some placeholder content</p>
            </${TAG_NAME}>
        </details>
    `;
    const details = <HTMLDetailsElement> container.querySelector('details');
    const lazyDetails = <LazyDetails> container.querySelector(TAG_NAME);

    createHttpGetExpectation({"html": "<h1>Hello</h1><p>I am the lazy loaded content.</p>"});

    document.body.append(container);

    details.open = true;
    triggerToggleEvent(details);

    await waitForElementToChange(lazyDetails);

    details.open = false;
    triggerToggleEvent(details);

    details.open = true;
    triggerToggleEvent(details);

    expect(mockGet).toBeCalledTimes(1);

    document.body.innerHTML = ''
});

function createHttpGetExpectation(result: Record<string, string>): void {
    mockGet.mockImplementation(async () => {
        return Promise.resolve(new Response(JSON.stringify(result), {headers: {'Content-Type': 'application/json'}}));
    });
}

function waitForElementToChange(element: LazyDetails): Promise<void> {
    return new Promise(resolve => {
        const observer = new MutationObserver(mutations => {
            for (const mutation of mutations) {
                if (mutation.addedNodes.length > 0) {
                    observer.disconnect();
                    resolve();
                }
            }
        });
        observer.observe(element, {childList: true});
    });
}

function triggerToggleEvent(element: HTMLElement): void {
    element.dispatchEvent(
        new Event('toggle', {
            bubbles: false,
            cancelable: false,
        })
    );
}
