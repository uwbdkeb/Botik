
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal, User, Car
from config import ADMIN_ID

async def handle_admin_text(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    
    admin_action = context.user_data.get("admin_action")
    
    if admin_action == "adding_driver":
        await handle_driver_adding(update, context)
    elif admin_action == "adding_car":
        await handle_car_adding(update, context)

async def handle_driver_adding(update: Update, context):
    driver_data = context.user_data.get("driver_data", {})
    text = update.message.text
    
    if "name" not in driver_data:
        driver_data["name"] = text
        context.user_data["driver_data"] = driver_data
        await update.message.reply_text("📱 Введите номер телефона водителя:")
    
    elif "phone" not in driver_data:
        # Проверяем, что номер не занят
        db = SessionLocal()
        existing_user = db.query(User).filter(User.phone == text).first()
        if existing_user:
            db.close()
            await update.message.reply_text("❌ Этот номер уже зарегистрирован. Введите другой номер:")
            return
        
        driver_data["phone"] = text
        
        # Создаем водителя
        new_driver = User(
            phone=driver_data["phone"],
            name=driver_data["name"],
            role="driver"
        )
        db.add(new_driver)
        db.commit()
        db.close()
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад к управлению", callback_data="manage_drivers")]]
        
        await update.message.reply_text(
            f"✅ Водитель добавлен!\n\n"
            f"👤 Имя: {driver_data['name']}\n"
            f"📱 Телефон: {driver_data['phone']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Очищаем данные
        context.user_data.pop("admin_action", None)
        context.user_data.pop("driver_data", None)

async def handle_car_adding(update: Update, context):
    car_data = context.user_data.get("car_data", {})
    text = update.message.text
    
    if "number" not in car_data:
        # Проверяем, что номер не занят
        db = SessionLocal()
        existing_car = db.query(Car).filter(Car.number == text).first()
        if existing_car:
            db.close()
            await update.message.reply_text("❌ Машина с таким номером уже существует. Введите другой номер:")
            return
        
        car_data["number"] = text
        context.user_data["car_data"] = car_data
        await update.message.reply_text("🏭 Введите марку машины:")
    
    elif "brand" not in car_data:
        car_data["brand"] = text
        context.user_data["car_data"] = car_data
        await update.message.reply_text("🚗 Введите модель машины:")
    
    elif "model" not in car_data:
        car_data["model"] = text
        context.user_data["car_data"] = car_data
        await update.message.reply_text("⛽ Введите тип топлива:")
    
    elif "fuel" not in car_data:
        car_data["fuel"] = text
        context.user_data["car_data"] = car_data
        await update.message.reply_text("📏 Введите текущий пробег:")
    
    elif "current_mileage" not in car_data:
        try:
            mileage = int(text)
            car_data["current_mileage"] = mileage
            
            # Создаем машину
            db = SessionLocal()
            new_car = Car(
                number=car_data["number"],
                brand=car_data["brand"],
                model=car_data["model"],
                fuel=car_data["fuel"],
                current_mileage=car_data["current_mileage"]
            )
            db.add(new_car)
            db.commit()
            db.close()
            
            keyboard = [[InlineKeyboardButton("⬅️ Назад к управлению", callback_data="manage_cars")]]
            
            await update.message.reply_text(
                f"✅ Машина добавлена!\n\n"
                f"🚗 Номер: {car_data['number']}\n"
                f"🏭 Марка: {car_data['brand']}\n"
                f"🚙 Модель: {car_data['model']}\n"
                f"⛽ Топливо: {car_data['fuel']}\n"
                f"📏 Пробег: {car_data['current_mileage']} км",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
            # Очищаем данные
            context.user_data.pop("admin_action", None)
            context.user_data.pop("car_data", None)
            
        except ValueError:
            await update.message.reply_text("❌ Введите корректное число для пробега:")
