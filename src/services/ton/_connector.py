from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage

from src.common import config


class Connector(TonConnect):
    def __init__(self, user_id: int):
        super().__init__(
            manifest_url=config.MANIFEST_URL,
            storage=FileStorage(f'connections/{user_id}.json'),
            wallets_list_source=config.WALLETS_LIST_URL
        )
