from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.auth import start, handle_contact

from config import BOT_TOKEN

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
