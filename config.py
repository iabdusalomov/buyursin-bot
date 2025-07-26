import os
# from dotenv import load_dotenv

# load_dotenv()

# Простой способ загрузки .env без python-dotenv
try:
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"').strip("'")
except FileNotFoundError:
    pass


class Config:
    # DB_USER = os.getenv("DB_USER")
    # DB_PASSWORD = os.getenv("DB_PASSWORD")
    # DB_NAME = os.getenv("DB_NAME")
    # DB_HOST = os.getenv("DB_HOST")
    # DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/postgres"
    # DB_CONFIG = f"postgresql+asyncpg://postgres:0@localhost/postgres"
    # DB_CONFIG = f"sqlite:///db.sqlite"
    DB_CONFIG = "sqlite+aiosqlite:///./db.sqlite"

BOT_TOKEN = os.getenv("TOKEN")
# ADMIN_IDS = [123456789, 987654321]
ADMIN_GROUP_ID = -1002804005202
CHANNEL_ID = -1002488415275
# CHANNEL_ID = -1002570244666