#!/usr/bin/env python3
"""
Скрипт запуска скрапера
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.habr_scraper import HabrScraper
from scrapers.dzen_scraper import DzenScraper
from config.settings import settings
import logging


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )


def run_habr_scraper():
    """Запуск скрапера для Habr"""
    logger = logging.getLogger(__name__)
    logger.info("Запуск скрапера для Habr")

    scraper = HabrScraper()
    urls = [f"https://habr.com/ru/hub/python/page{i}/" for i in range(1, 3)]

    data = scraper.run(urls, "data/raw/habr_articles.json")
    logger.info(f"Собрано {len(data)} статей с Habr")

    return data


def run_dzen_scraper():
    """Запуск скрапера для Dzen"""
    logger = logging.getLogger(__name__)
    logger.info("Запуск скрапера для Dzen")

    scraper = DzenScraper()
    urls = [f"https://dzen.ru/news/python/page{i}/" for i in range(1, 3)]

    data = scraper.run(urls, "data/raw/dzen_articles.json")
    logger.info(f"Собрано {len(data)} статей с Dzen")

    return data


def main():
    """Основная функция"""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=" * 50)
    logger.info("Запуск скрапера")
    logger.info("=" * 50)

    try:
        # Запуск скраперов
        habr_data = run_habr_scraper()
        dzen_data = run_dzen_scraper()

        total = len(habr_data) + len(dzen_data)
        logger.info(f"Всего собрано {total} статей")

        logger.info("Завершено успешно!")

    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()