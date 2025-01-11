import speedtest
from pyrogram import filters

def register(app):
    @app.on_message(filters.command("speedtest", prefixes=".") & filters.me)
    async def speed_test(_, msg):
        await msg.edit("\U0001F3A7 Запускаю тест скорости... \U0001F680")
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            server = st.results.server
            server_name = server.get("name", "Неизвестный сервер")
            server_country = server.get("country", "Неизвестная страна")

            ping = st.results.ping  # Получаем значение пинга
            download_speed = st.download() / 1_000_000  # в Мбит/с
            upload_speed = st.upload() / 1_000_000  # в Мбит/с

            result_message = (
                f"\U0001F3C1 **Результаты теста скорости**:\n"
                f"\U0001F4CD Сервер: {server_name}, {server_country}\n"
                f"\U000023F3 Пинг: `{ping:.2f} мс`\n"
                f"\U00002B07️ Скорость скачивания: `{download_speed:.2f} Мбит/с`\n"
                f"\U00002B06️ Скорость загрузки: `{upload_speed:.2f} Мбит/с`"
            )

            await msg.edit(result_message)
        except Exception as e:
            await msg.edit(f"\u26A0 Произошла ошибка при выполнении теста скорости: {e}")
