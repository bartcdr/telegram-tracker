from telethon.tl.types import Message
from typing import Any
from pathlib import Path
from ChatHTMLManager import ChatHTMLManager


def find_chats_html() -> Path:
    """Ищет файл chats.html по шаблону DataExport*/lists/chats.html."""
    matches = list(Path(".").glob("DataExport*/lists/chats.html"))
    if not matches:
        raise FileNotFoundError("Файл chats.html не найден по шаблону DataExport*/lists/chats.html")
    return matches[0]


class MessageHandler:
    """Класс для обработки входящих сообщений."""

    # Инициализация ChatHTMLManager для работы с chats.html
    chat_manager = ChatHTMLManager(find_chats_html())

    @staticmethod
    async def handleMessage(event: Any) -> None:
        """Обрабатывает входящее сообщение и выводит его в терминал.

        Args:
            event (Any): Событие сообщения от Telethon.
        """
        message: Message = event.message

        sender = await event.get_sender()
        if sender:
            first_name = getattr(sender, "first_name", "")
            last_name = getattr(sender, "last_name", "")
            username = getattr(sender, "username", "")
            sender_id = getattr(sender, "id", None)

            # Формируем полное имя отправителя
            display_name = f"{first_name} {last_name}".strip() or "Unknown"
            sender_name = display_name
            if username:
                sender_name += f" (@{username})"

            # Добавляем нового пользователя в chats.html
            try:
                initial = display_name[0].upper()

                # Получаем имя следующего чата (например, chat_001)
                chat_folder = MessageHandler.chat_manager.get_next_chat_folder()
                chat_name = chat_folder.name  # Это будет "chat_001", "chat_002" и т.д.
                href = f"../chats/{chat_name}/messages.html#allow_back"

                # Добавляем пользователя в список
                MessageHandler.chat_manager.add_user(
                    name=display_name,
                    initial=initial,
                    href=href,
                    messages_count=0  # Начальное количество сообщений
                )

                # Создаём новый чат, если это первый раз
                MessageHandler.chat_manager.create_chat_messages_html(chat_folder, display_name, initial)

            except Exception as e:
                print(f"[HTML Sync Error]: {e}")
        else:
            sender_name = "Unknown Sender"

        # Выводим сообщение в консоль
        if message.text:
            print(f"From {sender_name}: {message.text}")
        else:
            print(f"From {sender_name}: Received a non-text message (e.g., media, sticker)")