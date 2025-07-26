# Настройка бота для продакшна

## Варианты запуска

### 1. Webhook режим (рекомендуется для продакшна)

#### С SSL сертификатами (безопасно)
```bash
python main_production.py
```

#### Без SSL (для тестирования)
```bash
python main_production_simple.py
```

### 2. Polling режим (для разработки)
```bash
python main.py
```

## Настройка для продакшна

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
TOKEN=your_bot_token_here
```

### 2. Настройка домена и SSL

#### Вариант A: С собственным доменом
1. Замените `your-domain.com` в файле на ваш реальный домен
2. Получите SSL сертификат (например, через Let's Encrypt)
3. Поместите сертификаты в папку `ssl/`:
   - `ssl/cert.pem` - публичный сертификат
   - `ssl/private.key` - приватный ключ

#### Вариант B: С IP адресом
1. Замените `your-domain.com` на IP адрес вашего сервера
2. Используйте `main_production_simple.py` для запуска без SSL

### 3. Настройка портов

По умолчанию:
- С SSL: порт 8443
- Без SSL: порт 8080

Измените `WEBHOOK_PORT` в файле если нужно.

### 4. Настройка файрвола

Откройте нужный порт на сервере:
```bash
# Для Ubuntu/Debian
sudo ufw allow 8443
sudo ufw allow 8080

# Для CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8443/tcp
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

### 5. Запуск как служба (systemd)

Создайте файл `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/bot
Environment=PATH=/path/to/your/bot/venv/bin
ExecStart=/path/to/your/bot/venv/bin/python main_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### 6. Мониторинг

Логи сохраняются в файл `bot.log`:
```bash
tail -f bot.log
```

## Проверка работы

1. Запустите бота
2. Отправьте команду `/start` боту
3. Проверьте логи на наличие ошибок

## Устранение проблем

### Бот не отвечает
1. Проверьте, что токен правильный
2. Убедитесь, что порт открыт
3. Проверьте логи: `tail -f bot.log`

### Webhook ошибки
1. Убедитесь, что домен/IP доступен из интернета
2. Проверьте SSL сертификаты (если используете)
3. Проверьте настройки файрвола

### Проблемы с базой данных
1. Убедитесь, что файл `db.sqlite` доступен для записи
2. Проверьте права доступа к папке

## Рекомендации для продакшна

1. **Всегда используйте SSL** в продакшне
2. **Настройте мониторинг** (например, через systemd)
3. **Регулярно делайте бэкапы** базы данных
4. **Используйте reverse proxy** (nginx) для дополнительной безопасности
5. **Настройте логирование** в отдельную папку
6. **Используйте переменные окружения** для конфигурации 