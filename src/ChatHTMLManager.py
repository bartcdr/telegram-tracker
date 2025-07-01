from bs4 import BeautifulSoup
from pathlib import Path
import re

class ChatHTMLManager:
    """Класс для работы с файлом chats.html."""

    def __init__(self, html_path: Path):
        self.html_path = html_path
        self.soup = self._load_html()

    def _load_html(self) -> BeautifulSoup:
        """Загружает HTML-содержимое."""
        if not self.html_path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.html_path}")
        with self.html_path.open(encoding="utf-8") as f:
            return BeautifulSoup(f, "html.parser")

    def _save_html(self) -> None:
        """Сохраняет изменения в файл."""
        with self.html_path.open("w", encoding="utf-8") as f:
            f.write(str(self.soup))

    def user_exists(self, name: str) -> bool:
        """Проверяет, есть ли пользователь по имени."""
        entries = self.soup.select(".entry .name.bold")
        return any(name.strip() in entry.get_text(strip=True) for entry in entries)

    def add_user(self, name: str, initial: str, href: str, messages_count: int, chat_type: str = "private") -> None:
        """Добавляет нового пользователя в HTML."""
        if self.user_exists(name):
            return

        entry_list = self.soup.select_one(".entry_list")
        if not entry_list:
            raise ValueError("Не найдена точка вставки (.entry_list) в HTML.")

        new_entry = BeautifulSoup(f"""
        <a class="entry block_link clearfix" href="{href}">
          <div class="pull_left userpic_wrap">
           <div class="userpic userpic7" style="width: 48px; height: 48px">
            <div class="initials" style="line-height: 48px">
              {initial}
            </div>
           </div>
          </div>
          <div class="body">
           <div class="pull_right info details">{chat_type}</div>
           <div class="name bold">{name}</div>
           <div class="details_entry details">{messages_count} messages</div>
          </div>
        </a>
        """, "html.parser")

        entry_list.append(new_entry)
        self._save_html()

    def get_next_chat_folder(self) -> Path:
        """Создает следующую папку чата (chat_001, chat_002 и т.д.)."""
        base_dir = self.html_path.parent.parent
        chats_dir = base_dir / "chats"
        chats_dir.mkdir(parents=True, exist_ok=True)
        existing_numbers = [int(d.name.split('_')[1]) for d in chats_dir.iterdir() if d.is_dir() and re.match(r"chat_\d{3}", d.name)]
        next_number = max(existing_numbers, default=0) + 1
        chat_folder = chats_dir / f"chat_{next_number:03d}"
        chat_folder.mkdir()
        return chat_folder

    def get_chat_folder_for_existing_user(self, name: str) -> Path:
        """Находит папку чата для существующего пользователя."""
        entries = self.soup.select(".entry .name.bold")
        for entry in entries:
            if name.strip() in entry.get_text(strip=True):
                a_tag = entry.find_parent("a")
                if a_tag:
                    href = a_tag['href']
                    chat_dir = href.split('/')[2]  # e.g., "chat_001"
                    base_dir = self.html_path.parent.parent
                    return base_dir / "chats" / chat_dir
        raise ValueError(f"Пользователь {name} не найден в chats.html")

    def get_message_count(self, name: str) -> int:
        """Получает текущее количество сообщений для пользователя."""
        entries = self.soup.select(".entry .name.bold")
        for entry in entries:
            if name.strip() in entry.get_text(strip=True):
                details_entry = entry.find_next_sibling("div", class_="details_entry details")
                if details_entry:
                    text = details_entry.get_text(strip=True)
                    match = re.search(r"(\d+) messages", text)
                    if match:
                        return int(match.group(1))
        raise ValueError(f"Пользователь {name} не найден в chats.html")

    def update_message_count(self, name: str, new_count: int) -> None:
        """Обновляет количество сообщений для пользователя."""
        entries = self.soup.select(".entry .name.bold")
        for entry in entries:
            if name.strip() in entry.get_text(strip=True):
                details_entry = entry.find_next_sibling("div", class_="details_entry details")
                if details_entry:
                    details_entry.string = f"{new_count} messages"
                    self._save_html()
                    return
        raise ValueError(f"Пользователь {name} не найден в chats.html")

    def create_chat_messages_html(self, folder: Path, name: str, initial: str, messages: list) -> None:
        """Создает новый файл messages.html с начальными сообщениями."""
        html_content = f"""<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  <title>Exported Data</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <link href="../../css/style.css" rel="stylesheet"/>
  <script src="../../js/script.js" type="text/javascript"></script>
 </head>
 <body onload="CheckLocation();">
  <div class="page_wrap">
   <div class="page_header">
    <a class="content block_link" href="../../lists/chats.html" onclick="return GoBack(this)">
     <div class="text bold">{name}</div>
    </a>
   </div>
   <div class="page_body chat_page">
    <div class="history">
"""
        for msg in messages:
            message_html = f"""
     <div class="message default clearfix" id="message{msg['id']}">
      <div class="pull_left userpic_wrap">
       <div class="userpic userpic7" style="width: 42px; height: 42px">
        <div class="initials" style="line-height: 42px">{initial}</div>
       </div>
      </div>
      <div class="body">
       <div class="pull_right date details" title="{msg['timestamp']}">
        {msg['time']}
       </div>
       <div class="from_name">{msg['sender_name']}</div>
       <div class="text">{msg['text']}</div>
      </div>
     </div>
            """
            html_content += message_html

        html_content += """
    </div>
   </div>
  </div>
 </body>
</html>
"""
        (folder / "messages.html").write_text(html_content, encoding="utf-8")

    def append_message_to_chat(self, chat_folder: Path, message_data: dict) -> None:
        """Добавляет новое сообщение в существующий messages.html."""
        messages_html = chat_folder / "messages.html"
        if not messages_html.exists():
            raise FileNotFoundError(f"messages.html не найден в {chat_folder}")

        with messages_html.open(encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        history_div = soup.find("div", class_="history")
        if not history_div:
            raise ValueError("History div не найден в messages.html")

        new_message = BeautifulSoup(f"""
     <div class="message default clearfix" id="message{message_data['id']}">
      <div class="pull_left userpic_wrap">
       <div class="userpic userpic7" style="width: 42px; height: 42px">
        <div class="initials" style="line-height: 42px">{message_data['initial']}</div>
       </div>
      </div>
      <div class="body">
       <div class="pull_right date details" title="{message_data['timestamp']}">
        {message_data['time']}
       </div>
       <div class="from_name">{message_data['sender_name']}</div>
       <div class="text">{message_data['text']}</div>
      </div>
     </div>
        """, "html.parser")

        history_div.append(new_message)
        with messages_html.open("w", encoding="utf-8") as f:
            f.write(str(soup))

    def update_message_in_chat(self, chat_folder: Path, message_id: int, new_text: str, edit_time: str) -> None:
        """Обновляет сообщение в messages.html при редактировании."""
        messages_html = chat_folder / "messages.html"
        if not messages_html.exists():
            raise FileNotFoundError(f"messages.html не найден в {chat_folder}")

        with messages_html.open(encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        message_div = soup.find("div", id=f"message{message_id}")
        if not message_div:
            raise ValueError(f"Сообщение с id {message_id} не найдено")

        text_div = message_div.find("div", class_="text")
        if not text_div:
            raise ValueError("div.text не найден в сообщении")

        current_inner_html = text_div.decode_contents()
        new_inner_html = current_inner_html + f"<br/>edited {new_text}"
        text_div.clear()
        text_div.append(BeautifulSoup(new_inner_html, "html.parser"))

        if not message_div.find("div", class_="edited"):
            edited_div = BeautifulSoup('<div class="edited">Edited</div>', "html.parser")
            message_div.find("div", class_="body").append(edited_div)

        with messages_html.open("w", encoding="utf-8") as f:
            f.write(str(soup))