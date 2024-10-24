from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, handle_image, choose_size
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    print("Бот запущен...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^(300x250|600x400|1024x768)$'), choose_size))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Запускаем polling для получения сообщений
    application.run_polling()

if __name__ == "__main__":
    main()








