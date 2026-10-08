# MTProto monitor scaffold. Configure API_ID/API_HASH/SESSION and implement
# Telethon event handlers for authorized public channels in production.
from telethon import TelegramClient
from ..config import settings

def create_client():
    return TelegramClient("thinking-userbot", settings.userbot_api_id, settings.userbot_api_hash)
