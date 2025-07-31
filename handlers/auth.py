from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, User
from states import WAITING_PHONE
from keyboards import get_driver_menu, get_admin_menu, get_phone_button

async def start(update: Update, context):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
    db.close()

    if user:
        # Проверяем является ли пользователь настоящим админом
        from config import ADMIN_ID
        is_admin = (update.effective_user.id == ADMIN_ID)
        
        await update.message.reply_text(
            f"Добро пожаловать, {user.name}!",
            reply_markup=get_admin_menu() if is_admin else get_driver_menu()
        )
        context.user_data.clear()
