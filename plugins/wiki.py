import asyncio
from pyrogram import Client, filters
import wikipedia
import time
import requests
from pyrogram.types import InputMediaPhoto

def register(app: Client):
    @app.on_message(filters.command("wiki", prefixes=".") & filters.me)
    async def wiki(_, msg):
        try:
            # Получаем запрос из сообщения
            if len(msg.text.split(" ", 1)) < 2:
                await msg.reply("Ошибка: Пожалуйста, укажите запрос после команды .wiki. Пример: .wiki Python")
                return
            
            query = msg.text.split(".wiki ", maxsplit=1)[1].strip()
            
            # Устанавливаем язык для Wikipedia
            wikipedia.set_lang("ru")

            # Получаем краткое содержание страницы и изображение
            result = wikipedia.summary(query)

            # Получаем страницу и пытаемся извлечь первое изображение
            page = wikipedia.page(query)
            image_url = None

            # Попытка извлечь первое изображение (если оно есть)
            if page.images:
                image_url = page.images[0]  # Обычно первое изображение — это подходящее для статьи

            # Добавляем ссылку на статью в конце текста
            result += f"\n\n[Ссылка на статью]({page.url})"

            # Проверяем, что результат не слишком длинный
            if len(result) > 4096:
                # Разбиваем текст на части, если он превышает лимит Telegram
                parts = [result[i:i + 4096] for i in range(0, len(result), 4096)]
                for part in parts:
                    await msg.reply(part)
            else:
                # Если картинка есть, отправляем ее вместе с текстом
                if image_url:
                    # Проверяем, если изображение доступно для загрузки
                    try:
                        # Пробуем скачать изображение, чтобы убедиться, что оно существует и доступно
                        response = requests.get(image_url, stream=True)
                        if response.status_code == 200:
                            # Если изображение скачалось успешно, отправляем его
                            await msg.reply_text(result, quote=True)
                            await msg.reply_photo(image_url)
                        else:
                            # Если изображение не доступно, отправляем только текст
                            await msg.reply(result, quote=True)
                    except Exception as e:
                        print(f"Ошибка при скачивании изображения: {e}")
                        await msg.reply(result, quote=True)
                else:
                    # Если картинки нет, просто отправляем текст
                    await msg.reply(result, quote=True)

        except wikipedia.exceptions.DisambiguationError as e:
            # Если запрос неоднозначный, выводим варианты
            options = "\n".join(e.options)
            await msg.reply(f"Уточните запрос, возможно вы имели в виду:\n{options}", quote=True)

        except wikipedia.exceptions.PageError:
            # Если страница не найдена
            await msg.reply(f"Запрос '{query}' не найден на Википедии.", quote=True)

        except Exception as e:
            # Логирование и вывод ошибок
            error_message = f"[{time.strftime('%d-%m-%Y %H:%M:%S')}]> ❌ При работе KnUser произошла ошибка: {e}"
            print(error_message)
            await msg.reply(f"❌ Произошла ошибка: {str(e)}", quote=True)
