import ClearableInput from 'custom_elements/ClearableInput';

const customElements = {
    'clearable-input': ClearableInput,
};

Object.entries(customElements).forEach(([name, classDef]) => {
    if (!window.customElements.get(name)) {
        window.customElements.define(name, classDef);
    }
});
