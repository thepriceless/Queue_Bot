from Bot import bot
import Bot


@bot.message_handler(commands=['Start', 'start'])
def Start(message):
    # english keyboard buttons
    buttons_markup_eng = Bot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_in_eng = Bot.types.KeyboardButton("Get in")
    get_out_eng = Bot.types.KeyboardButton("Get out")
    show_eng = Bot.types.KeyboardButton("Show queue")
    swap_eng = Bot.types.KeyboardButton("Skip one person")
    skipall_eng = Bot.types.KeyboardButton("Go back")
    help_eng = Bot.types.KeyboardButton("Help")
    buttons_markup_eng.add(get_in_eng, get_out_eng, show_eng, swap_eng, skipall_eng, help_eng)

    # russian keyboard buttons
    buttons_markup_rus = Bot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_in_rus = Bot.types.KeyboardButton("Встать в очередь")
    get_out_rus = Bot.types.KeyboardButton("Выйти из очереди")
    show_rus = Bot.types.KeyboardButton("Показать очередь")
    swap_rus = Bot.types.KeyboardButton("Пропустить одного человека")
    skipall_rus = Bot.types.KeyboardButton("Уйти в конец")
    help_rus = Bot.types.KeyboardButton("Помощь - я овощ")
    buttons_markup_rus.add(get_in_rus, get_out_rus, show_rus, swap_rus, skipall_rus, help_rus)

    language_markup = Bot.types.InlineKeyboardMarkup(row_width=2)
    ENG = Bot.types.InlineKeyboardButton("🇬🇧 ENG 🇬🇧", callback_data='ENG')
    RUS = Bot.types.InlineKeyboardButton("🇷🇺 RUS 🇷🇺", callback_data='RUS')
    language_markup.add(ENG, RUS)

    bot.send_message(message.chat.id, "🇬🇧 Hi 🥰! I'm the bot, who tracks the queue!\n"
                                      "First of all, choose the language you want to use...\n"
                                      "I will type you using chosen language\n\n"
                                      "🇷🇺 Привет 🥰! Я бот, который отслеживает очередь!\n"
                                      "Для начала выбери язык, который ты хочешь использовать...\n"
                                      "Я буду писать тебе на выбранном языке", reply_markup=language_markup)
    while Bot.English is None:
        pass

    if Bot.English:
        bot.send_message(message.chat.id, "Okay, nice to meet you! 🙂", reply_markup=buttons_markup_eng)
    else:
        bot.send_message(message.chat.id, "Хорошо, приятно познакомиться! 🙂", reply_markup=buttons_markup_rus)

    Help(message)


@bot.message_handler(commands=['Lang', 'lang'])
def SetLang(message):
    Bot.LanguageTumbler()
    if Bot.English:
        bot.send_message(message.chat.id, "🇬🇧Now you are from England🇬🇧!")
    else:
        bot.send_message(message.chat.id, "🇷🇺Now you are from Russia🇷🇺!")


@bot.message_handler(commands=['Help', 'help'])
def Help(message):
    if Bot.English:
        bot.send_message(message.chat.id, "Here's a list of my commands:\n/add - stand into the end of the queue\n"
                                          "/remove - remove yourself from the queue\n/show - show current queue\n"
                                          "/swap - skip one person from behind to stay in front of you\n"
                                          "/skipAll - skip everyone and get to the end of the queue\n"
                                          "\nControl🤪me")
    else:
        bot.send_message(message.chat.id, "Вот список моих команд:\n/add - встать в очередь\n"
                                          "/remove - выйти из очереди\n/show - показать актуальную очередь\n"
                                          "/swap - пропустить одного человека вперёд себя\n"
                                          "/skipAll - уйти в конец очереди, находясь в ней\n"
                                          "\nControl🤪me")


@bot.message_handler(commands=['Add', 'add'])
def Add(message):
    place = Bot.AddUser(message.from_user.first_name, message.from_user.username, message.chat.id)
    if place[1]:
        if Bot.English:
            bot.send_message(message.chat.id, f"You've been added to the queue.\n"
                                              f"<b>Your place is {place[0]}</b>", parse_mode='html')
        else:
            bot.send_message(message.chat.id, f"Ты добавлен в очередь.\n"
                                              f"<b>Твоё место в очереди - {place[0]}</b>", parse_mode='html')
    else:
        if Bot.English:
            bot.send_message(message.chat.id, f"Oops, you're already in queue.\n"
                                              f"<b>Your place is {place[0]}</b>\n"
                                              f"Use /skipAll to get to the end of the queue\n"
                                              f"Use /swap to swap with the person behind", parse_mode='html')
        else:
            bot.send_message(message.chat.id, f"Ой, а ты уже в очереди.\n"
                                              f"<b>Твоё место в очереди - {place[0]}</b>\n"
                                              f"Используй /skipAll чтобы оказаться в конце очереди\n"
                                              f"Используй /swap чтобы пропустить одного человека вперёд себя",
                             parse_mode='html')
    Show(message)


@bot.message_handler(commands=['Show', 'show'])
def Show(message):
    bot.send_message(message.chat.id, Bot.FormList(), parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['Remove', 'remove'])
def Remove(message):
    place = Bot.RemoveUser(message.from_user.first_name, message.from_user.username)
    if place[1]:
        if Bot.English:
            bot.send_message(message.chat.id, "You've been removed from the queue.\nYour history is finished.")
        else:
            bot.send_message(message.chat.id, "Ты вышел из очереди.\nТвоя история окончена.")
        Bot.ShowUpdates(place[0] - 1, min(3, Bot.GetLength()))
        if place[0] == 1:
            Bot.CallFirst()
    else:
        if Bot.English:
            bot.send_message(message.chat.id, "Oops, you're already not in the queue")
        else:
            bot.send_message(message.chat.id, "Ой, а ты ещё не в очереди")


@bot.message_handler(commands=['SkipAll', 'skipall'])
def SkipAll(message):

    markup_eng = Bot.types.InlineKeyboardMarkup(row_width=2)
    skip_eng = Bot.types.InlineKeyboardButton("Skip", callback_data='skipall')
    dontskip_eng = Bot.types.InlineKeyboardButton("Don't skip", callback_data='dont skip')
    markup_eng.add(skip_eng, dontskip_eng)

    markup_rus = Bot.types.InlineKeyboardMarkup(row_width=2)
    skip_rus = Bot.types.InlineKeyboardButton("Пропустить", callback_data='skipall')
    dontskip_rus = Bot.types.InlineKeyboardButton("Не пропускать", callback_data='dont skip')
    markup_rus.add(skip_rus, dontskip_rus)

    if Bot.English:
        bot.send_message(message.chat.id, "Do you really wanna skip everyone?", reply_markup=markup_eng)
    else:
        bot.send_message(message.chat.id, "Ты действительно хочешь всех пропустить?", reply_markup=markup_rus)


@bot.message_handler(commands=['Swap', 'swap'])
def Swap(message):
    place = Bot.SwapBehind(message.from_user.first_name, message.from_user.username)
    if place[1]:
        if Bot.English:
            bot.send_message(Bot.GetChatId(place[0]), f"<b>Attention!</b>\nYour classmate decided to swap places with "
                                                      f"you and now you're one step closer to the head of the queue.\n"
                                                      f"<b>Now your place is {place[0]}</b>", parse_mode='html')
            bot.send_message(Bot.GetChatId(place[0] + 1), f"You successfully swapped with the person from behind.\n"
                                                          f"<b>Now your place is {place[0] + 1}</b>", parse_mode='html')
        else:
            bot.send_message(Bot.GetChatId(place[0]), f"<b>Внимание!</b>\nТвой одногруппник решил пропустить тебя "
                                                      f"вперёд себя, и теперь ты на один шаг ближе к началу очереди.\n"
                                                      f"<b>Теперь твоё место в очереди - {place[0]}</b>",
                             parse_mode='html')
            bot.send_message(Bot.GetChatId(place[0] + 1), f"Ты успешно поменялся местами с человеком позади тебя.\n"
                                                          f"<b>Теперь твоё место в очереди - {place[0] + 1}</b>",
                             parse_mode='html')
        Bot.ShowUpdates(place[0] - 1, place[0] + 1)
    else:
        if Bot.English:
            if place[0] == 0:
                bot.send_message(message.chat.id, f"Oops, you're not in the queue yet. You can't swap places.\n"
                                                  f"Use /add to stand in")
            else:
                bot.send_message(message.chat.id, f"Oops, you're the last in the queue <b>(your place is "
                                                  f"{place[0]})</b>. There's nobody behind, you can't swap places",
                                 parse_mode='html')
        else:
            if place[0] == 0:
                bot.send_message(message.chat.id, f"Ой, а ты ещё не в очереди. Ты не можешь поменяться местами.\n"
                                                  f"Используй /add, чтобы встать в очередь")
            else:
                bot.send_message(message.chat.id, f"Ой, а ты последний в очереди <b>(твоё место в очереди - "
                                                  f"{place[0]})</b>. Позади никого нет, ты не можешь поменяться "
                                                  f"местами", parse_mode='html')


@bot.message_handler(commands=['Restart', 'restart'])
def RestartTry(message):
    Bot.RestartTumbler()
    if message.from_user.username != "Fedorucho":
        if Bot.English:
            bot.send_message(message.chat.id, "You need admin roots to do this action.\n"
                                              "Please, enter the special code...")
        else:
            bot.send_message(message.chat.id, "Требуются права админа, чтобы выполнить это действие.\n"
                                              "Пожалуйста, введи специальный код...")
    else:
        Bot.RestartQueue()
        if Bot.English:
            bot.send_message(message.chat.id, "The queue is successfully restarted")
        else:
            bot.send_message(message.chat.id, "Очередь успешно перезапущена")


@bot.message_handler(commands=['Kick', 'kick'])
def ChangeKickVar(message):
    if message.from_user.username != "Fedorucho":
        Bot.KickTryTumbler()
        if Bot.English:
            bot.send_message(message.chat.id, "You need admin roots to do this action.\n"
                                              "Please, enter the special code...")
        else:
            bot.send_message(message.chat.id, "Требуются права админа, чтобы выполнить это действие.\n"
                                              "Пожалуйста, введи специальный код...")
    else:
        Bot.RealKickTumbler()
        if Bot.English:
            bot.send_message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                             parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, "Oк\, введи _место_ человека, которого ты хочешь кикнуть\.\.\.",
                             parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def Special(message):
    if Bot.restart_try:
        if message.text == str(Bot.CODE):
            Bot.RestartQueue()
            if Bot.English:
                bot.send_message(message.chat.id, "The queue is successfully restarted")
            else:
                bot.send_message(message.chat.id, "Очередь успешно перезапущена")
        else:
            if Bot.English:
                bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                                  "try the command again")
            else:
                bot.send_message(message.chat.id, "Неверный специальный код.\nЕсли ты уверен, что ты админ, "
                                                  "попробуй команду ещё раз")

    elif Bot.kick_try:
        if message.text == str(Bot.CODE):
            if Bot.English:
                bot.send_message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                                 parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, "Oк\, введи _место_ человека, которого ты хочешь кикнуть\.\.\.",
                                 parse_mode='MarkdownV2')
            Bot.RealKickTumbler()
        else:
            if Bot.English:
                bot.send_message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                                  "try the command again")
            else:
                bot.send_message(message.chat.id, "Неверный специальный код.\nЕсли ты уверен, что ты админ, "
                                                  "попробуй команду ещё раз")
        Bot.KickTryTumbler()

    elif Bot.real_kick:
        kick_num = message.json['text']
        if not kick_num.isdigit():
            if Bot.English:
                bot.send_message(message.chat.id, "The number is expected, not letters or spaces")
            else:
                bot.send_message(message.chat.id, "Можно ввести только цифры, а не буквы или пробелы")
        else:
            kick_name = Bot.SuggestUserForKick(int(kick_num))

            if kick_name != "":
                if Bot.English:
                    # english keyboard
                    markup_eng = Bot.types.InlineKeyboardMarkup(row_width=2)
                    kick_eng = Bot.types.InlineKeyboardButton("Kick", callback_data='kick')
                    dontkick_eng = Bot.types.InlineKeyboardButton("Don't kick", callback_data='dont kick')
                    markup_eng.add(kick_eng, dontkick_eng)

                    bot.send_message(message.chat.id, f"Do you really want to kick {kick_name} from the "
                                                      f"{kick_num}th position?", reply_markup=markup_eng)
                else:
                    # russian keyboard
                    markup_rus = Bot.types.InlineKeyboardMarkup(row_width=2)
                    kick_rus = Bot.types.InlineKeyboardButton("Кикнуть", callback_data='kick')
                    dontkick_rus = Bot.types.InlineKeyboardButton("Не кикать", callback_data='dont kick')
                    markup_rus.add(kick_rus, dontkick_rus)

                    bot.send_message(message.chat.id, f"Ты действительно хочешь кикнуть {kick_name} с "
                                                      f"позиции №{kick_num}?", reply_markup=markup_rus)
            else:
                if Bot.English:
                    bot.send_message(message.chat.id, f"There's nobody with number {kick_num} in the queue.\n"
                                                      f"No one has been kicked")
                else:
                    bot.send_message(message.chat.id, f"В очереди нет человека с номером {kick_num}.\n"
                                                      f"Никто не был кикнут")
        Bot.RealKickTumbler()

    else:
        if (message.text.lower() == "get in") or (message.text.lower() == "встать в очередь"):
            Add(message)
        elif (message.text.lower() == "show queue") or (message.text.lower() == "показать очередь"):
            Show(message)
        elif (message.text.lower() == "get out") or (message.text.lower() == "выйти из очереди"):
            Remove(message)
        elif (message.text.lower() == "skip one person") or (message.text.lower() == "пропустить одного человека"):
            Swap(message)
        elif (message.text.lower() == "go back") or (message.text.lower() == "уйти в конец"):
            SkipAll(message)
        elif (message.text.lower() == "help") or (message.text.lower() == "помощь - я овощ"):
            Help(message)
        else:
            bot.send_message(message.chat.id, "Sorry, I can't understand you. Please, use suggested commands.\n"
                                          "Go /Help to see the full list of commands")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:

            # kick or not
            if call.data == 'kick':
                kicked = Bot.KickUser(Bot.to_kick)
                bot.send_message(kicked[0], "You've been kicked from the queue by the admin "
                                            "due to the bad behaviour.\nYOUR HISTORY IS FINISHED!")
                bot.send_message(call.message.chat.id, f"{kicked[1]} has been kicked.")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            elif call.data == 'dont kick':
                bot.send_message(call.message.chat.id, 'No problem, nothing changed')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                              reply_markup='')

            # skip or not
            if call.data == 'skipall':
                place = Bot.TrySkip(call.message.chat.first_name, call.message.chat.username, call.message.chat.id)
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

            # choosing language
            if call.data == 'ENG':
                Bot.LanguageTumbler("ENG")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            elif call.data == 'RUS':
                Bot.LanguageTumbler("RUS")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

    except:
        pass


bot.polling(none_stop=True)
