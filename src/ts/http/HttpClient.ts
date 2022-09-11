import { isObject } from 'helpers/typeof';

export class HttpError extends Error {
    public request: Request;
    public response: Response;

    constructor(request: Request, response: Response) {
        let message = `${response.status} ${response.statusText}`;
        if (message.trim().length === 0) {
            message = 'Unknown response error';
        }

        super(message);

        this.request = request;
        this.response = response;
    }
}

export class HttpClientError extends HttpError {}

export class HttpServerError extends HttpError {}

export enum RequestMethod {
    GET = 'GET',
    PUT = 'PUT',
    POST = 'POST',
    DELETE = 'DELETE',
    PATCH = 'PATCH',
    HEAD = 'HEAD',
}

type RequestBody = Blob | ArrayBuffer | DataView | FormData | URLSearchParams | ReadableStream | string | Record<string, any> | null;

type ResponsePromise = Promise<Response>;

interface RequestOptions {
    method: RequestMethod;
    headers: Headers;
    body?: Blob | ArrayBuffer | DataView | FormData | URLSearchParams | ReadableStream | string;
    signal?: AbortSignal;
}

export default class HttpClient {
    public async request(
        method: RequestMethod,
        url: string,
        body: RequestBody = null,
        signal: AbortSignal | null = null
    ): ResponsePromise {
        const headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'Fetch',
        };

        const options: RequestOptions = {
            method: method,
            headers: new Headers(headers),
        };

        if (isObject(body)) {
            options.body = JSON.stringify(body);
            options.headers.append('Content-Type', 'application/json');
        } else if (null !== body) {
            options.body = <Blob | ArrayBuffer | DataView | FormData | URLSearchParams | ReadableStream | string> body;
        }

        if (null !== signal) {
            options.signal = signal;
        }

        const request = new Request(url, options);
        const response = await fetch(request);

        if (response.ok) {
            return response;
        }

        if (response.status >= 400 && response.status <= 499) {
            throw new HttpClientError(request, response);
        }

        if (response.status >= 500 && response.status <= 599) {
            throw new HttpServerError(request, response);
        }

        throw new HttpError(request, response);
    }

    public async get(
        url: string,
        parameters: Record<string, any> | null = null,
        signal: AbortSignal | null = null
    ): ResponsePromise {
        const qs = (null !== parameters) ? (new URLSearchParams(parameters)).toString() : null;
        if (null !== qs) {
            url = `${url}?${qs}`;
        }

        return this.request(RequestMethod.GET, url, null, signal);
    }
}
