import telebot
from Config import token
from logic import get_cheapest_by_taste, get_most_expensive_by_taste, get_cheese_pairings

bot = telebot.TeleBot(token)
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот для поиска ваших вкусных сыров.\n"
        "Вот команды:\n"
        "/cheapest — самый дешёвый сыр в каждой категории, категория это вкусный, не вкусный и средний.\n"
        "/most_expensive — самый дорогой сыр в каждой категории, категория это вкусный, не вкусный и средний.\n"
        "/pairings — узнать, с чем сочетаются разные сыры."
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Вот мои команды: /cheapest, /most_expensive, /pairings.")

@bot.message_handler(commands=['cheapest'])
def get_cheapest(message):
    cheeses = get_cheapest_by_taste()

    if cheeses:
        response = "Самый дешёвый сыр в каждой категории:\n\n"
        for taste, cheese, price in cheeses:
            response += f"Вкус: {taste}\nСыр: {cheese} — {price:.2f} руб/кг\n\n"
    else:
        response = "Такого сыра нету, печалька."

    bot.reply_to(message, response)

@bot.message_handler(commands=['most_expensive'])
def get_most_expensive(message):
    cheeses = get_most_expensive_by_taste()

    if cheeses:
        response = "Самый дорогой сыр в каждой категории:\n\n"
        for taste, cheese, price in cheeses:
            response += f"Вкус: {taste}\nСыр: {cheese} — {price:.2f} руб/кг\n\n"
    else:
        response = "Такого сыра нету, печалька."

    bot.reply_to(message, response)

@bot.message_handler(commands=['pairings'])
def get_pairings(message):
    pairings = get_cheese_pairings()

    if pairings:
        response = "Сочетания сыров с другими продуктами:\n\n"
        current_cheese = None
        for cheese, paired_with, description in pairings:
            if cheese != current_cheese:
                if current_cheese is not None:
                    response += "\n"
                response += f"**{cheese}**:\n"
                current_cheese = cheese
            response += f"• {paired_with}: {description}\n"
    else:
        response = "печалька."

    bot.reply_to(message, response)

if __name__ == "__main__":
    print("Бот запущен")
    bot.polling(none_stop=True)
