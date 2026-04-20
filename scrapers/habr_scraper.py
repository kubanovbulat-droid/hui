from typing import List, Dict
from .base_scraper import BaseScraper


class HabrScraper(BaseScraper):
    """
    Скрапер для сайта Habr
    """

    def __init__(self):
        super().__init__("https://habr.com")

    def extract_articles(self, soup) -> List[Dict]:
        """
        Извлечение статей с Habr

        Args:
            soup: BeautifulSoup объект

        Returns:
            Список словарей со статьями
        """
        articles = []

        # Поиск статей по CSS-селектору
        article_elements = soup.find_all("article", class_="tm-articles-list__item")

        for element in article_elements:
            try:
                # Заголовок
                title_element = element.find("a", class_="tm-title__link")
                title = title_element.text.strip() if title_element else "Без заголовка"

                # Ссылка
                url = title_element["href"] if title_element else ""
                full_url = f"{self.base_url}{url}" if url else ""

                # Автор
                author_element = element.find("a", class_="tm-user-info__username")
                author = author_element.text.strip() if author_element else "Неизвестный автор"

                # Рейтинг
                rating_element = element.find("span", class_="tm-votes-meter__value")
                rating = rating_element.text.strip() if rating_element else "0"

                # Дата
                date_element = element.find("time")
                date = date_element["datetime"] if date_element else ""

                articles.append({
                    "источник": "Habr",
                    "заголовок": title,
                    "ссылка": full_url,
                    "автор": author,
                    "рейтинг": rating,
                    "дата": date
                })
            except Exception as e:
                print(f"Ошибка при извлечении статьи: {e}")
                continue

        return articles

    def get_hub_articles(self, hub_name: str, pages: int = 1) -> List[Dict]:
        """
        Получение статей из хаба

        Args:
            hub_name: Название хаба
            pages: Количество страниц

        Returns:
            Список статей
        """
        urls = [f"{self.base_url}/ru/hub/{hub_name}/page{i}/" for i in range(1, pages + 1)]
        return self.run(urls)