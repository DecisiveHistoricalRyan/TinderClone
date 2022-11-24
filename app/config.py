from pydantic import BaseSettings


class Settings(BaseSettings):
    STAGE = "local"
    POSTGRES_PROTOCOL = ""
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""
    POSTGRES_SERVER = ""
    POSTGRES_PORT = ""
    POSTGRES_DB = ""

    class Config:
        env_file = ".env"


settings = Settings()
