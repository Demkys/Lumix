import time
import requests
from pyrogram import filters

# Функция для проверки доступности сайта
def check_url_availability(url):
    try:
        response = requests.get(url, timeout=5)  # Установим таймаут в 5 секунд
        return response.status_code == 200
    except requests.RequestException:
        return False

def register(app):
    @app.on_message(filters.command("ping", prefixes=".") & filters.me)
    async def ping_pong(_, msg):
        # Получаем текст команды и проверяем наличие URL
        command_parts = msg.text.split()
        url_to_check = None

        if len(command_parts) > 1:
            url_to_check = command_parts[1]

        if url_to_check:
            # Проверяем доступность указанного URL
            await msg.edit(f"Проверяю доступность {url_to_check}...")
            is_available = check_url_availability(url_to_check)

            if is_available:
                await msg.edit(f"Сайт {url_to_check} доступен!")
            else:
                await msg.edit(f"Сайт {url_to_check} недоступен или произошла ошибка при попытке подключения.")
        else:
            # Измеряем задержку, если URL не указан
            start_time = time.time()
            await msg.edit("Pong!")
            end_time = time.time()
            ping_duration = end_time - start_time
            await msg.edit(f"Pong! Задержка: {ping_duration:.2f} секунд")
