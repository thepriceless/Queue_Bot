import os

import telebot
from telebot import types

CODE = os.environ["QM3100_CODE"]
TOKEN = os.environ["QM3100_TOKEN"]

bot = telebot.TeleBot(TOKEN)

reopen_try = False
kick_try = False
real_kick = False
kickn_try = False
real_kickn = False

queue = []


def CheckExistance(item):
    for i in range(len(queue)):
        if item in queue[i][0]:
            return i + 1
    return 0


def CallFirst():
    if len(queue) > 0:
        bot.send_message(queue[0][1], "It's your turn now!")


def FormUser(message):
    temp = []
    full_name = message.from_user.first_name + " https://t.me/" + message.from_user.username
    temp.append(full_name)
    temp.append(message.chat.id)
    return temp


def FormList():
    string = ""
    if len(queue) > 0:
        string += "Queue:\n"
        for i in range(len(queue)):
            string += str(i + 1) + "\. [" + queue[i][0].split()[0] + '](' + queue[i][0].split()[1] + ')\n'
    else:
        string += "Queue is empty"
    return string


def ShowUpdates(start_pos, end_pos, add_info = ""):
    string = FormList()
    for i in range(start_pos, end_pos):
        bot.send_message(queue[i][1], add_info + string, parse_mode='MarkdownV2', disable_web_page_preview=True)


def RestartQueue(chat_id):
    global queue, reopen_try
    queue.clear()
    bot.send_message(chat_id, "The queue is restarted")
    reopen_try = False


def Kick(kick_name, kicker_id):
    global queue, kick_try, real_kick
    place = CheckExistance(kick_name)
    if place != 0:
        bot.send_message(queue[place - 1][1], "You've been kicked from the queue by the admin due to the bad behaviour."
                                              "\nYOUR HISTORY IS FINISHED!")
        queue.pop(place - 1)
        bot.send_message(kicker_id, f"{kick_name} has been kicked.")
        if place <= 3:
            ShowUpdates(place - 1, min(3, len(queue)), "Someone in front of you was kicked from the queue\.\n")
            if place == 1:
                CallFirst()
    else:
        bot.send_message(kicker_id, f"There's no {kick_name} in the queue")
    kick_try, real_kick = False, False


def Kickn(kickn_num, kicker_id):
    global queue, kickn_try, real_kickn
    if (1 <= kickn_num) and (kickn_num <= len(queue)):
        bot.send_message(queue[kickn_num - 1][1], "You've been kicked from the queue by the admin due to the"
                                                  "bad behaviour.\nYOUR HISTORY IS FINISHED!")
        bot.send_message(kicker_id, f"{queue[kickn_num - 1][0].split()[0]} has been kicked.")
        queue.pop(kickn_num - 1)
        if kickn_num <= 3:
            ShowUpdates(kickn_num - 1, min(3, len(queue)), "Someone in front of you was kicked from the queue\.\n")
            if kickn_num == 1:
                CallFirst()
    else:
        bot.send_message(kicker_id, f"There're less than {kickn_num} people in the queue, "
                                    f"the {kickn_num}th can't be kicked")
    kickn_try, real_kickn = False, False





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

    bot.send_message(message.chat.id, "Hi 🥰, I'm the bot, who trackes the queue in M3100!\nUse /Help to see the commands' description", reply_markup=markup)


@bot.message_handler(commands=['Help'])
def Help(message):
    bot.send_message(message.chat.id, "Here's a list of my commands:\n/Add - stand into the end of the queue\n"
                                      "/Remove - remove yourself from the queue\n/Show - show current queue\n"
                                      "/Swap - skip one person from behind to stay in front of you\n"
                                      "/SkipAll - skip everyone and get to the end of the queue")


@bot.message_handler(commands=['Add'])
def Add(message):
    global queue
    place = CheckExistance(message.from_user.first_name)
    if place == 0:
        queue.append(FormUser(message))
        bot.send_message(message.chat.id, f"Now you're in the queue.\n<b>Your place is {len(queue)}</b>", parse_mode='html')
        Show(message)
        # CallFirst()
    else:
        bot.send_message(message.chat.id, f"You are already in queue.\n<b>Your place is {place}</b>\nIf you want to get to the end of the queue, use /SkipAll\n"
                                          f"If you want to swap with the person behind, use /Swap", parse_mode='html')


@bot.message_handler(commands=['Show'])
def Show(message):
    global queue
    bot.send_message(message.chat.id, FormList(), parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['Remove'])
def Remove(message):
    global queue
    place = CheckExistance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        if place <= 3:
            ShowUpdates(place - 1, min(3, len(queue)), "Someone in front of you removed himself from the queue\.\n")
            if place == 1:
                CallFirst()
        bot.send_message(message.chat.id, "You are removed from the queue.\nYour history is finished.")
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /Add to stand in.")


@bot.message_handler(commands=['SkipAll'])
def SkipAll(message):
    global queue
    place = CheckExistance(message.from_user.first_name)
    if place != 0:
        queue.pop(place - 1)
        queue.append(FormUser(message))
        bot.send_message(message.chat.id, f"Your lost your place and got into the end of the queue.\n<b>Now your place is {len(queue)}</b>", parse_mode='html')
        ShowUpdates(place - 1, len(queue) - 1, "Someone in front of you has done /SkipAll\n")
        ShowUpdates(len(queue) - 1, len(queue))
        if place == 1:
            CallFirst()
    else:
        bot.send_message(message.chat.id, "You are already not in the queue.\nUse /Add to stand in.")


@bot.message_handler(commands=['Swap'])
def Swap(message):
    global queue
    place = CheckExistance(message.from_user.first_name)
    if place < len(queue) and place != 0:
        queue[place - 1], queue[place] = queue[place], queue[place - 1]
        bot.send_message(queue[place - 1][1], "<b>Attention!</b>\nYour classmate decided to swap places with you and now you're one step closer "
                                              f"to the head of the queue.\n<b>Now your place is {place}</b>", parse_mode='html')
        bot.send_message(queue[place][1], f"You successfully swapped with the person from behind.\n<b>Now your place is {place + 1}</b>", parse_mode='html')
        ShowUpdates(place - 1, place + 1)
    else:
        if place == 0:
            bot.send_message(message.chat.id, f"Oh, you're not in the queue yet. You can't swap places.\nUse /Add to stand in.")
        else:
            bot.send_message(message.chat.id, f"Oh, you're the last in the queue (your place is {place}). There's nobody behind, you can't swap places.")


@bot.message_handler(commands=['Restart'])
def ChangeReopenVar(message):
    global reopen_try
    reopen_try = True
    if message.from_user.username != "Fedorucho":
        bot.send_message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...")
    else:
        RestartQueue(966254083)


@bot.message_handler(commands=['Kick'])
def ChangeKickVar(message):
    global kick_try, real_kick
    if message.from_user.username != "Fedorucho":
        kick_try = True
        bot.send_message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...")
    else:
        real_kick = True
        bot.send_message(message.chat.id, "Ok, enter the name of the person you want to kick...")


@bot.message_handler(commands=['Kickn'])
def ChangeKicknVar(message):
    global kickn_try, real_kickn
    if message.from_user.username != "Fedorucho":
        kickn_try = True
        bot.send_message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...")
    else:
        real_kickn = True
        bot.send_message(message.chat.id, "Ok, enter the position of the person you want to kick...")


@bot.message_handler(content_types=['text'])
def Special(message):
    global real_kick, kick_try, real_kickn, kickn_try
    if reopen_try:
        if message.text == str(CODE):
            RestartQueue(message.chat.id)
        else:
            bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                              "try the command again")
    if kick_try:
        if message.text == str(CODE):
            bot.send_message(message.chat.id, "Ok, enter the name of the person you want to kick...")
            kick_try = False
            real_kick = True
        else:
            bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                              "try the command again")
    elif real_kick:
        kick_name = message.json['text']
        Kick(kick_name, message.chat.id)
    if kickn_try:
        if message.text == str(CODE):
            bot.send_message(message.chat.id, "Ok, enter the position of the person you want to kick...")
            kickn_try = False
            real_kickn = True
        else:
            bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                              "try the command again")
    elif real_kickn:
        kickn_num = message.json['text']
        Kickn(int(kickn_num), message.chat.id)


bot.polling(none_stop=True)