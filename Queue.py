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


def FormList():
    string = ""
    if len(queue) > 0:
        string += "Queue:\n"
        for i in range(len(queue)):
            string += str(i + 1) + ". " + queue[i][0] + '\n'
    else:
        string += "Queue is empty"
    return string


def ShowUpdates(start_pos, end_pos, add_info = ""):
    string = FormList()
    for i in range(start_pos, end_pos):
        bot.send_message(queue[i][1], add_info + string)


@bot.message_handler(commands=['start'])
def Start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Add")
    item2 = types.KeyboardButton("/Remove")
    item3 = types.KeyboardButton("/Show")
    item4 = types.KeyboardButton("/Swap")
    item5 = types.KeyboardButton("/SkipAll")
    item6 = types.KeyboardButton("/Help")

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, "Hi, I'm the bot, who trackes the queue in M3100!\nUse /Help to see the commands' description", reply_markup=markup)


@bot.message_handler(commands=['Help'])
def Help(message):
    bot.send_message(message.chat.id, "Here's a list of my commands:\n/Add - stand into the end of the queue\n"
                                      "/Remove - remove yourself from the queue\n/Show - show current queue\n"
                                      "/Swap - skip one person from behind to stay in front of you\n"
                                      "/SkipAll - skip everyone and get to the end of the queue")


@bot.message_handler(commands=['Add'])
def Add(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place == 0:
        temp = []
        temp.append(message.from_user.first_name)
        temp.append(message.chat.id)
        queue.append(temp)
        bot.send_message(message.chat.id, f"Now you're in the queue.\n<b>Your place is {len(queue)}</b>", parse_mode='html')
        Show(message)
        CallFirst()
    else:
        bot.send_message(message.chat.id, f"You are already in queue.\n<b>Your place is {place}</b>\nIf you want to get to the end of the queue, use /SkipAll.", parse_mode='html')


@bot.message_handler(commands=['Show'])
def Show(message):
    global queue
    bot.send_message(message.chat.id, FormList())


@bot.message_handler(commands=['Remove'])
def Remove(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        ShowUpdates(place - 1, len(queue), "Someone in front of you removed himself from the queue.\n")
        CallFirst()
        bot.send_message(message.chat.id, "You are removed from the queue.\nYour history is finished.")
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /add to stand in.")


@bot.message_handler(commands=['SkipAll'])
def SkipAll(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        temp = []
        temp.append(message.from_user.first_name)
        temp.append(message.chat.id)
        queue.append(temp)
        bot.send_message(message.chat.id, f"Your lost your place and got into the end of the queue.\n<b>Now your place is {len(queue)}</b>", parse_mode='html')
        ShowUpdates(place - 1, len(queue) - 1, "Someone in front of you has done /SkipAll\n")
        ShowUpdates(len(queue) - 1, len(queue))
        CallFirst()
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /add to stand in.")


@bot.message_handler(commands=['Swap'])
def Swap(message):
    global queue
    place = Check_Existance(message.from_user.first_name)
    if place < len(queue):
        if place != 0:
            queue[place - 1], queue[place] = queue[place], queue[place - 1]
            bot.send_message(queue[place - 1][1], "<b>Attention!</b>\nYour classmate decided to swap places with you and now you're one step closer "
                                                  f"to the head of the queue.\n<b>Now your place is {place}</b>", parse_mode='html')
            bot.send_message(queue[place][1], f"You successfully swapped with the person from behind.\n<b>Now your place is {place + 1}</b>", parse_mode='html')
            ShowUpdates(place - 1, place + 1)
        else:
            bot.send_message(message.chat.id, "You're not in the queue yet. So, you can't swap places.\nUse /add to stand in.")
    else:
        bot.send_message(message.chat.id, f"Oh, you're the last in the queue (your place is {place}). There's nobody behind, you can't swap places.")


@bot.message_handler(content_types=['text'])
def Clear(message):
    global queue
    if message.text == "0028":
        queue.clear()
        bot.send_message(message.chat.id, "Cheat-code has been used.\nThe queue is cleared")


bot.polling(none_stop=True)