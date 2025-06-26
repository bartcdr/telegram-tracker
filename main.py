from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Замените на ваши API ID и Hash
# Перейдите на https://my.telegram.org, войдите, выберите 'API development tools',
# создайте приложение и скопируйте api_id и api_hash.

# Загружаем переменные из .env
load_dotenv(dotenv_path="configuration.env")

api_id = os.getenv("API_ID")  # Ваш API ID
api_hash = os.getenv("API_HASH")  # Ваш API Hash

# Имя сессии, может быть любым
session_name = os.getenv("SESSION_NAME")

# Проверка
if not api_id:
    raise RuntimeError("Не найден API_ID в файле configuration.env")
elif not api_hash:
    raise RuntimeError("Не найден API_HASH в файле configuration.env")

# Приводим api_id к числу
try:
    api_id = int(api_id)
except ValueError:
    raise RuntimeError("❌ API_ID должен быть числом (int), а не строкой или другим типом")

# Создаём клиент
client = TelegramClient(session_name, api_id, api_hash)

# Обработчик новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    if event.message.text:
        print(f"Text message: {event.message.text}")
    else:
        print("Received a non-text message (e.g., media, sticker)")

# Запускаем клиент и слушаем сообщения
try:
    client.start()
    print("Клиент запущен. Ожидаем сообщения...")
    client.run_until_disconnected()
except Exception as e:
    print(f"Произошла ошибка: {e}")