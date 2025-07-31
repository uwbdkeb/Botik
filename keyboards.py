from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_phone_button():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )

def get_driver_menu():
    return ReplyKeyboardMarkup(
        [["🚛 Начать смену"], ["📦 Список доставки"], ["🔚 Завершить смену"]],
        resize_keyboard=True
    )

def get_admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["🛠️ Админка"],
            ["👥 Водители", "🚗 Машины"],
            ["📊 Отчёт смен", "💬 Чат водителей"]
        ],
        resize_keyboard=True
    )

def get_car_keyboard(cars):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🚗 {c.number}", callback_data=f"car_{c.id}")] for c in cars
    ])
