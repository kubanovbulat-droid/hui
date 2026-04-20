#!/usr/bin/env python3
"""
Скрипт установки проекта
"""

import os
import subprocess
import sys


def create_directories():
    """Создание необходимых директорий"""
    directories = [
        "data/raw",
        "data/processed",
        "data/logs",
        "logs",
        "config",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана директория: {directory}")


def install_dependencies():
    """Установка зависимостей"""
    print("Установка зависимостей...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def create_env_file():
    """Создание файла .env"""
    env_content = """# Database
DATABASE_URL=sqlite:///data/scraper.db

# Logging
LOG_LEVEL=INFO

# Scraping
REQUEST_TIMEOUT=10
DELAY_BETWEEN_REQUESTS=1.0

# Notifications
SLACK_WEBHOOK_URL=
"""

    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("Создан файл .env")
    else:
        print("Файл .env уже существует")


def main():
    """Основная функция"""
    print("Установка проекта...")

    create_directories()
    create_env_file()
    install_dependencies()

    print("\nУстановка завершена!")
    print("Для продолжения:")
    print("1. Настройте файл .env")
    print("2. Запустите: python scripts/run_scraper.py")


if __name__ == "__main__":
    main()