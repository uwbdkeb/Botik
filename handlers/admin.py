from telegram import Update
from telegram.ext import ContextTypes

async def admin_panel(update, context):
    await update.message.reply_text("🛠️ Админка (в разработке)")
