from telegram import Update
from telegram.ext import ContextTypes

async def chat(update, context):
    await update.message.reply_text("💬 Чат водителей (в разработке)")
