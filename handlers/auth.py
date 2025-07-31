from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, User
from states import WAITING_PHONE
from keyboards import get_driver_menu, get_admin_menu, get_phone_button

async def start(update: Update, context):
    from config import ADMIN_ID
    
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
    
    # Если это админ и его нет в базе - создаем автоматически
    if update.effective_user.id == ADMIN_ID and not user:
        admin_user = User(
            telegram_id=ADMIN_ID,
            phone="admin",
            name=update.effective_user.first_name or "Администратор",
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        user = admin_user
    
    db.close()

    if user:
        # Проверяем является ли пользователь настоящим админом
        is_admin = (update.effective_user.id == ADMIN_ID)
        
        await update.message.reply_text(
            f"Добро пожаловать, {user.name}!",
            reply_markup=get_admin_menu() if is_admin else get_driver_menu()
        )
        context.user_data.clear()
    else:
        await update.message.reply_text(
            "Отправьте номер для входа:",
            reply_markup=get_phone_button()
        )
        context.user_data["state"] = WAITING_PHONErkup=get_phone_button()
        )
        context.user_data["state"] = WAITING_PHONE

async def handle_contact(update: Update, context):
    if context.user_data.get("state") != WAITING_PHONE:
        return
    phone = update.message.contact.phone_number
    db = SessionLocal()
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        await update.message.reply_text("❌ Ваш номер телефона не найден в системе. Обратитесь к администратору для регистрации.")
        db.close()
        return
    user.telegram_id = update.effective_user.id
    db.commit()
    db.close()
    # Проверяем является ли пользователь настоящим админом
    from config import ADMIN_ID
    is_admin = (update.effective_user.id == ADMIN_ID)
    
    await update.message.reply_text(
        f"Добро пожаловать, {user.name}!",
        reply_markup=get_admin_menu() if is_admin else get_driver_menu()
    )
    context.user_data.clear()

async def create_admin(update: Update, context):
    from config import ADMIN_ID
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("У вас нет прав для создания администратора.")
        return

    db = SessionLocal()
    admin_user = User(
        telegram_id=update.effective_user.id,
        phone="admin",
        name=update.effective_user.first_name or "Администратор",
        role="admin"
    )
    db.add(admin_user)
    db.commit()
    db.close()

    await update.message.reply_text(
        "Администратор создан!",
        reply_markup=get_admin_menu()
    )