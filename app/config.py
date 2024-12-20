from pydantic import AnyUrl, Secret
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    database_url: AnyUrl = "sqlite:///./crowdfunding.sqlite3"
    secret_key: Secret[str] = "secret123"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
