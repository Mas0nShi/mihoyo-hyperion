from enum import Enum
from miyoushe.untility import log
from os.path import dirname, abspath, join as path_join, exists as path_exists
import pathlib
try:
    import tomllib
except ImportError:
    import toml as tomllib


PATH = pathlib.Path(dirname(abspath(__file__))).parent
TOML_PATH = path_join(PATH, 'config', 'config.toml')  # TODO: change to config.toml


class Gid(Enum):
    bh3: int = 1     # 崩坏3
    ys: int = 2      # 原神
    bhxy2: int = 3   # 崩坏学园2
    wdsjb: int = 4   # 未定事件簿
    dbs: int = 5     # 大别墅
    bhxqtd: int = 6  # 崩坏: 星穹铁道
    jq0: int = 8     # 绝区零

class GidName(Enum):
    bh3: str = '崩坏3'
    ys: str = '原神'
    bhxy2: str = '崩坏学园2'
    wdsjb: str = '未定事件簿'
    dbs: str = '大别墅'
    bhxqtd: str = '崩坏: 星穹铁道'
    jq0: str = '绝区零'


class Config:
    @log.called(f'toml config loaded: {TOML_PATH}')
    def __init__(self):
        assert path_exists(TOML_PATH), f'Config file not found: {TOML_PATH}'
        self.toml = tomllib.load(TOML_PATH)

    @property
    def headers(self) -> dict:
        headers = self.toml['headers']
        buf = {f'x-rpc-{k}': v for k, v in headers['x-rpc'].items()}
        buf.update({k: v for k, v in headers.items() if k != 'x-rpc'})
        return buf

    @property
    def cookies(self) -> dict:
        return self.toml['account']['cookies']

    @property
    def host(self) -> str:
        return self.toml['general']['host']

    @property
    def gids(self) -> dict:
        return self.toml['general']['gids']

