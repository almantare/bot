# 1409846178:AAHDg0KmVgN1aF9BrF6AO1aVmEXCm-eQzrw
# ^^ telegram token ^^

from qiwi import QiwiChecker

import telebot

from info import info

bot = telebot.TeleBot('1409846178:AAHDg0KmVgN1aF9BrF6AO1aVmEXCm-eQzrw')

users_storage = {}

SUM = 1

BLACK_LIST_OF_TRANSACTION = []

articles_storage = {

    "гайд для windows": "https://telegra.ph/Rukovodstvo-po-ustanovke-i-vklyuchenie-prilozheniya-ANTISCH-na-Windows-10-11-10",

    "гайд для linux": "https://telegra.ph/Rukovodstvo-po-ustanovke-i-vklyucheniyu-ANTISCH-na-OS-Linux-11-11"

}


class Session:
    def __init__(self, ID: int, PAID=False) -> None:
        self.id = ID

        self.paid = PAID


@bot.message_handler(commands=['start'])
def start_message(message):
    kb1 = telebot.types.ReplyKeyboardMarkup(True)
    kb1.row('/buy', '/start', '/guide')

    users_storage[message.chat.id] = Session(message.chat.id)

    bot.send_message(message.chat.id, info, reply_markup=kb1)


@bot.message_handler(commands=['buy'])
def buy_info(message):

    kb2 = telebot.types.ReplyKeyboardMarkup(True)
    kb2.row('/check', '/start')

    text = '''
    Оплата на qiwi кошелёк: {phone}\nСумма к оплате: {sum} руб.\nОбязательный комментарий: {comment}
            '''.format(phone="+79851609109", sum=SUM, comment=message.chat.id)

    bot.send_message(message.chat.id, text, reply_markup=kb2)


@bot.message_handler(commands=['check'])
def check(message):

    kb_if_success = telebot.types.ReplyKeyboardMarkup(True)
    kb_if_success.row('/ubuntu_20', '/ubuntu_18', '/windows', '/debian_10')

    kb_if_fail = telebot.types.ReplyKeyboardMarkup(True)
    kb_if_fail.row('/check', '/buy')

    text = """ \tУСПЕШНО\nВыберите свою OC"""

    CHECK = QiwiChecker(message.chat.id, SUM).check()

    if CHECK.__class__ == tuple:

        if CHECK[1] not in BLACK_LIST_OF_TRANSACTION:

            BLACK_LIST_OF_TRANSACTION.append(CHECK[1])

            users_storage[message.chat.id] = Session(message.chat.id, True)

            bot.send_message(message.chat.id, text, reply_markup=kb_if_success)

        else:
            bot.send_message(message.chat.id, text="Не оплачено")

    else:

        bot.send_message(message.chat.id, "что-то пошло не так...", reply_markup=kb_if_fail)


@bot.message_handler(commands=['guide'])
def send_guide(message):

    for guide, link in articles_storage.items():

        bot.send_message(message.chat.id, "{}\n\n{}".format(guide, link))


@bot.message_handler(commands=['ubuntu_20', 'ubuntu_18', 'debian_10', 'windows'])
def send_product(message):

    try:

        if users_storage[message.chat.id].paid:

            finish_kb = telebot.types.ReplyKeyboardMarkup(True)
            finish_kb.row('/start')

            if "/ubuntu_18" in str(message):

                bot.send_document(message.chat.id,
                                  open("soft_storage//linux//ubuntu18//antiSCH_ubuntu18.04.zip", 'rb'),
                                  reply_markup=finish_kb)

                bot.send_message(message.chat.id, articles_storage["гайд для linux"])

            elif "/ubuntu_20" in str(message):

                bot.send_document(message.chat.id,
                                  open("soft_storage//linux//ubuntu20//antiSCH_ubuntu20.04.zip", 'rb'),
                                  reply_markup=finish_kb)
                # open("soft_storage//linux//ubuntu20//antiSCH_ubuntu20.04.zip")

                bot.send_message(message.chat.id, articles_storage["гайд для linux"])

            elif "/windows" in str(message):

                bot.send_document(message.chat.id, open("soft_storage//windows//antiSCH_windows_kali.zip", 'rb'),
                                  reply_markup=finish_kb)

                bot.send_message(message.chat.id, articles_storage["гайд для windows"])

            elif "/debian_10" in str(message):

                bot.send_document(message.chat.id, open("soft_storage//linux//debian10//antiSCH_debian10.zip", 'rb'),
                                  reply_markup=finish_kb)

                bot.send_message(message.chat.id, articles_storage["гайд для linux"])

            text = "Удачи!"

            del users_storage[message.chat.id]

            print(users_storage[message.chat.id])

            bot.send_message(message.chat.id, text=text,
                             reply_markup=telebot.types.ReplyKeyboardMarkup(True).row('/start'))

        else:

            bot.send_message(message.chat.id, text="Не оплачено!",
                             reply_markup=telebot.types.ReplyKeyboardMarkup(True).row('/buy'))


    except KeyError:

        pass


bot.polling()
