from miyoushe.untility import log
from miyoushe.lib.request import MiHoYoRequest, HeaderSign
from miyoushe.untility.config import Gid
from miyoushe.lib.ds import DS

class PostsResult:
    retcode: int
    message: str
    data: dict
    """
    {'data': None, 'message': 'Something went wrong...please retry later', 'retcode': -502}
    
    """
    def __init__(self, retcode: int, message: str, data: dict):
        self.retcode = retcode
        self.message = message
        self.data = data

    def __str__(self):
        return f'PostsResult: | {self.retcode} | {self.message} | {self.data} |'

    def __repr__(self):
        return f'{self.retcode}, {self.message}, {self.data}'

    def __bool__(self):
        return self.is_success

    @property
    def raw(self) -> dict | None:
        return self.data

    @property
    def list(self) -> list:
        return self.data.get('list', [])

    @property
    def length(self) -> int:
        return len(self.list)

    @property
    def is_success(self) -> bool:
        return self.retcode == 0 and self.message == 'OK'

    @property
    def posts_id(self) -> list:
        return [item['post']['post_id'] for item in self.list]

    @property
    def posts_subject(self) -> list:
        return [item['post']['subject'] for item in self.list]

class Posts(MiHoYoRequest):
    def __init__(self):
        super().__init__()

    @HeaderSign(DS.api_others)
    def get(self, uri, params=None, headers: dict = None, **kwargs):
        return super().get(uri, params, headers, **kwargs)

    @log.logger.catch
    def _run(self, gid: Gid) -> dict:
        """
        :uri: /post/api/feeds/posts
        :param: gids=1&last_id=&fresh_action=1&is_first_initialize=false&filter=
        :return: response json
        """
        response = self.get(
            uri='/post/api/feeds/posts',
            params={
                'gids': gid.value,
                'last_id': '',
                'fresh_action': 1,
                'is_first_initialize': 'false',
                'filter': '',
            },
            headers={
                'Referer': 'https://app.mihoyo.com',
                'Content-Type': 'application/www-form-urlencoded',
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Posts failed: {response.status_code} {response.text}')

    def get_posts(self, gid: Gid) -> PostsResult:
        """
        :param gid: Gid enum
        :return: list of posts
        """
        response = self._run(gid)
        result = PostsResult(**response)
        return result


if __name__ == '__main__':
    posts = Posts()
    r = posts.get_posts(Gid.bh3)
    print(r.raw)
