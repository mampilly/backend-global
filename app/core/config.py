'''application configuration'''
from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    """Global configurations

     This variable will be loaded from the .env file. However, if there is a
    shell environment variable having the same name, that will take precedence.

     the class Field is necessary while defining the global variables"""
    ENV_STATE: Optional[str] = Field(..., env="ENV_STATE")
    HOST: Optional[str] = Field(..., env="HOST")

    ''' environment specific configs'''
    API_USERNAME: Optional[str] = None
    API_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_POOL_SIZE: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_SECONDS: Optional[int] = None
    API_KEY_NAME: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    OFFLINE_HOST: Optional[str] = None

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        '''Dev configuration'''
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        '''Production Configuration'''
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]) -> None:
        self.env_state = env_state

    def __call__(self) -> Union[DevConfig, ProdConfig]:
        if self.env_state == "dev":
            return DevConfig()

        return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()
