from dotenv import load_dotenv
import aiobot.handlers.commands as commands
import aiobot.handlers.user as user
import aiobot.handlers.ad as ad
import aiobot.handlers.admin as admin
import asyncio
import logging
import requests
import socket
from aiohttp import web
from dispatcher.dispatcher import dis, bot
from aiobot.database import db
from network_config import setup_network_logging, get_polling_settings

# Настройка логирования для продакшна
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Настройка сетевого логирования
setup_network_logging()

load_dotenv()

dis.include_router(commands.router)
dis.include_router(ad.router)
dis.include_router(user.router)
dis.include_router(admin.router)

def get_free_port():
    """Находит свободный порт"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def get_public_ip():
    """Получает публичный IP адрес"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return None

async def on_startup():
    await db.init()
    await db.create_all()
    
    # Получаем публичный IP
    public_ip = get_public_ip()
    if public_ip:
        logger.info(f"Public IP detected: {public_ip}")
        print(f"🌐 Публичный IP: {public_ip}")
    else:
        logger.warning("Could not detect public IP")
        print("⚠️  Не удалось определить публичный IP")
        return False
    
    return True

async def on_shutdown():
    # Удаляем webhook при остановке
    try:
        await bot.delete_webhook()
        logger.info("Webhook removed")
    except:
        pass

async def webhook_handler(request):
    """Обработчик webhook запросов от Telegram"""
    if request.match_info.get('token') == bot.token:
        update = await request.json()
        await dis.feed_webhook_update(bot, update)
        return web.Response()
    else:
        return web.Response(status=403)

def try_webhook_mode():
    """Пытается запустить webhook режим"""
    try:
        # Находим свободный порт
        port = get_free_port()
        print(f"🔍 Найден свободный порт: {port}")
        
        # Создаем приложение
        app = web.Application()
        
        # Добавляем маршрут для webhook
        app.router.add_post("/webhook/{token}", webhook_handler)
        app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
        app.router.add_get("/status", lambda r: web.Response(text="Bot is online!"))
        
        # Настройки запуска
        web.run_app(
            app,
            host="0.0.0.0",
            port=port,
        )
        return True
    except Exception as e:
        logger.error(f"Webhook mode failed: {e}")
        return False

def polling_mode():
    """Запускает polling режим"""
    print("🔄 Переключение на polling режим...")
    
    async def main():
        await on_startup()
        
        # Используем улучшенные настройки polling
        polling_settings = get_polling_settings()
        
        print("[INFO] Bot started in polling mode (fallback)")
        print("[INFO] Using enhanced error handling and connection settings")
        
        try:
            await dis.start_polling(bot, **polling_settings)
        except Exception as e:
            logger.error(f"Critical error in polling: {e}")
            # Попытка перезапуска через некоторое время
            await asyncio.sleep(5)
            await main()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"[ERROR] Bot crashed: {e}")

if __name__ == '__main__':
    try:
        print("🚀 Запуск бота в продакшн режиме...")
        print("📋 Проверка настроек...")
        
        # Запускаем startup
        startup_success = asyncio.run(on_startup())
        
        if not startup_success:
            print("❌ Не удалось определить публичный IP")
            print("🔄 Переключение на polling режим...")
            polling_mode()
            exit()
        
        print("⚠️  ВНИМАНИЕ: Telegram требует HTTPS для webhook!")
        print("💡 Рекомендуется использовать polling режим без домена")
        print()
        
        choice = input("Выберите режим:\n1. Polling (рекомендуется)\n2. Webhook (экспериментально)\nВаш выбор (1/2): ").strip()
        
        if choice == "1" or choice == "":
            polling_mode()
        else:
            print("🔄 Попытка запуска webhook режима...")
            if not try_webhook_mode():
                print("❌ Webhook режим не удался")
                print("🔄 Переключение на polling режим...")
                polling_mode()
                
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user")
        asyncio.run(on_shutdown())
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"[ERROR] Bot crashed: {e}")
        asyncio.run(on_shutdown()) 