import timeout from 'helpers/timeout';
import ClearableInput from 'custom_elements/ClearableInput';

const TAG_NAME: string = 'clearable-input';

beforeAll(() => {
    customElements.define(TAG_NAME, ClearableInput);
});

test('Can create with document.createElement', () => {
    const element = document.createElement(TAG_NAME);
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Can create from constructor', () => {
    const element = new ClearableInput();
    expect(element.nodeName).toBe(TAG_NAME.toUpperCase());
});

test('Silently fails when contains invalid markup', () => {
    const container = document.createElement('div');
    container.innerHTML = `<${TAG_NAME}><p>No input or button in here!</p></${TAG_NAME}>`;
    expect(() => { document.body.append(container) }).not.toThrow();
    document.body.innerHTML = ''
});

describe('Event tests', () => {
    beforeEach(() => {
        const container = document.createElement('div');
        container.innerHTML = `
            <${TAG_NAME}>
                <input type="text">
                <button type="button" hidden>Clear</button>
            </${TAG_NAME}>
        `;
        document.body.append(container);
    });

    afterEach(() => {
        document.body.innerHTML = ''
    });

    test('On focus, button is shown if input not empty', () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        input.value = 'Foobar';

        triggerFocusEvent(element, 'focusin');

        expect(button.hidden).toBe(false);
    });

    test('On focus, button is not shown if input is empty', () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        triggerFocusEvent(element, 'focusin');

        expect(button.hidden).toBe(true);
    });

    test('On blur, button is hidden', async () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        button.hidden = false;

        triggerFocusEvent(element, 'focusout');

        await timeout(160);

        expect(button.hidden).toBe(true);
    });

    test('On blur, button is not hidden if focus restored within 150ms', async () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        button.hidden = false;

        triggerFocusEvent(element, 'focusout');

        await timeout(100);
        input.focus();
        await timeout(60);

        expect(button.hidden).toBe(false);
    });

    test('On input, button is hidden if input is empty', () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        button.hidden = false;
        input.value = '';

        triggerInputEvent(input);

        expect(button.hidden).toBe(true);
    });

    test('On input, button becomes visible if input is not empty', () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        button.hidden = true;
        input.value = 'F';

        triggerInputEvent(input);

        expect(button.hidden).toBe(false);
    });

    test('Clicking button clears input', () => {
        const element = <ClearableInput> document.querySelector(TAG_NAME);
        const input = <HTMLInputElement> element.querySelector('input');
        const button = <HTMLButtonElement> element.querySelector('button');

        button.hidden = false;
        input.value = 'Foobar';

        triggerMouseEvent(button, 'click');

        expect(document.activeElement).toBe(input);
        expect(input.value).toBe('');
        expect(button.hidden).toBe(true);
    });
});

function triggerFocusEvent(element: HTMLElement, eventName: string): void {
    element.dispatchEvent(
        new FocusEvent(eventName, {
            bubbles: true,
            cancelable: true
        })
    );
}

function triggerInputEvent(element: HTMLElement): void {
    element.dispatchEvent(
        new Event('input', {
            bubbles: true,
            cancelable: true
        })
    );
}

function triggerMouseEvent(element: HTMLElement, eventName: string): void {
    element.dispatchEvent(
        new MouseEvent(eventName, {
            bubbles: true,
            cancelable: true
        })
    );
}
