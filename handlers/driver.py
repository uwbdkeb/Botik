from telegram import Update
from telegram.ext import ContextTypes

async def start_shift(update, context):
    await update.message.reply_text("🚛 Начало смены (в разработке)")
