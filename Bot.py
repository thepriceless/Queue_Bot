import os

import telebot
from telebot import types


CODE = os.environ["QM3100_CODE"]
TOKEN = os.environ["QM3100_TOKEN"]

bot = telebot.TeleBot(TOKEN)

# state variables
restart_try = False
kick_try = False
real_kick = False

to_kick = 0

# language
English = True

queue = []


def GetChatId(place):
    return queue[place - 1][1]


def GetLength():
    return len(queue)


# tumblers

def RestartTumbler():
    global restart_try
    restart_try = not restart_try


def KickTryTumbler():
    global kick_try
    kick_try = not kick_try


def RealKickTumbler():
    global real_kick
    real_kick = not real_kick

# queue operators
def CheckExistance(full_name):
    for i in range(len(queue)):
        if full_name == queue[i][0]:
            return i + 1
    return 0


def CallFirst():
    if len(queue) > 0:
        bot.send_message(queue[0][1], "<b>ATTENTION!</b>\nIt's your turn now!", parse_mode='html')


def FormUser(full_name, chat_id):
    user = []
    user.append(full_name)
    user.append(chat_id)
    return user


def FormList():
    string = "Queue:\n"
    if len(queue) > 0:
        for i in range(len(queue)):
            string += str(i + 1) + "\. [" + queue[i][0].split()[0] + '](' + queue[i][0].split()[1] + ')\n'
    else:
        string = "Queue is empty"
    return string


def ShowUpdates(start_pos, end_pos):
    string = FormList()
    for i in range(start_pos, end_pos):
        bot.send_message(queue[i][1], "The queue has been changed\!\n" + string,
                         parse_mode='MarkdownV2', disable_web_page_preview=True)


def RestartQueue():
    global queue
    queue.clear()
    RestartTumbler()


def SuggestUserForKick(place):
    global queue, to_kick
    if (1 <= place) and (place <= len(queue)):
        to_kick = place
        return queue[place - 1][0].split()[0]
    else:
        return ""


def AddUser(name, username, chat_id):
    global queue
    full_name = name + " https://t.me/" + username
    place = CheckExistance(full_name)
    if place == 0:
        queue.append(FormUser(full_name, chat_id))
        return [len(queue), True]
    else:
        return [place, False]


def RemoveUser(name, username):
    global queue
    full_name = name + " https://t.me/" + username
    place = CheckExistance(full_name)
    if place != 0:
        queue.pop(place - 1)
        return [place, True]
    else:
        return [0, False]


def SwapBehind(name, username):
    global queue
    full_name = name + " https://t.me/" + username
    place = CheckExistance(full_name)
    if (place == 0) or (place == len(queue)):
        return [place, False]
    else:
        queue[place - 1], queue[place] = queue[place], queue[place - 1]
        return [place, True]


def TrySkip(name, username, chat_id):
    place_remove = RemoveUser(name, username)
    if place_remove[1]:
        place_add = AddUser(name, username, chat_id)
        return [place_add[0], place_remove[0]]
    else:
        return [0, 0]


def KickUser(kick_num):
    global queue
    kicked_chat_id = queue[kick_num - 1][1]
    kicked_name = queue[kick_num - 1][0].split()[0]
    queue.pop(kick_num - 1)
    return [kicked_chat_id, kicked_name]
