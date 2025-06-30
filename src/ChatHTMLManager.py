from bs4 import BeautifulSoup
from pathlib import Path


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