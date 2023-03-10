from miyoushe.lib.request import MiHoYoRequest, HeaderSign
from miyoushe.untility import log
from miyoushe.untility.config import Gid
from miyoushe.lib.ds import DS

class QuerySignIn(MiHoYoRequest):
    """
    :uri: /apihub/sapi/querySignInStatus
    """
    def __init__(self):
        super().__init__()

    @HeaderSign(DS.api_others)
    def get(self, uri, params=None, headers: dict = None, **kwargs):
        return super().get(uri, params, headers, **kwargs)

    @log.logger.catch
    def _run(self, gid: Gid) -> dict:
        """
        :param gid: Gid enum
        :return: response json
        """
        response = self.get(uri='/apihub/sapi/querySignInStatus', params={'gids': gid.value}, headers={
            'Referer': 'https://app.mihoyo.com',
            'Content-Type': 'application/json',
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Invalid status code: {response.status_code}, {response.text}')

    def get_signin_status(self, gid: Gid) -> bool:
        return self._run(gid=gid)['data']['is_signed']


if __name__ == '__main__':
    print(QuerySignIn().get_signin_status(Gid.dbs))