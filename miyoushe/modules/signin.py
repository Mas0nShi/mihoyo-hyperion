from miyoushe.lib.request import MiHoYoRequest, HeaderSign
from miyoushe.untility import log
from miyoushe.lib.ds import DS
import json as JSON

from miyoushe.untility.config import Gid

class SigninResult:
    retcode: int
    message: str
    data: dict

    def __init__(self, retcode: int, message: str, data: dict):
        self.retcode = retcode
        self.message = message
        self.data = data

    def __str__(self):
        return f'SigninResult: | {self.retcode} | {self.message} | {self.data} |'

    def __repr__(self):
        return f'{self.retcode}, {self.message}, {self.data}'

    def __bool__(self):
        return self.is_success

    def __int__(self):
        return self.points

    @property
    def points(self):
        return self.data.get('points', -1)

    @property
    def raw(self):
        return self.data

    @property
    def is_success(self):
        return self.retcode == 0 and self.message == 'OK'


class Signin(MiHoYoRequest):
    """
    :uri: /apihub/app/api/signIn
    :param: e.g. {'gids': 1}

    response example:
    error: {'data': None, 'message': '签到失败或重复签到', 'retcode': 1008}
    captcha: {'data': None, 'message': '', 'retcode': 1034}
    success: {'retcode': 0, 'message': 'OK', 'data': {'points': 30}}

    @TODO: captcha:
      Geetest verification
      URL: https://bbs-api.miyoushe.com/misc/api/createVerification?is_high=true
      URL: https://apiv6.geetest.com/get.php
      URL: https://bbs-api.miyoushe.com/misc/api/verifyVerification
      Add Header: x-rpc-challenge: 93fe4bd3dee8b87b63a443a646660640
    """
    def __init__(self):
        super().__init__()

    @HeaderSign(DS.sign_in)
    def post(self, uri, data=None, json=None, headers: dict = None, **kwargs):
        return super().post(uri, data, json, headers, **kwargs)

    @log.logger.catch
    def _run(self, gid: Gid) -> dict:
        response = self.post(uri='/apihub/app/api/signIn', data=JSON.dumps({'gids': gid.value}), headers={
            'Referer': 'https://app.mihoyo.com',
            'Content-Type': 'application/json',
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Invalid status code: {response.status_code}, {response.text}')

    def signin(self, gid: Gid) -> SigninResult:
        result = self._run(gid=gid)
        return SigninResult(**result)


if __name__ == '__main__':
    print(Signin().signin(Gid.bhxy2))
