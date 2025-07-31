
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal, User, Car
from keyboards import get_admin_inline_keyboard

async def admin_panel(update, context):
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "🛠️ Админ панель",
            reply_markup=get_admin_inline_keyboard()
        )
    else:
        await update.message.reply_text(
            "🛠️ Админ панель",
            reply_markup=get_admin_inline_keyboard()
        )

async def manage_drivers(update, context):
    keyboard = [
        [InlineKeyboardButton("➕ Добавить водителя", callback_data="add_driver")],
        [InlineKeyboardButton("📋 Список водителей", callback_data="list_drivers")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]
    ]
    await update.callback_query.edit_message_text(
        "👥 Управление водителями",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def manage_cars(update, context):
    keyboard = [
        [InlineKeyboardButton("➕ Добавить машину", callback_data="add_car")],
        [InlineKeyboardButton("📋 Список машин", callback_data="list_cars")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]
    ]
    await update.callback_query.edit_message_text(
        "🚗 Управление машинами",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def add_driver(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("➕ Добавление водителя (в разработке)")

async def add_car(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("➕ Добавление машины (в разработке)")

async def list_drivers(update, context):
    db = SessionLocal()
    drivers = db.query(User).filter(User.role == "driver").all()
    db.close()
    
    if not drivers:
        text = "📋 Водители не найдены"
    else:
        text = "📋 Список водителей:\n\n"
        for driver in drivers:
            text += f"👤 {driver.name}\n📞 {driver.phone}\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="manage_drivers")]]
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def list_cars(update, context):
    db = SessionLocal()
    cars = db.query(Car).all()
    db.close()
    
    if not cars:
        text = "📋 Машины не найдены"
    else:
        text = "📋 Список машин:\n\n"
        for car in cars:
            text += f"🚗 {car.brand} {car.model}\n🔢 {car.number}\n⛽ {car.fuel}\n📏 {car.current_mileage} км\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="manage_cars")]]
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_stats(update, context):
    db = SessionLocal()
    drivers_count = db.query(User).filter(User.role == "driver").count()
    cars_count = db.query(Car).count()
    db.close()
    
    text = f"📊 Статистика:\n\n👥 Водителей: {drivers_count}\n🚗 Машин: {cars_count}"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]]
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_admin_text(update, context):
    # Обработка текстовых сообщений в админ-панели
    await update.message.reply_text("Используйте кнопки для навигации по админ-панели.")

