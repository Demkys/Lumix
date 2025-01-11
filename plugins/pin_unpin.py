from pyrogram import filters

def register(app):
    @app.on_message(filters.command("pin", prefixes=".") & filters.me)
    async def pin_message(_, msg):
        if msg.reply_to_message:
            await msg.reply_to_message.pin()
            await msg.delete()

    @app.on_message(filters.command("unpin", prefixes=".") & filters.me)
    async def unpin_message(_, msg):
        if msg.reply_to_message:
            await msg.reply_to_message.unpin()
            await msg.delete()
