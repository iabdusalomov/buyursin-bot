import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("[INFO] Bot started in polling mode")
    print(f"[INFO] TOKEN: {os.getenv('TOKEN', 'NOT_SET')}")
    print(f"[INFO] ADMIN_GROUP_ID: {os.getenv('ADMIN_GROUP_ID', 'NOT_SET')}")
    print(f"[INFO] CHANNEL_ID: {os.getenv('CHANNEL_ID', 'NOT_SET')}")
    
    # Простой бесконечный цикл для тестирования
    while True:
        print("[INFO] Bot is running...")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main()) 