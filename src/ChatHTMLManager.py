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
        """Находит следующую доступную папку chat_XXX и создаёт её."""
        base_dir = self.html_path.parent.parent  # Папка DataExport*/
        chats_dir = base_dir / "chats"
        chats_dir.mkdir(parents=True, exist_ok=True)

        existing = sorted(
            (d for d in chats_dir.iterdir() if d.is_dir() and re.match(r"chat_\d{3}", d.name)),
            key=lambda d: int(d.name.split("_")[1])
        )

        next_number = (int(existing[-1].name.split("_")[1]) + 1) if existing else 1
        next_folder = chats_dir / f"chat_{next_number:03d}"
        next_folder.mkdir()
        return next_folder

    def create_chat_messages_html(self, folder: Path, name: str, initial: str) -> None:
        """Создаёт файл messages.html в новой папке."""
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
     <div class="message service" id="message-1">
      <div class="body details">1 July 2025</div>
     </div>
     <div class="message default clearfix" id="message1">
      <div class="pull_left userpic_wrap">
       <div class="userpic userpic7" style="width: 42px; height: 42px">
        <div class="initials" style="line-height: 42px">{initial}</div>
       </div>
      </div>
      <div class="body">
       <div class="pull_right date details" title="01.07.2025 00:00:00 UTC+03:00">00:00</div>
       <div class="from_name">{name}</div>
       <div class="text">Чат создан автоматически.</div>
      </div>
     </div>
    </div>
   </div>
  </div>

 </body>
</html>
"""
        (folder / "messages.html").write_text(html_content, encoding="utf-8")