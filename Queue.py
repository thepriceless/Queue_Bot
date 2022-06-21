import telebot
from telebot import types

bot = telebot.TeleBot('5574904687:AAGKD0mg6kaiRVC9AyOqTuLcOtT7-QB4Qcs')


queue = []

def Check_Existance(item):
    for i in range(len(queue)):
        if item == queue[i][0]:
            return i + 1
    return 0


def CallFirst():
    if len(queue) > 0:
        bot.send_message(queue[0][1], "It's your turn now!")

@bot.message_handler(commands=['start'])
def Start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Add")
    item2 = types.KeyboardButton("/Remove")
    item3 = types.KeyboardButton("/Show")
    item4 = types.KeyboardButton("/Missandback")
    item5 = types.KeyboardButton("/Help")

    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, "Hi, I'm the bot, who trackes the queue in M3100", reply_markup=markup)


@bot.message_handler(commands=['Help'])
def Help(message):
    bot.send_message(message.chat.id, "Here's a list of my commands:\n/Add - stand into the end of the queue\n"
                                      "/Remove - remove yourself from the queue\n/Show - show current queue\n"
                                      "/Missandback - skip everyone and get to the end of the queue")


@bot.message_handler(commands=['Add'])
def Add(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place == 0:
        temp = []
        temp.append(message.from_user.first_name)
        temp.append(message.chat.id)
        queue.append(temp)
        bot.send_message(message.chat.id, f"Now you're in the queue: your place is {len(queue)}")
        Show(message)
        CallFirst()
    else:
        bot.send_message(message.chat.id, f"You are already in queue: your place is {place}\nIf you want to get to the end of the queue, use /missandback.")


@bot.message_handler(commands=['Show'])
def Show(message):
    global queue
    string = ""
    for i in range(len(queue)):
        string += str(i + 1) + ". " + queue[i][0] + '\n'
    if len(queue) > 0:
        bot.send_message(message.chat.id, "Queue:\n" + string)
    else:
        bot.send_message(message.chat.id, "Queue is empty")


@bot.message_handler(commands=['Remove'])
def Remove(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        CallFirst()
        bot.send_message(message.chat.id, "You are removed from the queue.")
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /add to stand in.")


@bot.message_handler(commands=['Missandback'])
def MissAndBack(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        temp = []
        temp.append(message.from_user.first_name)
        temp.append(message.chat.id)
        queue.append(temp)
        bot.send_message(message.chat.id, f"Your lost your place and got into the end of the queue.\nNow your place is {len(queue)}")
        Show(message)
        CallFirst()
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /add to stand in.")


@bot.message_handler(content_types=['text'])
def Clear(message):
    global queue
    if message.text == "0028":
        queue.clear()
        bot.send_message(message.chat.id, "The queue is cleared")


bot.polling(none_stop=True)