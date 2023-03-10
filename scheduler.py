import random
import time
from typing import List
from miyoushe.modules import *
from miyoushe.untility.config import Gid, GidName
from miyoushe.untility.log import mlog
from miyoushe.modules.posts import PostsResult


def delay(seconds: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            mlog.debug(f'Sleep {seconds} seconds.')
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Scheduler:
    @staticmethod
    @delay(random.randint(3, 6))
    def _sign_in(gid: Gid):
        gid_name = GidName[gid.name].value
        if query_signin.get_signin_status(gid=gid):
            mlog.info(f'Gid [{gid_name}] has signed in.')
            return

        mlog.info(f'Start sign in Gid [{gid_name}].')
        r = signin.signin(gid=gid)
        if r.is_success:
            mlog.info(f'Sign in Gid [{gid_name}] success.')
        else:
            mlog.error(f'Sign in Gid [{gid_name}] failed.')

    @staticmethod
    @delay(random.randint(2, 5))
    def _get_rand_posts() -> PostsResult | None:
        gid = random.sample(list(Gid), 1)[0]
        prs = posts.get_posts(gid=gid)
        if not prs.is_success:
            mlog.error(f'Get posts failed: {prs.retcode} {prs.message}')
            return None
        return prs

    @staticmethod
    @delay(random.randint(2, 5))
    def _upvote(post_id: int, post_subject: str):
        mlog.info(f'Start upvote post {post_id} {post_subject}')
        is_success = upvote.vote(post_id=post_id)
        if is_success:
            mlog.info(f'Upvote post: <{post_subject}> success.')
        else:
            mlog.error(f'Upvote post: <{post_subject}> failed.')

    @staticmethod
    def _share(post_id: int):
        r = share.share(post_id=post_id)
        if r.is_success:
            mlog.info(f'Share post: <{r.title}> success.')
        else:
            mlog.error(f'Share post: <{r.title}> failed.')


    @classmethod
    def run(cls):
        gids = list(Gid)
        random.shuffle(gids)
        for gid in gids:
            cls._sign_in(gid=gid)
        # =================================================
        prs = cls._get_rand_posts()
        if prs is None:
            return

        # upvote
        posts_id = prs.posts_id
        posts_subject = prs.posts_subject
        for post_id, post_subject in zip(posts_id, posts_subject):
            cls._upvote(post_id=post_id, post_subject=post_subject)

        # share
        cls._share(post_id=random.choice(posts_id))


if __name__ == '__main__':
    Scheduler.run()
