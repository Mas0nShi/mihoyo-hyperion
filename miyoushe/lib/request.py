import json as JSON

from requests import sessions, Session
from miyoushe.untility import config, log
from typing import Callable
from urllib.parse import urlencode, urljoin

def HeaderSign(func_sign: Callable):
    def decorator(func):
        def wrapper(*args, **kwargs):
            query = kwargs.get('params', '')
            if isinstance(query, dict):
                query = urlencode(query)
            body = kwargs.get('data', '') or kwargs.get('json', '')
            if isinstance(body, dict):
                body = JSON.dumps(body, separators=(',', ':'))
            kwargs['headers'] = kwargs.get('headers', {})
            kwargs['headers']['DS'] = func_sign(query=query, body=body)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class MiHoYoRequest(Session):
    headers: dict
    cookies: sessions.RequestsCookieJar
    header_ds: dict

    def __init__(self):
        super().__init__()
        self.headers = config.headers
        self.cookies = sessions.cookiejar_from_dict(config.cookies)

    @log.called('MiHoYoRequest', show_args=True, show_return=True)
    def get(self, uri, params=None, headers: dict = None, **kwargs):
        bufHeaders = self.headers.copy()
        bufHeaders.update(headers or {})
        url = urljoin(config.host, uri)
        return super().get(url, params=params, headers=bufHeaders, cookies=self.cookies, **kwargs)

    @log.called('MiHoYoRequest', show_args=True, show_return=True)
    def post(self, uri, data=None, json=None, headers: dict = None, **kwargs):
        bufHeaders = self.headers.copy()
        bufHeaders.update(headers or {})
        url = urljoin(config.host, uri)
        return super().post(url, data=data, json=json, headers=bufHeaders, cookies=self.cookies, **kwargs)


if __name__ == '__main__':
    from miyoushe.lib.ds import DS

    class Test(MiHoYoRequest):
        @HeaderSign(DS.sign_in)
        def get(self, url, params=None, headers: dict = None, **kwargs):
            print(headers)

        @HeaderSign(DS.sign_in)
        def post(self, url, data=None, json=None, headers: dict = None, **kwargs):
            print(headers)

    test = Test()
    test.get('/ys/article/123', params={'a': 1, 'b': 2})
    test.post('/ys/article/123', data='a=1&b=2')
    test.post('/ys/article/123', json={'a': 1, 'b': 2})