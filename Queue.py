from Bot import bot
import Bot


@bot.message_handler(commands=['start'])
def Start(message):
    markup = Bot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = Bot.types.KeyboardButton("/Add")
    item2 = Bot.types.KeyboardButton("/Remove")
    item3 = Bot.types.KeyboardButton("/Show")
    item4 = Bot.types.KeyboardButton("/Swap")
    item5 = Bot.types.KeyboardButton("/SkipAll")
    item6 = Bot.types.KeyboardButton("/Help")

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, "Hi 🥰, I'm the bot, who tracks the queue in M3100!\n"
                                      "Use /Help to see the commands' description", reply_markup=markup)


@bot.message_handler(commands=['Help'])
def Help(message):
    bot.send_message(message.chat.id, "Here's a list of my commands:\n/Add - stand into the end of the queue\n"
                                      "/Remove - remove yourself from the queue\n/Show - show current queue\n"
                                      "/Swap - skip one person from behind to stay in front of you\n"
                                      "/SkipAll - skip everyone and get to the end of the queue")


@bot.message_handler(commands=['Add'])
def Add(message):
    place = Bot.AddUser(message.from_user.first_name, message.from_user.username, message.chat.id)
    if place[1]:
        bot.send_message(message.chat.id, f"You've been added to the queue.\n"
                                          f"<b>Your place is {place[0]}</b>", parse_mode='html')
    else:
        bot.send_message(message.chat.id, f"Oops, you're already in queue.\n"
                                          f"<b>Your place is {place[0]}</b>\n"
                                          f"Use /SkipAll to get to the end of the queue\n"
                                          f"Use /Swap to to swap with the person behind", parse_mode='html')
    Show(message)


@bot.message_handler(commands=['Show'])
def Show(message):
    bot.send_message(message.chat.id, Bot.FormList(), parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['Remove'])
def Remove(message):
    place = Bot.RemoveUser(message.from_user.first_name, message.from_user.username)
    if place[1]:
        bot.send_message(message.chat.id, "You've been removed from the queue.\nYour history is finished.")
        Bot.ShowUpdates(place[0] - 1, min(3, Bot.GetLength()))
        if place[0] == 1:
            Bot.CallFirst()
    else:
        bot.send_message(message.chat.id, "Oops, you're already not in the queue")


@bot.message_handler(commands=['SkipAll'])
def SkipAll(message):

    markup = Bot.types.InlineKeyboardMarkup(row_width=2)
    item1 = Bot.types.InlineKeyboardButton("Skip!", callback_data='skipall')
    item2 = Bot.types.InlineKeyboardButton("Don't skip", callback_data='dont skip')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Do you really wanna skip everyone?", reply_markup=markup)


@bot.message_handler(commands=['Swap'])
def Swap(message):
    place = Bot.SwapBehind(message.from_user.first_name, message.from_user.username)
    if place[1]:
        bot.send_message(Bot.GetChatId(place[0]), f"<b>Attention!</b>\nYour classmate decided to swap places with you "
                                                  f"and now you're one step closer to the head of the queue.\n"
                                                  f"<b>Now your place is {place[0]}</b>", parse_mode='html')
        bot.send_message(Bot.GetChatId(place[0] + 1), f"You successfully swapped with the person from behind.\n"
                                                   f"<b>Now your place is {place[0] + 1}</b>", parse_mode='html')
        Bot.ShowUpdates(place[0] - 1, place[0] + 1)
    else:
        if place[0] == 0:
            bot.send_message(message.chat.id, f"Oops, you're not in the queue yet. You can't swap places.\n"
                                              f"Use /Add to stand in")
        else:
            bot.send_message(message.chat.id, f"Oops, you're the last in the queue <b>(your place is {place[0]})</b>. "
                                              f"There's nobody behind, you can't swap places", parse_mode='html')


@bot.message_handler(commands=['Restart', 'restart'])
def RestartTry(message):
    Bot.RestartTumbler()
    if message.from_user.username != "Fedorucho":
        bot.send_message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...")
    else:
        Bot.RestartQueue()


@bot.message_handler(commands=['Kick', 'kick'])
def ChangeKickVar(message):
    if message.from_user.username != "Fedorucho":
        Bot.KickTryTumbler()
        bot.send_message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...")
    else:
        Bot.RealKickTumbler()
        bot.send_message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                         parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def Special(message):
    if Bot.restart_try:
        if message.text == str(Bot.CODE):
            Bot.RestartQueue()
            bot.send_message(message.chat.id, "The queue is successfully restarted")
        else:
            bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                              "try the command again")

    if Bot.kick_try:
        if message.text == str(Bot.CODE):
            bot.send_message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                             parse_mode='MarkdownV2')
            Bot.RealKickTumbler()
        else:
            bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                              "try the command again")
        Bot.KickTryTumbler()

    elif Bot.real_kick:
        kick_num = message.json['text']
        kick_name = Bot.SuggestUserForKick(int(kick_num))

        if kick_name != "":
            markup = Bot.types.InlineKeyboardMarkup(row_width=2)
            item1 = Bot.types.InlineKeyboardButton("Kick!", callback_data='kick')
            item2 = Bot.types.InlineKeyboardButton("Don't kick", callback_data='dont kick')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, f"Do you really want to kick {kick_name} from the "
                                              f"{kick_num}th position?", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"There's nobody with number {kick_num} in the queue.\n"
                                              f"No one has been kicked")
        Bot.RealKickTumbler()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'kick':
                kicked = Bot.KickUser(Bot.to_kick)
                bot.send_message(kicked[0], "You've been kicked from the queue by the admin "
                                            "due to the bad behaviour.\nYOUR HISTORY IS FINISHED!")
                bot.send_message(call.message.chat.id, f"{kicked[1]} has been kicked.")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            elif call.data == 'dont kick':
                bot.send_message(call.message.chat.id, 'No problem, nothing changed')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')

            if call.data == 'skipall':
                print(call.message.chat.first_name, call.message.chat.username, call.message.chat.id)
                place = Bot.TrySkip(call.message.chat.first_name, call.message.chat.username, call.message.chat.id)
                print(place)
                if place[0] != 0:
                    bot.send_message(call.message.chat.id, f"You've skipped everyone and got into the end of the queue."
                                                           f"\n<b>Now your place is {place[0]}</b>", parse_mode='html')
                    Bot.ShowUpdates(place[1] - 1, min(3, Bot.GetLength()))
                    if place[1] == 1:
                        Bot.CallFirst()
                else:
                    bot.send_message(call.message.chat.id, "Oops, you're not in the queue yet.\nUse /Add to stand in")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')
            elif call.data == 'dont skip':
                bot.send_message(call.message.chat.id, "No problem, nothing changed")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

    except:
        pass


bot.polling(none_stop=True)
