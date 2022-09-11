import ClearableInput from 'custom_elements/ClearableInput';
import LazyDetails from 'custom_elements/LazyDetails';

const customElements = {
    'clearable-input': ClearableInput,
    'lazy-details': LazyDetails,
};

Object.entries(customElements).forEach(([name, classDef]) => {
    if (!window.customElements.get(name)) {
        window.customElements.define(name, classDef);
    }
});
