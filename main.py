
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
