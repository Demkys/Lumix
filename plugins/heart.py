import random
import asyncio
from pyrogram import filters

def register(app):
    # Списки эмодзи для облаков и сердец
    clouds = [
        "\u2601\ufe0f", "\u2744\ufe0f", "\ud83c\udf27\ufe0f", "\ud83c\udf28\ufe0f", "\ud83c\udf2b\ufe0f", "\ud83c\udf2c\ufe0f", "\ud83c\udf24\ufe0f", "\ud83c\udf26\ufe0f", "\ud83c\udf25\ufe0f", "\u2728",
        "\ud83c\udf2a\ufe0f", "\ud83c\udf29\ufe0f", "\ud83d\udca8", "\ud83c\udf00", "\u2614", "\ud83c\udf2a", "\ud83c\udf2c"
    ]

    hearts = [
        "\u2764\ufe0f", "\ud83d\udc96", "\ud83d\udc98", "\ud83d\udc9d", "\ud83d\udc93", "\ud83d\udc97", "\ud83d\udc8c", "\ud83d\udc99", "\ud83d\udc9a", "\ud83d\udc9b",
        "\ud83d\udc9c", "\ud83e\udde1", "\ud83e\udeb5", "\ud83e\udeb6", "\ud83d\udc95", "\ud83d\udc9e", "\ud83d\udc9f", "\ud83d\udc8b", "\ud83d\udc9d", "\u2764\ufe0f\u200d\ud83d\udd25", "\ud83d\udc33"
    ]

    # Функция генерации сердца из эмодзи
    def generate_heart(cloud_emoji, heart_emoji):
        heart = [
            f"{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}",
            f"{cloud_emoji}{cloud_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}{cloud_emoji}",
            f"{cloud_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}",
            f"{cloud_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}",
            f"{cloud_emoji}{cloud_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}{cloud_emoji}",
            f"{cloud_emoji}{cloud_emoji}{cloud_emoji}{heart_emoji}{heart_emoji}{heart_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}",
            f"{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{heart_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}",
            f"{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}{cloud_emoji}"
        ]
        return "\n".join(heart)

    # Обработчик команды .heart
    @app.on_message(filters.command("heart", prefixes=".") & filters.me)
    async def heart(_, msg):
        for _ in range(15):  # Количество смен эмодзи
            cloud_emoji = random.choice(clouds)
            heart_emoji = random.choice(hearts)
            
            heart = generate_heart(cloud_emoji, heart_emoji)
            await msg.edit(heart)

            # Задержка перед следующим обновлением
            await asyncio.sleep(1.5)
