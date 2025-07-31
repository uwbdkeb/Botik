
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.auth import start, handle_contact, create_admin
from handlers.driver import start_shift
from handlers.delivery import delivery_list
from handlers.admin import admin_panel
from handlers.chat import chat
from handlers.parking import parking_check
from handlers.report import report

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create_admin", create_admin))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    # Обработчики текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🛠️ Админка"), admin_panel))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🚛 Начать смену"), start_shift))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📦 Список доставки"), delivery_list))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("💬 Чат водителей"), chat))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🅿️ Стоянка"), parking_check))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📊 Отчёт смен"), report))

    # Запуск бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
