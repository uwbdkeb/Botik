from telegram import Update
from telegram.ext import ContextTypes

async def parking_check(update, context):
    await update.message.reply_text("🅿️ Стоянка (в разработке)")
