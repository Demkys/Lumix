import os
import time
import socket
import sys
import requests
from pyrogram import Client, filters
from colorama import Fore, Style
from art import text2art
import importlib.util
import logging
import asyncio
import subprocess

# Папка для сессий и логов
session_folder = "sessions"
logs_folder = "logs"

# Список необходимых библиотек
required_libraries = ['pyrogram', 'requests', 'colorama', 'art']

# Функция для установки недостающих библиотек
def install_libraries():
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{Fore.RED}Библиотека {library} не найдена. Устанавливаем...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Установка недостающих библиотек
install_libraries()

app = Client("Lumix")

# Создаем директории
os.makedirs(session_folder, exist_ok=True)
os.makedirs(logs_folder, exist_ok=True)

# Лог-файл
log_filename = os.path.join(logs_folder, time.strftime("log(%Y-%m-%d, %H-%M-%S).log"))
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для форматированного вывода сообщений с временем
def log_message(message, color=Fore.WHITE, bold=False):
    current_time = time.strftime("%d-%m-%Y %H:%M:%S")
    if bold:
        message = f"{Style.BRIGHT}{message}{Style.RESET_ALL}"
    print(f"{color}[{current_time}]> {message}{Style.RESET_ALL}")

# Проверка файлов сессии
if not os.path.exists(os.path.join(session_folder, "Lumix.session")):
    logging.warning("Файлы сессии не найдены")
    log_message("Начнем первоначальную настройку", Fore.GREEN, bold=True)

    log_message("Введите API ID: ", Fore.GREEN)
    api_id = input()  # Получаем API ID
    log_message("Введите API Hash: ", Fore.GREEN)
    api_hash = input()  # Получаем API Hash
    log_message("Введите номер телефона, привязанный к Телеграмм: ", Fore.GREEN)
    phone_number = input()  # Получаем номер телефона

    app = Client(
        os.path.join(session_folder, "Lumix"),
        api_id=api_id,
        api_hash=api_hash,
        phone_number=phone_number
    )

    with open(os.path.join(session_folder, "config.txt"), "w") as config_file:
        config_file.write(f"API_ID: {api_id}\nAPI_HASH: {api_hash}\n")
    logging.info("API ID и API Hash сохранены в конфигурационный файл")

else:
    with open(os.path.join(session_folder, "config.txt"), "r") as config_file:
        for line in config_file:
            if line.startswith("API_ID"):
                api_id = line.split(":")[1].strip()
            elif line.startswith("API_HASH"):
                api_hash = line.split(":")[1].strip()

    app = Client(
        os.path.join(session_folder, "Lumix"),
        api_id=api_id,
        api_hash=api_hash
    )

# Логотип и приветствие
def print_logo():
    logo = text2art("Lumix", font='small')
    print(Fore.LIGHTMAGENTA_EX + logo + Style.RESET_ALL)

print_logo()
log_message("Lumix запущен, привет " + socket.gethostname(), Fore.GREEN, bold=True)

# Версия
version = "5.0"
log_message(f"Текущая версия : {version}", Fore.CYAN)

# Подключение плагинов
plugins_dir = "plugins"
for plugin_file in os.listdir(plugins_dir):
    if plugin_file.endswith(".py"):
        plugin_path = os.path.join(plugins_dir, plugin_file)
        plugin_name = os.path.splitext(plugin_file)[0]
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            plugin_module.register(app)
            logging.info(f"Плагин {plugin_name} зарегистрирован")
            log_message(f"Плагин {plugin_name} зарегистрирован", Fore.LIGHTYELLOW_EX)  # Подходящий цвет для плагина
        except Exception as e:
            logging.error(f"Ошибка с плагином {plugin_name}: {str(e)}")
            log_message(f"Ошибка с плагином {plugin_name}: {str(e)}", Fore.RED)

# Момент времени, когда бот был запущен
start_time = time.time()

# Команда .about
@app.on_message(filters.command("about", prefixes=".") & filters.me)
async def about_command(_, msg):
    # Рассчитываем время с последнего запуска
    last_start_time = time.time() - start_time
    hours, remainder = divmod(last_start_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    last_start_formatted = f"{int(hours)} ч {int(minutes)} мин {int(seconds)} сек"

    about_text = (
        "💡Lumix:\n"
        f"🚀Версия: {version}\n"
        f"⚡Последний запуск: {last_start_formatted} назад"
    )
    await msg.reply(about_text)

# Команда .reset
@app.on_message(filters.command("reset", prefixes=".") & filters.me)
async def reset_bot(_, msg):
    await msg.edit("Перезапуск\nПотребуется некоторое время....")
    await asyncio.sleep(3)
    await msg.edit("Lumix перезагружен")

    # Перезапуск сессии без полного завершения процесса
    await app.stop()  # Останавливаем текущую сессию
    python = sys.executable
    os.execl(python, python, *sys.argv)  # Перезапуск с сохранением состояния сессии

# Запуск
app.run()
