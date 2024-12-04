import telebot
import json
import random
TOKEN = "your telegram token"

bot = telebot.TeleBot(TOKEN)
try:
    with open("user_data.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
except FileNotFoundError:
    user_data = {}
@bot.message_handler(commands=["start"])
def handle_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет! Я твой карманный учитель английского языка")

@bot.message_handler(commands=['learn'])
def handle_learn(message):
    words_right = 0
    bot.send_message(message.chat.id, 'Обучение сейчас начнется')
    chat_id = str(message.chat.id)
    try:
        # Извлечение количества слов из команды
        words_number = int(message.text.split()[1])
        all_words = words_number
    except IndexError:
        bot.send_message(chat_id, "Укажите количество слов для изучения")
        return
    except ValueError:
        bot.send_message(chat_id, "кол-во слов должно быть числом")
    if chat_id in user_data and user_data[chat_id]:
        user_dict = user_data[chat_id]
        ask_translation(message.chat.id, user_dict, words_number, words_right, all_words)
    else:
        bot.send_message(chat_id,"Слова для обучения отсутствуют, добавьте их с помощью команды /addword 'слово на английском' 'слово на русском' (нажимать на команду в этом сообщении не требуется)+")
def ask_translation(chat_id, user_words, words_left, words_right, all_words):
    if words_left >0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Запиши перевод слова '{word}'.")
        words_left -=1
        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left, words_right, all_words)
    else:
        bot.send_message(chat_id, f'Правильных слов: {words_right} из {all_words}')
def check_translation(message, translation, words_left, words_right, all_words):
    user_translation = message.text.strip().lower()
    if user_translation == translation.lower():
        words_right += 1
        bot.send_message(message.chat.id, "Перевод правильный!")
    else:
        bot.send_message(message.chat.id, f"Перевод неправильный Правильный перевод {translation}!")
    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left, words_right, all_words)
@bot.message_handler(commands=['addword'])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(str(chat_id), {})
    try:
        words = message.text.split()[1: ]
        if len(words) ==2:
            word, translation = words[0].lower(), words[1].lower()
            user_dict[word] = translation
            user_data[str(chat_id)] = user_dict
            print(user_data)
            with open('user_data.json', 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, "Слово было добавлено в словарь")
        else:
            bot.send_message(chat_id, f"Неправильно введен текст")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Этот бот нужен для изучения английского языка')
    bot.send_message(message.chat.id, 'Команды: help, learn, start, addword')
    bot.send_message(message.chat.id, 'Автор: skoprov')


@bot.message_handler(func=lambda message: True)
def handle_all(message: telebot.types.Message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, 'У меня пока нет имени')
    elif message.text.lower() == 'какую функцию ты выполняешь?':
        bot.send_message(message.chat.id, 'копирую текст пользователя')

if __name__ == '__main__':
    bot.polling(none_stop=True)
