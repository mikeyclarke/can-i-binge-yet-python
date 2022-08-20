import timeout from 'helpers/timeout';

export default class ClearableInput extends HTMLElement {
    #abortController: AbortController | null = null;
    #input: HTMLInputElement | null = null;
    #clearButton: HTMLButtonElement | null = null;

    connectedCallback(): void {
        if (!this.isConnected) {
            return;
        }

        const input = this.querySelector('input');
        const clearButton = this.querySelector('button');

        if (!(input instanceof HTMLInputElement) || !(clearButton instanceof HTMLButtonElement)) {
            return;
        }

        this.#input = input;
        this.#clearButton = clearButton;

        this.#abortController = new AbortController();
        const signal = this.#abortController.signal;

        const eventOptions = {
            signal: signal,
            passive: true,
        };
        this.addEventListener('focusin', this.#onFocusIn.bind(this), eventOptions);
        this.addEventListener('focusout', this.#onFocusOut.bind(this), eventOptions);
        this.#input.addEventListener('input', this.#onInputElementInput.bind(this), eventOptions);
        this.#clearButton.addEventListener('click', this.#onClearButtonClick.bind(this), eventOptions);
    }

    disconnectedCallback(): void {
        if (null !== this.#abortController) {
            this.#abortController.abort();
            this.#abortController = null;
        }
    }

    #onFocusIn(): void {
        if (null === this.#input || null === this.#clearButton) {
            return;
        }

        if (this.#input.value.length > 0) {
            this.#clearButton.hidden = false;
        }
    }

    async #onFocusOut(): Promise<void> {
        if (null === this.#clearButton) {
            return;
        }

        await timeout(150);

        if (null !== document.activeElement && this.contains(document.activeElement)) {
            return;
        }

        this.#clearButton.hidden = true;
    }

    #onInputElementInput(): void {
        if (null === this.#input || null === this.#clearButton) {
            return;
        }

        this.#clearButton.hidden = (this.#input.value.length === 0);
    }

    #onClearButtonClick(): void {
        if (null === this.#input || null === this.#clearButton) {
            return;
        }

        this.#input.value = '';
        this.#input.focus();
        this.#clearButton.hidden = true;
    }
}
