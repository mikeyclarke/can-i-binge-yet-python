import HttpClient from 'http/HttpClient';

export default class LazyDetails extends HTMLElement {
    #httpClient: HttpClient;
    #abortController: AbortController | null = null;
    #details: HTMLDetailsElement | null = null;
    #loaded: boolean = false;
    #isRequestInProgress = false;

    constructor() {
        super();

        this.#httpClient = new HttpClient();
    }

    set src(src: string) {
        this.setAttribute('src', src);
    }

    get src(): string {
        return this.getAttribute('src') || '';
    }

    connectedCallback(): void {
        if (!this.isConnected) {
            return;
        }

        const parentElement = this.parentElement;
        if (!(parentElement instanceof HTMLDetailsElement)) {
            return;
        }

        this.#details = parentElement;

        if (this.#loaded) {
            return;
        }

        this.#abortController = new AbortController();
        const signal = this.#abortController.signal;

        if (this.#details.open) {
            this.#load();
            return;
        }

        const eventOptions = {
            signal: signal,
            passive: true,
        };
        this.#details.addEventListener('toggle', this.#onDetailsToggle.bind(this), eventOptions);
    }

    disconnectedCallback(): void {
        this.#removeEventListeners();
    }

    #onDetailsToggle(): void {
        if (null === this.#details) {
            return;
        }

        if (!this.#details.open) {
            return;
        }

        if (this.#isRequestInProgress) {
            return;
        }

        this.#load();
    }

    async #load(event: Event | null = null): Promise<void> {
        if (!this.hasAttribute('src')) {
            return;
        }

        this.#isRequestInProgress = true;
        this.setAttribute('aria-busy', 'true');

        const signal = (null !== this.#abortController) ? this.#abortController.signal : null;
        const response = await this.#httpClient.get(this.src, null, signal);
        const json = await response.json();
        if (!json.html) {
            throw new Error('Response body does not contain `html`');
        }

        this.#insertHtml(json.html);

        this.#removeEventListeners();
        this.#loaded = true;
        this.#isRequestInProgress = false;
        this.setAttribute('aria-busy', 'false');
    }

    #insertHtml(html: string): void {
        const fragment = document.createElement('template');
        fragment.innerHTML = html;

        this.innerHTML = '';
        this.appendChild(fragment.content);
    }

    #removeEventListeners(): void {
        if (null !== this.#abortController) {
            this.#abortController.abort();
            this.#abortController = null;
        }
    }
}
