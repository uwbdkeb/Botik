
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal, User, Car
from keyboards import get_admin_inline_keyboard
from config import ADMIN_ID

async def admin_panel(update, context):
    # Проверка что пользователь - настоящий админ
    if update.effective_user.id != ADMIN_ID:
        if update.callback_query:
            await update.callback_query.answer("❌ У вас нет прав администратора.")
        else:
            await update.message.reply_text("❌ У вас нет прав администратора.")
        return
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        
        if query.data == "manage_drivers":
            await show_drivers_management(update, context)
        elif query.data == "manage_cars":
            await show_cars_management(update, context)
        elif query.data == "admin_stats":
            await show_admin_stats(update, context)
        elif query.data == "add_driver":
            await add_driver_start(update, context)
        elif query.data == "add_car":
            await add_car_start(update, context)
        elif query.data == "back_to_admin":
            await query.edit_message_text(
                "🛠️ Админ панель",
                reply_markup=get_admin_inline_keyboard()
            )
        else:
            # Возвращаемся к главной админ панели если неизвестная команда
            await query.edit_message_text(
                "🛠️ Админ панель",
                reply_markup=get_admin_inline_keyboard()
            )
    else:
        await update.message.reply_text(
            "🛠️ Админ панель",
            reply_markup=get_admin_inline_keyboard()
        )

async def show_drivers_management(update, context):
    db = SessionLocal()
    drivers = db.query(User).filter(User.role == "driver").all()
    db.close()
    
    keyboard = [
        [InlineKeyboardButton("➕ Добавить водителя", callback_data="add_driver")]
    ]
    
    if drivers:
        keyboard.append([InlineKeyboardButton("📋 Список водителей", callback_data="list_drivers")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_admin")])
    
    text = f"👥 Управление водителями\n\nВсего водителей: {len(drivers)}"
    
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_cars_management(update, context):
    db = SessionLocal()
    cars = db.query(Car).all()
    db.close()
    
    keyboard = [
        [InlineKeyboardButton("➕ Добавить машину", callback_data="add_car")]
    ]
    
    if cars:
        keyboard.append([InlineKeyboardButton("🚗 Список машин", callback_data="list_cars")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_admin")])
    
    text = f"🚗 Управление машинами\n\nВсего машин: {len(cars)}"
    
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_admin_stats(update, context):
    db = SessionLocal()
    drivers_count = db.query(User).filter(User.role == "driver").count()
    cars_count = db.query(Car).count()
    db.close()
    
    text = f"📊 Статистика\n\n👥 Водителей: {drivers_count}\n🚗 Машин: {cars_count}"
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_admin")]]
    
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def add_driver_start(update, context):
    context.user_data["admin_action"] = "adding_driver"
    context.user_data["driver_data"] = {}
    
    await update.callback_query.edit_message_text(
        "👤 Добавление нового водителя\n\nВведите имя водителя:"
    )

async def add_car_start(update, context):
    context.user_data["admin_action"] = "adding_car"
    context.user_data["car_data"] = {}
    
    await update.callback_query.edit_message_text(
        "🚗 Добавление новой машины\n\nВведите номер машины:"
    )
