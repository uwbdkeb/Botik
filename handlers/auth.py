from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, User
from states import WAITING_PHONE
from keyboards import get_driver_menu, get_admin_menu

async def start(update: Update, context):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
    db.close()

    if user:
        await update.message.reply_text(
            f"Добро пожаловать, {user.name}!",
            reply_markup=get_admin_menu() if user.role == "admin" else get_driver_menu()
        )
        context.user_data.clear()
    else:
        await update.message.reply_text(
            "Отправьте номер для входа:",
            reply_markup=get_phone_button()
        )
        context.user_data["state"] = WAITING_PHONE

async def handle_contact(update: Update, context):
    if context.user_data.get("state") != WAITING_PHONE:
        return
    phone = update.message.contact.phone_number
    db = SessionLocal()
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        await update.message.reply_text("Вы не зарегистрированы.")
        db.close()
        return
    user.telegram_id = update.effective_user.id
    db.commit()
    db.close()
    await update.message.reply_text("✅ Вход выполнен.")
    context.user_data.clear()
