import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait

def register(app):
    @app.on_message(filters.command("type", prefixes=".") & filters.me)
    async def type_command(_, msg):
        orig_text = msg.text.split(".type ", maxsplit=1)[1]
        tbp = ""
        typing_symbol = "▒"

        for character in orig_text:
            try:
                tbp += character
                await msg.edit(tbp + typing_symbol)
                await asyncio.sleep(0.50)

            except FloodWait as e:
                await asyncio.sleep(e.x)

        await msg.edit(orig_text)
