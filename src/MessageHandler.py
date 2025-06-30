from telethon.tl.types import Message
from typing import Any
from pathlib import Path
from ChatHTMLManager import ChatHTMLManager
from datetime import timedelta


def find_chats_html() -> Path:
    """Ищет файл chats.html по шаблону DataExport*/lists/chats.html."""
    matches = list(Path(".").glob("DataExport*/lists/chats.html"))
    if not matches:
        raise FileNotFoundError("Файл chats.html не найден по шаблону DataExport*/lists/chats.html")
    return matches[0]


class MessageHandler:
    """Класс для обработки входящих сообщений."""
    chat_manager = ChatHTMLManager(find_chats_html())

    @staticmethod
    async def handleMessage(event: Any) -> None:
        """Обрабатывает входящее сообщение и синхронизирует с HTML."""
        message: Message = event.message
        sender = await event.get_sender()
        if sender:
            first_name = getattr(sender, "first_name", "")
            last_name = getattr(sender, "last_name", "")
            username = getattr(sender, "username", "")
            display_name = f"{first_name} {last_name}".strip() or "Unknown"
            sender_name = display_name
            if username:
                sender_name += f" (@{username})"

            try:
                initial = display_name[0].upper()

                # Получаем текущее время в UTC и добавляем 3 часа для Минска
                local_time = message.date + timedelta(hours=3)

                if not MessageHandler.chat_manager.user_exists(display_name):
                    # Новый пользователь
                    chat_folder = MessageHandler.chat_manager.get_next_chat_folder()
                    chat_name = chat_folder.name
                    href = f"../chats/{chat_name}/messages.html#allow_back"
                    MessageHandler.chat_manager.add_user(
                        name=display_name,
                        initial=initial,
                        href=href,
                        messages_count=1
                    )
                    messages = [{
                        "id": message.id,
                        "sender_name": sender_name,
                        "text": message.text or "Non-text message",
                        "timestamp": local_time.strftime("%d.%m.%Y %H:%M:%S UTC+3"),
                        "time": local_time.strftime("%H:%M"),
                        "initial": initial
                    }]
                    MessageHandler.chat_manager.create_chat_messages_html(chat_folder, display_name, initial, messages)
                else:
                    # Существующий пользователь
                    chat_folder = MessageHandler.chat_manager.get_chat_folder_for_existing_user(display_name)
                    current_count = MessageHandler.chat_manager.get_message_count(display_name)
                    MessageHandler.chat_manager.update_message_count(display_name, current_count + 1)
                    message_data = {
                        "id": message.id,
                        "sender_name": sender_name,
                        "text": message.text or "Non-text message",
                        "timestamp": local_time.strftime("%d.%m.%Y %H:%M:%S UTC+3"),
                        "time": local_time.strftime("%H:%M"),
                        "initial": initial
                    }
                    MessageHandler.chat_manager.append_message_to_chat(chat_folder, message_data)
            except Exception as e:
                print(f"[HTML Sync Error]: {e}")
        else:
            sender_name = "Unknown Sender"

        if message.text:
            print(f"From {sender_name}: {message.text}")
        else:
            print(f"From {sender_name}: Received a non-text message (e.g., media, sticker)")