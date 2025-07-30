from telegram import Update
from telegram.ext import ContextTypes

async def report(update, context):
    await update.message.reply_text("📊 Отчёт смен (в разработке)")
