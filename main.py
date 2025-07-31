from telegram.ext import Application

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    # Добавь обработчики команд здесь
    app.run_polling()

if __name__ == "__main__":
    main()