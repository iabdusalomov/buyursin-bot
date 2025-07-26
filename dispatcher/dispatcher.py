from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
PROXY_URL = "http://proxy.server:3128"

bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL)
try:
    from aiogram.fsm.storage.redis import RedisStorage
    storage = RedisStorage.from_url("redis://localhost:6379/0")
    print("[INFO] FSM: RedisStorage enabled")
except ImportError:
    from aiogram.fsm.storage.memory import MemoryStorage
    storage = MemoryStorage()
    print("[INFO] FSM: MemoryStorage enabled (no redis)")
dis = Dispatcher(storage=storage)