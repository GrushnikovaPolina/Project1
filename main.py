import telebot,random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import literary,annotation,year
bot = telebot.TeleBot('7051768277:AAHAiEzkiIdPfhhXyCTHtQynKzxObf-ffgI')
@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id, text='Привет! Я - твой бот написанный на Python. Я готов поделиться с вами информацией о литературных произведениях , а так же сыграть с вами в небольшую игру! Для того чтобы я знал о чем вам рассказать и чем помочь воспользуйтесь командой/help')
@bot.message_handler(commands=['help'])
def start_bot(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Самые популярные произведения в наше время", callback_data='literary'),
                 InlineKeyboardButton("Игра", callback_data='game') )
    keyboard.add(InlineKeyboardButton("Аннотация", callback_data='annotation'),
                 InlineKeyboardButton("Год выпуска", callback_data='year'), )
    bot.send_message(chat_id=message.chat.id, text='Чем я могу Вам помочь?', reply_markup=keyboard)
@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text.__contains__('привет') or message.text.__contains__('Привет!'):
        bot.send_message(message.chat.id, 'Добрый день!))')
    elif message.text.__contains__('Пока'):
        bot.send_message(message.chat.id, 'До свидания!')
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'literary':
        literary_info = ', '.join(literary.keys())
        bot.send_message(chat_id=call.message.chat.id, text="О каком литературном произведении вы хотите узнать " + literary_info +'.')
        bot.register_next_step_handler(call.message, print_info_literary)
    elif call.data == 'annotation':
        annotation_info = ', '.join(annotation.keys())
        bot.send_message(chat_id=call.message.chat.id, text="Произведения о которых я могу рассказать: " + annotation_info +'. Выбери произведение.')
        bot.register_next_step_handler(call.message, print_info_annotation)
    elif call.data == 'year':
        year_info = ', '.join(year.keys())
        bot.send_message(chat_id=call.message.chat.id, text="Я могу рассказать вам о датах опубликования таких произведенй: " + year_info +'.Выберите интересующее вас произведение')
        bot.register_next_step_handler(call.message, print_info_year)
    elif call.data=='game':
       bot.send_message(chat_id=call.message.chat.id, text="Чтобы запустить игру используйте команду /game")

def print_info_literary(message):
    if message.text in literary:
        bot.send_message(chat_id=message.chat.id, text=literary[message.text])
    else:
        bot.send_message(chat_id=message.chat.id, text='Я не знаю данное произведение(')
    start_bot(message)
def print_info_annotation(message):
    if message.text in annotation:
        bot.send_message(chat_id=message.chat.id, text=annotation[message.text])
    else:
        bot.send_message(chat_id=message.chat.id, text='Я не знаю аннотацию данной книги')
    start_bot(message)
def print_info_year(message):
    if message.text in year:
        bot.send_message(chat_id=message.chat.id, text=year[message.text])
    else:
        bot.send_message(chat_id=message.chat.id, text='Я не знаю год опубликации данного произведения')
    start_bot(message)


def init_storage(id):
    pass


def set_data_storage(id, param, attempt):
    pass


@bot.message_handler(func=lambda message: message.text.lower() == "game")
def digitgames(message):
    init_storage(message.chat.id)
    attempt = 10
    set_data_storage(message.chat.id, "attempt", attempt)

    bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')

    random_digit = random.randint(1, 10)
    set_data_storage(message.chat.id, "random_digit", random_digit)

    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)

def process_digit_step(message, get_data_storage=None):
    user_digit = message.text

    if not user_digit.isdigit() or int(user_digit) < 1 or int(user_digit) > 10:
        msg = bot.reply_to(message, 'Вы ввели некорректное число. Введите число от 1 до 10')
        bot.register_next_step_handler(msg, process_digit_step)
        return

    attempt = get_data_storage(message.chat.id)["attempt"]
    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
        init_storage(message.chat.id)
        return

    elif attempt > 1:
        attempt -= 1
        set_data_storage(message.chat.id, "attempt", attempt)
        bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Вы проиграли!')
        init_storage(message.chat.id)
        return

if __name__ == '__main__':
    bot.polling()
