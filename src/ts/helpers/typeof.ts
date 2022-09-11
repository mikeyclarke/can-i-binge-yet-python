export function isObject(thing: any): boolean {
    return Object.prototype.toString.call(thing) === '[object Object]';
}
