#!/usr/bin/env python3
"""
Скрипт для запуска бота в продакшн режиме
Используйте переменные окружения для настройки
"""

import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки из переменных окружения
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "your-domain.com")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
USE_SSL = os.getenv("USE_SSL", "true").lower() == "true"

def main():
    print("=== Telegram Bot Production Launcher ===")
    print(f"Host: {WEBHOOK_HOST}")
    print(f"Port: {WEBHOOK_PORT}")
    print(f"SSL: {USE_SSL}")
    print(f"Webhook URL: {'https' if USE_SSL else 'http'}://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}")
    print()
    
    if WEBHOOK_HOST == "your-domain.com":
        print("⚠️  ВНИМАНИЕ: Не забудьте настроить WEBHOOK_HOST в .env файле!")
        print("   Пример: WEBHOOK_HOST=your-domain.com")
        print()
    
    # Выбираем файл для запуска
    if USE_SSL:
        print("🚀 Запуск с SSL (рекомендуется для продакшна)...")
        print("   Убедитесь, что SSL сертификаты настроены в main_production.py")
        os.system(f"{sys.executable} main_production.py")
    else:
        print("🚀 Запуск без SSL (для тестирования)...")
        print("   ⚠️  Не рекомендуется для продакшна!")
        os.system(f"{sys.executable} main_production_simple.py")

if __name__ == "__main__":
    main() 