import CacheableAsset from 'custom_elements/CacheableAsset';
import ClearableInput from 'custom_elements/ClearableInput';
import LazyDetails from 'custom_elements/LazyDetails';

const customElements = {
    'cacheable-asset': CacheableAsset,
    'clearable-input': ClearableInput,
    'lazy-details': LazyDetails,
};

Object.entries(customElements).forEach(([name, classDef]) => {
    if (!window.customElements.get(name)) {
        window.customElements.define(name, classDef);
    }
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
}
