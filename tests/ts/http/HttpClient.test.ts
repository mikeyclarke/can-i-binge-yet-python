import HttpClient, { HttpClientError, HttpServerError, RequestMethod } from 'http/HttpClient';

const fetchMock = jest.spyOn(window, 'fetch');
let httpClient: HttpClient;

beforeEach(() => {
    fetchMock.mockClear();
    httpClient = new HttpClient();
});

test('request method sets default headers on Request interface', () => {
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(new Response());
    });

    httpClient.request(RequestMethod.GET, '/foo/bar');

    expect((<Request> fetchMock.mock.calls[0][0]).headers.get('Accept')).toBe('application/json');
    expect((<Request> fetchMock.mock.calls[0][0]).headers.get('X-Requested-With')).toBe('Fetch');
});

test('request method sets signal on Request interface', () => {
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(new Response());
    });

    const controller = new AbortController();
    const signal = controller.signal;
    httpClient.request(RequestMethod.GET, '/foo/bar', null, signal);

    expect((<Request> fetchMock.mock.calls[0][0]).signal).toBe(signal);
});

test('request method stringifies JSON and sets Content-Type header if body is an object', async () => {
    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(new Response());
    });

    const json = {
        'some_param': 'abc',
        'some_other_param': 123,
    }
    httpClient.request(RequestMethod.POST, '/foo/bar', json);

    expect((<Request> fetchMock.mock.calls[0][0]).headers.get('Content-Type')).toBe('application/json');
    expect(await (<Request> fetchMock.mock.calls[0][0]).text()).toBe(JSON.stringify(json));
});

test('request method does not stringify JSON or set Content-Type header if body is not an object', async () => {
    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(new Response());
    });

    const text = 'foobar';
    httpClient.request(RequestMethod.POST, '/foo/bar', text);

    expect((<Request> fetchMock.mock.calls[0][0]).headers.get('Content-Type')).toBe('text/plain;charset=UTF-8');
    expect(await (<Request> fetchMock.mock.calls[0][0]).text()).toBe(text);
});

test('request method returns response if response ok', async () => {
    const response = new Response(
        null,
        {
            status: 200,
        }
    );

    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(response);
    });

    const result = await httpClient.request(RequestMethod.GET, '/foo/bar');

    expect(result).toBe(response);
});

test('request method throws HttpClientError if response not okay and status is 4XX', async () => {
    const response = new Response(
        null,
        {
            status: 400,
        }
    );

    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(response);
    });

    async function request() {
        return await httpClient.request(RequestMethod.GET, '/foo/bar');
    }

    await expect(request()).rejects.toThrow(HttpClientError);
});

test('request method throws HttpServerError if response not okay and status is 5XX', async () => {
    const response = new Response(
        null,
        {
            status: 500,
        }
    );

    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(response);
    });

    async function request() {
        return await httpClient.request(RequestMethod.GET, '/foo/bar');
    }

    await expect(request()).rejects.toThrow(HttpServerError);
});

test('request method throws HttpServerError if response not okay and status is 5XX', async () => {
    const response = new Response(
        null,
        {
            status: 500,
        }
    );

    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(response);
    });

    async function request() {
        return await httpClient.request(RequestMethod.GET, '/foo/bar');
    }

    await expect(request()).rejects.toThrow(HttpServerError);
});

test('get method', async () => {
    const response = new Response(
        null,
        {
            status: 200,
        }
    );

    const fetchMock = jest.spyOn(window, 'fetch');
    fetchMock.mockImplementation(async () => {
        return Promise.resolve(response);
    });

    const parameters = {
        'foo': 'abc',
        'bar': 'def',
    }
    const controller = new AbortController();
    const signal = controller.signal;
    const result = await httpClient.get('/foo/bar', parameters, signal);

    const qs = (new URLSearchParams(parameters)).toString();

    expect((<Request> fetchMock.mock.calls[0][0]).url).toBe(`/foo/bar?${qs}`);
    expect((<Request> fetchMock.mock.calls[0][0]).signal).toBe(signal);
    expect(result).toBe(response);
});
