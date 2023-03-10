import random
import json
import time
import hashlib
from enum import Enum
from miyoushe.untility import rand, log


class SALT(Enum):
    PROD = 'JwYDpKvLj6MrMqqYU6jTKF17KNO2PXoS'
    API_SIGN_IN = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'
    OTHER = 'KZazpG4cO2QECFDBUCxdhS8cYCsQHfzn'

def _createSign(salt: SALT, t: str, r: str, query: str = '', body: str = ''):
    sign = hashlib.md5(("salt=" + salt.value + "&t=" + t + "&r=" + r + "&b=" + body + "&q=" + query).encode()).hexdigest()
    return t + "," + r + "," + sign


class DS:
    @staticmethod
    def sign_in(query: str = '', body: str = '') -> str:
        """
        uri matches:
           [POST] /apihub/app/api/signIn

        :param query: query string
        :param body: body string or json dict
        :return: DS header value
        """
        r = rand.randFromSystem()
        r = (r / 2147483650.0 * 100000.0 + 100000.0) % 1000000
        if r > 0x100001:
            r += 0x8469F
        r = int(r)
        r &= 0xFFFFFFFF
        return _createSign(salt=SALT.API_SIGN_IN, t=str(int(time.time())), r=str(r), query=query, body=body)

    @staticmethod
    def api_others(query: str = '', body: str = '') -> str:
        """
        uri matches:
           [GET] /apihub/sapi/querySignInStatus

        :param query: is not used
        :param body: is not used
        :return: DS header value
        """
        r = rand.randString(length=6)
        t = str(int(time.time()))
        sign = hashlib.md5(("salt=" + SALT.OTHER.value + "&t=" + t + "&r=" + r).encode()).hexdigest()
        return t + "," + r + "," + sign


if __name__ == '__main__':
    print(DS.sign_in(body='{"gids":"8"}'))
    print(DS.api_others(query='gids=8'))

