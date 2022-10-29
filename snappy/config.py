from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        case_sensitive = False
        env_file = ".env"


settings = Settings()
