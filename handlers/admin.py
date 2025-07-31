
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal, User, Car
from keyboards import get_admin_inline_keyboard
from config import ADMIN_ID

async def admin_panel(update, context):
    # Проверка что пользователь - настоящий админ
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав администратора.")
        return
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "🛠️ Админ панель",
            reply_markup=get_admin_inline_keyboard()
        )
    else:
        await update.message.reply_text(
            "🛠️ Админ панель",
