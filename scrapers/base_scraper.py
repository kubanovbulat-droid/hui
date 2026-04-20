import requests
from bs4 import BeautifulSoup
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time


class BaseScraper(ABC):
    """
    Базовый класс для веб-скраперов.
    Содержит общую логику для всех скраперов.
    """

    def __init__(self, base_url: str):
        """
        Инициализация скрапера

        Args:
            base_url: Базовый URL сайта
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def get_page(self, url: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        Получение страницы

        Args:
            url: URL страницы
            params: Параметры запроса

        Returns:
            Response объект или None при ошибке
        """
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Парсинг HTML

        Args:
            html: HTML строка

        Returns:
            BeautifulSoup объект
        """
        return BeautifulSoup(html, "html.parser")

    @abstractmethod
    def extract_articles(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Извлечение статей из HTML
        (абстрактный метод, должен быть реализован в наследниках)

        Args:
            soup: BeautifulSoup объект

        Returns:
            Список словарей со статьями
        """
        pass

    def scrape_page(self, url: str) -> Optional[List[Dict]]:
        """
        Скрапинг одной страницы

        Args:
            url: URL страницы

        Returns:
            Список словарей со статьями или None
        """
        response = self.get_page(url)
        if not response:
            return None

        soup = self.parse_html(response.text)
        articles = self.extract_articles(soup)

        return articles

    def scrape_multiple_pages(self, urls: List[str]) -> List[Dict]:
        """
        Скрапинг нескольких страниц

        Args:
            urls: Список URL

        Returns:
            Список всех статей
        """
        all_articles = []

        for i, url in enumerate(urls, 1):
            print(f"Обработка страницы {i}/{len(urls)}: {url}")
            articles = self.scrape_page(url)

            if articles:
                all_articles.extend(articles)

            # Задержка между запросами
            if i < len(urls):
                time.sleep(1)

        return all_articles

    def save_to_json(self, data: List[Dict], filename: str) -> None:
        """
        Сохранение данных в JSON

        Args:
            data: Список данных
            filename: Имя файла
        """
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в {filename}")

    def save_to_database(self, data: List[Dict], db_name: str, table_name: str) -> None:
        """
        Сохранение данных в базу данных SQLite

        Args:
            data: Список данных
            db_name: Имя базы данных
            table_name: Имя таблицы
        """
        import sqlite3

        if not data:
            print("Нет данных для сохранения")
            return

        # Создание таблицы
        columns = list(data[0].keys())
        column_defs = ", ".join([f"{col} TEXT" for col in columns])

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {column_defs}
            )
        """)

        # Вставка данных
        placeholders = ", ".join(["?"] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        for article in data:
            values = [str(article.get(col, "")) for col in columns]
            cursor.execute(insert_query, values)

        connection.commit()
        connection.close()
        print(f"Данные сохранены в {db_name} (таблица: {table_name})")

    def run(self, urls: List[str], output_file: str = None) -> List[Dict]:
        """
        Основной метод запуска скрапера

        Args:
            urls: Список URL для скрапинга
            output_file: Имя файла для сохранения (опционально)

        Returns:
            Список собранных данных
        """
        print(f"Запуск скрапера для {len(urls)} страниц")
        data = self.scrape_multiple_pages(urls)
        print(f"Собрано {len(data)} статей")

        if output_file:
            self.save_to_json(data, output_file)

        return data