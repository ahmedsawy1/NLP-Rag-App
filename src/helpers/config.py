from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPEN_API_KEY: str

    FILE_MAX_SIZE: int
    FILE_ALLOWED_EXTENSIONS: list
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGO_DATABASE: str

    class Config:
        env_file: str = ".env"


def get_settings():
    return Settings()
