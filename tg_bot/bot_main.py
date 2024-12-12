from telebot import TeleBot, types
from datetime import datetime
import random
import string

# Конфигурация
TOKEN = ""

# Создание бота
bot = TeleBot(TOKEN)

print("Бот запущен")


def generate_daily_password():
    random.seed(datetime.now().strftime('%Y-%m-%d'))
    return ''.join(random.choices("0123456789", k=6))


@bot.message_handler(commands=['getpass_pr'])
def send_password(message):
    daily_password = generate_daily_password()
    bot.reply_to(message, f"Так так так, пароль на сегодня:\n\n ```{daily_password}```", parse_mode="Markdown")


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
