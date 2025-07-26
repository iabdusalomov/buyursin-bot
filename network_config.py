import aiohttp
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class NetworkConfig:
    """Настройки для улучшения сетевого подключения"""
    
    # Настройки HTTP клиента
    HTTP_TIMEOUT = aiohttp.ClientTimeout(
        total=60,  # Общий таймаут
        connect=30,  # Таймаут подключения
        sock_read=30,  # Таймаут чтения
        sock_connect=30  # Таймаут установки соединения
    )
    
    # Настройки для повторных попыток
    MAX_RETRIES = 5
    RETRY_DELAY = 2.0  # секунды
    BACKOFF_FACTOR = 1.5  # множитель для экспоненциальной задержки
    
    @staticmethod
    async def create_session() -> aiohttp.ClientSession:
        """Создает HTTP сессию с оптимизированными настройками"""
        connector = aiohttp.TCPConnector(
            limit=100,  # Максимальное количество соединений
            limit_per_host=30,  # Максимум соединений на хост
            ttl_dns_cache=300,  # Кэш DNS на 5 минут
            use_dns_cache=True,
            keepalive_timeout=30,  # Keep-alive таймаут
            enable_cleanup_closed=True,  # Автоочистка закрытых соединений
        )
        
        return aiohttp.ClientSession(
            connector=connector,
            timeout=NetworkConfig.HTTP_TIMEOUT,
            headers={
                'User-Agent': 'TelegramBot/1.0 (aiogram)',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
            }
        )
    
    @staticmethod
    async def retry_with_backoff(func, *args, **kwargs):
        """Выполняет функцию с повторными попытками и экспоненциальной задержкой"""
        last_exception = None
        
        for attempt in range(NetworkConfig.MAX_RETRIES):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < NetworkConfig.MAX_RETRIES - 1:
                    delay = NetworkConfig.RETRY_DELAY * (NetworkConfig.BACKOFF_FACTOR ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {NetworkConfig.MAX_RETRIES} attempts failed. Last error: {e}")
        
        raise last_exception

def setup_network_logging():
    """Настройка логирования для сетевых операций"""
    # Увеличиваем уровень логирования для aiohttp
    logging.getLogger('aiohttp.client').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.connector').setLevel(logging.WARNING)
    
    # Настройка для aiogram
    logging.getLogger('aiogram').setLevel(logging.INFO)
    logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)

def get_polling_settings():
    """Возвращает настройки для polling режима"""
    return {
        "timeout": 30,
        "limit": 100,
        "allowed_updates": ["message", "callback_query", "inline_query"],
        "drop_pending_updates": True,
        "close_loop": False,  # Не закрываем loop при ошибках
    } 