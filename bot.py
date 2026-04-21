import telebot
from Config import token
from logic import cheese_info, get_cheapest_by_taste, get_most_expensive_by_taste, get_cheese_pairings

bot = telebot.TeleBot(token)
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот для поиска ваших вкусных сыров.\n"
        "Вот команды:\n"
        "/tutorial - используйте сразу после чтения, чтобы понять, о чём этот бот.\n"
        "/cheese_info - узнайте вкус и цену каждого сыра.\n"
        "/cheapest - самый дешёвый сыр в каждой категории (вкусный, средний, невкусный).\n"
        "/most_expensive - самый дорогой сыр в каждой категории.\n"
        "/pairings - узнать, с чем сочетаются разные сыры."
    )

bot.message_handler(commands=['tutorial'])
def send_help(message):
    bot.reply_to(message, "Вот мои команды: Этот бот это бот для поиска сыров, тут вы можете узнать какие сыры вкусный а какие нет, используйте"
    "команду /cheese_info есле хотите узнать вкус и цену сыров, хоть у всех своё мнение но тут я написал что мне нравится"
    "используйте коману /cheapest есле вы хотите узнать какой сыр самый дешёвый в каждой категории"
    "используйте команду /most_expensive есле вы хотите узнать какой сыр самый дорогой из каждой категории"
    "и используйте комнаду /pairings есле хотите узнать с чем сочитаются все данные сыры.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Вот мои команды: /tutorial, /cheese_info, /cheapest, /most_expensive, /pairings.")

@bot.message_handler(commands=['cheese_info'])
def get_taste_info(message):
    cheeses = cheese_info()

    if cheeses:
        response = "🧀 Вкус и цена сыров:\n\n"
        for cheese_name, taste_name, price in cheeses:
            response += f"• <b>{cheese_name}</b>\n  Вкус: {taste_name}\n  Цена: {price:.2f} руб/кг\n\n"
    else:
        response = "Есле ты это видешь оно не должно так быть."

    bot.reply_to(message, response)

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
        response = "Сочетания сыров:\n\n"
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
