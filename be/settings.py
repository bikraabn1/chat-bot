from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    ai_url: str
    secret_key: SecretStr
    
    class Config:
        env_file= ".env"
        env_file_encoding="utf-8"