import asyncio
from Сonfig import Config
from TelegramClient import TelegramClientManager
from MessageHandler import MessageHandler

async def main():
    """Основная функция для запуска приложения."""
    try:
        # Загружаем конфигурацию
        config = Config()
        apiId, apiHash, sessionName = config.getConfig()

        # Инициализируем клиент
        clientManager = TelegramClientManager(apiId, apiHash, sessionName)

        # Регистрируем обработчик сообщений
        clientManager.registerMessageHandler(MessageHandler.handleMessage)

        # Запускаем клиент
        await clientManager.start()
        await clientManager.run()

    except Exception as e:
        print(f"Ошибка приложения: {e}")

if __name__ == "__main__":
    asyncio.run(main())