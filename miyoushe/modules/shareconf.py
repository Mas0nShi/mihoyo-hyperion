from miyoushe.lib.request import MiHoYoRequest, HeaderSign
from miyoushe.untility import log
from miyoushe.untility.config import Gid
from miyoushe.lib.ds import DS


class ShareResult:
    def __init__(self, retcode: int, message: str, data: dict):
        self.retcode = retcode
        self.message = message
        self.data = data

    def __str__(self):
        return f'ShareResult(retcode={self.retcode}, message={self.message}, data={self.data})'

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.is_success

    @property
    def is_success(self):
        return self.retcode == 0 and self.message == 'OK'

    @property
    def title(self):
        return self.data['title']

    @property
    def content(self):
        return self.data['content']

    @property
    def icon(self):
        return self.data['icon']

    @property
    def url(self):
        return self.data['url']


class ShareConf(MiHoYoRequest):
    """
    :uri: /apihub/api/getShareConf
    :params: entity_type=1&entity_id=123456
    :response: {"retcode":0,"message":"OK","data":{"title":"","content":"","icon":"","url":""}}

    """
    def __init__(self):
        super().__init__()

    @HeaderSign(DS.api_others)
    def get(self, uri, params=None, headers: dict = None, **kwargs):
        return super().get(uri, params, headers, **kwargs)

    @log.logger.catch
    def _run(self, post_id: int) -> dict:
        response = self.get(uri='/apihub/api/getShareConf', params={
            'entity_type': 1,
            'entity_id': post_id,
        }, headers={
            'Referer': 'https://app.mihoyo.com',
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Invalid status code: {response.status_code}, {response.text}')

    def share(self, post_id: int) -> ShareResult:
        return ShareResult(**self._run(post_id))


if __name__ == '__main__':
    sr = ShareConf().share(36692251)
    print(sr)
    print(sr.is_success)
    print(sr.title)
