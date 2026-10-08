from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    admin_user_id: int
    database_url: str
    userbot_api_id: int
    userbot_api_hash: str
    userbot_session: str = ""
    token_encryption_key: str
    log_level: str = "INFO"
    worker_count: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
