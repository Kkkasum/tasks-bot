from pydantic_settings import BaseSettings, SettingsConfigDict

from ._constants import BASE_DIR


class Config(BaseSettings):
    BOT_TOKEN: str

    MANIFEST_URL: str
    WALLETS_LIST_URL: str

    PG_HOST: str
    PG_PORT: str
    PG_NAME: str
    PG_USER: str
    PG_PASS: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding='utf-8', extra='ignore')


config = Config()
DB_URL = f'postgresql+asyncpg://{config.PG_USER}:{config.PG_PASS}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_NAME}'
