
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.auth import start, handle_contact, create_admin
from handlers.driver import start_shift
from handlers.delivery import delivery_list
from handlers.admin import (admin_panel, manage_drivers, manage_cars,
                            add_driver, add_car, list_drivers, list_cars,
                            admin_stats, handle_admin_text)
from handlers.chat import chat
from handlers.parking import parking_check
from handlers.report import report

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create_admin", create_admin))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(
        MessageHandler(filters.Regex("🚛 Начать смену"), start_shift))
    app.add_handler(
        MessageHandler(filters.Regex("📦 Список доставки"), delivery_list))
    app.add_handler(MessageHandler(filters.Regex("🛠️ Админка"), admin_panel))
    app.add_handler(MessageHandler(filters.Regex("💬 Чат водителей"), chat))
    app.add_handler(MessageHandler(filters.Regex("🅿️ Стоянка"), parking_check))
    app.add_handler(MessageHandler(filters.Regex("📊 Отчёт смен"), report))

    # Обработчики кнопок админ-панели
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="admin_panel"))
    app.add_handler(
        CallbackQueryHandler(manage_drivers, pattern="manage_drivers"))
    app.add_handler(CallbackQueryHandler(manage_cars, pattern="manage_cars"))
    app.add_handler(CallbackQueryHandler(add_driver, pattern="add_driver"))
    app.add_handler(CallbackQueryHandler(add_car, pattern="add_car"))
    app.add_handler(CallbackQueryHandler(list_drivers, pattern="list_drivers"))
    app.add_handler(CallbackQueryHandler(list_cars, pattern="list_cars"))
    app.add_handler(CallbackQueryHandler(admin_stats, pattern="admin_stats"))

    # Обработчик текста для админ-панели
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_text))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
