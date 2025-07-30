from telegram import Update
from telegram.ext import ContextTypes

async def delivery_list(update, context):
    await update.message.reply_text("📦 Список доставки (в разработке)")
