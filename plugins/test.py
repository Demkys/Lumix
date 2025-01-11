from pyrogram import filters

def register(app):
    @app.on_message(filters.command("bot", prefixes=".") & filters.me)
    async def bot_reply(_, msg):
        await msg.reply("Lumix функционирует нормально.")
