from miyoushe.lib.ds import DS
from miyoushe.lib.request import MiHoYoRequest, HeaderSign
from miyoushe.untility import log


class UpVote(MiHoYoRequest):
    def __init__(self):
        super().__init__()

    @HeaderSign(DS.api_others)
    def post(self, uri, data=None, json=None, headers: dict = None, **kwargs):
        return super().post(uri, data, json, headers, **kwargs)

    @log.logger.catch
    def _run(self, post_id: int) -> dict:
        """
        :uri: /apihub/sapi/upvotePost
        :json: {'post_id': post_id, 'is_cancel': False}
        :headers: {'Referer': 'https://app.mihoyo.com', 'Content-Type': 'application/json'}
        :response: {"retcode":0,"message":"OK","data":{}}
        :
        :param post_id: post id
        :return: response json
        """
        response = self.post(
            uri='/apihub/sapi/upvotePost',
            json={'post_id': post_id, 'is_cancel': False},
            headers={
                'Referer': 'https://app.mihoyo.com',
                'Content-Type': 'application/json',
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'UpVote failed: {response.status_code} {response.text}')

    def vote(self, post_id: int) -> bool:
        """
        :param post_id: post id
        :return: True if success
        """
        response = self._run(post_id)
        return response.get('retcode') == 0 and response.get('message') == 'OK'


if __name__ == '__main__':
    upvote = UpVote()
    print(upvote.vote(36399831))
