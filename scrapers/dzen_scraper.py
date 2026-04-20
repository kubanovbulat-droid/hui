from typing import List, Dict
from .base_scraper import BaseScraper


class DzenScraper(BaseScraper):
    """
    Скрапер для сайта Dzen
    """

    def __init__(self):
        super().__init__("https://dzen.ru")

    def extract_articles(self, soup) -> List[Dict]:
        """
        Извлечение статей с Dzen

        Args:
            soup: BeautifulSoup объект

        Returns:
            Список словарей со статьями
        """
        articles = []

        # Поиск статей по CSS-селектору
        article_elements = soup.find_all("div", class_="card-compact-view")

        for element in article_elements:
            try:
                # Заголовок
                title_element = element.find("a", class_="card-compact-view__title-link")
                title = title_element.text.strip() if title_element else "Без заголовка"

                # Ссылка
                url = title_element["href"] if title_element else ""

                # Автор
                author_element = element.find("span", class_="card-compact-view__author")
                author = author_element.text.strip() if author_element else "Неизвестный автор"

                # Время
                time_element = element.find("span", class_="card-compact-view__time")
                time = time_element.text.strip() if time_element else ""

                articles.append({
                    "источник": "Dzen",
                    "заголовок": title,
                    "ссылка": url,
                    "автор": author,
                    "время": time
                })
            except Exception as e:
                print(f"Ошибка при извлечении статьи: {e}")
                continue

        return articles

    def get_tag_articles(self, tag: str, pages: int = 1) -> List[Dict]:
        """
        Получение статей по тегу

        Args:
            tag: Тег для поиска
            pages: Количество страниц

        Returns:
            Список статей
        """
        urls = [f"{self.base_url}/news/{tag}/page{i}/" for i in range(1, pages + 1)]
        return self.run(urls)