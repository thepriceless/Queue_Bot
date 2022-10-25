from Bot import bot
import Bot


def Send_Message(chat, text_eng, text_rus, parsemode=None):  # shell for bot.send_message() because of multilingual
    english = Bot.GetUserLang(chat)
    if english is False:
        if parsemode is None:
            bot.send_message(chat, text_rus)
        else:
            bot.send_message(chat, text_rus, parse_mode=parsemode, disable_web_page_preview=True)
    else:
        if parsemode is None:
            bot.send_message(chat, text_eng)
        else:
            bot.send_message(chat, text_eng, parse_mode=parsemode, disable_web_page_preview=True)


# buttons[0] are english, buttons[1] are russian; callbacks are the same
# shell for bot.send_message() [with reply buttons] because of multilingual
def Send_Buttoned_Message(chat, text_eng, text_rus, buttons, callbacks=None, parsemode=None):
    if callbacks is None:
        callbacks = []

    english = Bot.GetUserLang(chat)
    if english is False:  # russian invariant
        if callbacks:
            inline_markup_rus = Bot.types.InlineKeyboardMarkup(row_width=2)
            left_rus = Bot.types.InlineKeyboardButton(buttons[1][0], callback_data=callbacks[0])
            right_rus = Bot.types.InlineKeyboardButton(buttons[1][1], callback_data=callbacks[1])
            inline_markup_rus.add(left_rus, right_rus)
            if parsemode is None:
                bot.send_message(chat, text_rus, reply_markup=inline_markup_rus)
            else:
                bot.send_message(chat, text_rus, reply_markup=inline_markup_rus, parse_mode=parsemode)
        else:
            reply_keyboard_markup_rus = Bot.types.ReplyKeyboardMarkup(resize_keyboard=True)

            # probably can be done better
            if len(buttons[1]) == 6:
                button1 = Bot.types.KeyboardButton(buttons[1][0])
                button2 = Bot.types.KeyboardButton(buttons[1][1])
                button3 = Bot.types.KeyboardButton(buttons[1][2])
                button4 = Bot.types.KeyboardButton(buttons[1][3])
                button5 = Bot.types.KeyboardButton(buttons[1][4])
                button6 = Bot.types.KeyboardButton(buttons[1][5])
                reply_keyboard_markup_rus.add(button1, button2, button3, button4, button5, button6)

            elif len(buttons[1]) == 4:
                button1 = Bot.types.KeyboardButton(buttons[1][0])
                button2 = Bot.types.KeyboardButton(buttons[1][1])
                button3 = Bot.types.KeyboardButton(buttons[1][2])
                button4 = Bot.types.KeyboardButton(buttons[1][3])
                reply_keyboard_markup_rus.add(button1, button2, button3, button4)

            elif len(buttons[1]) == 2:
                button1 = Bot.types.KeyboardButton(buttons[1][0])
                button2 = Bot.types.KeyboardButton(buttons[1][1])
                reply_keyboard_markup_rus.add(button1, button2)

            if parsemode is None:
                bot.send_message(chat, text_rus, reply_markup=reply_keyboard_markup_rus)
            else:
                bot.send_message(chat, text_rus, reply_markup=reply_keyboard_markup_rus, parse_mode=parsemode)

    else:  # english invariant
        if callbacks:
            inline_markup_eng = Bot.types.InlineKeyboardMarkup(row_width=2)
            left_eng = Bot.types.InlineKeyboardButton(buttons[0][0], callback_data=callbacks[0])
            right_eng = Bot.types.InlineKeyboardButton(buttons[0][1], callback_data=callbacks[1])
            inline_markup_eng.add(left_eng, right_eng)
            if parsemode is None:
                bot.send_message(chat, text_eng, reply_markup=inline_markup_eng)
            else:
                bot.send_message(chat, text_eng, reply_markup=inline_markup_eng, parse_mode=parsemode)
        else:
            reply_keyboard_markup_eng = Bot.types.ReplyKeyboardMarkup(resize_keyboard=True)

            # probably can be done better
            if len(buttons[0]) == 6:
                button1 = Bot.types.KeyboardButton(buttons[0][0])
                button2 = Bot.types.KeyboardButton(buttons[0][1])
                button3 = Bot.types.KeyboardButton(buttons[0][2])
                button4 = Bot.types.KeyboardButton(buttons[0][3])
                button5 = Bot.types.KeyboardButton(buttons[0][4])
                button6 = Bot.types.KeyboardButton(buttons[0][5])
                reply_keyboard_markup_eng.add(button1, button2, button3, button4, button5, button6)

            elif len(buttons[0]) == 4:
                button1 = Bot.types.KeyboardButton(buttons[0][0])
                button2 = Bot.types.KeyboardButton(buttons[0][1])
                button3 = Bot.types.KeyboardButton(buttons[0][2])
                button4 = Bot.types.KeyboardButton(buttons[0][3])
                reply_keyboard_markup_eng.add(button1, button2, button3, button4)

            elif len(buttons[0]) == 2:
                button1 = Bot.types.KeyboardButton(buttons[0][0])
                button2 = Bot.types.KeyboardButton(buttons[0][1])
                reply_keyboard_markup_eng.add(button1, button2)

            if parsemode is None:
                bot.send_message(chat, text_eng, reply_markup=reply_keyboard_markup_eng)
            else:
                bot.send_message(chat, text_eng, reply_markup=reply_keyboard_markup_eng, parse_mode=parsemode)


@bot.message_handler(commands=['Start', 'start', 'Lang', 'lang', 'Switch', 'switch'])
def Start(message):
    if not Bot.IfExists(message.chat.id):  # if language is not chosen yet (real start)
        Bot.SetUserLang(message.chat.id, True)

        language_markup = Bot.types.InlineKeyboardMarkup(row_width=2)
        ENG = Bot.types.InlineKeyboardButton("🇬🇧 ENG 🇬🇧", callback_data='ENG')
        RUS = Bot.types.InlineKeyboardButton("🇷🇺 RUS 🇷🇺", callback_data='RUS')
        language_markup.add(ENG, RUS)

        bot.send_message(message.chat.id, "🇬🇧 Hi 🥰! I'm the bot, who tracks the queue!\n"
                                          "First of all, choose the language you want to use (🇬🇧 by default)\n"
                                          "I will type you using chosen language\n"
                                          "If you see this message not the first time, probably, I've been updated! 🖥\n"
                                          "If you want to switch 🇬🇧 to 🇷🇺, use /lang\n\n"
                                          "🇷🇺 Привет 🥰! Я бот, который отслеживает очередь!\n"
                                          "Для начала выбери язык, который ты хочешь использовать (по умолчанию 🇬🇧)\n"
                                          "Я буду писать тебе на выбранном языке\n"
                                          "Если ты видишь это сообщение не впервые, то, вероятно, я обновился! 🖥\n"
                                          "Если ты хочешь поменять язык с 🇬🇧 на 🇷🇺, используй /lang\n\n")

    elif Bot.GetUserLang(message.chat.id) is True:  # eng or rus
        Bot.SetUserLang(message.chat.id, False)
        Send_Message(message.chat.id, "error", "Ты успешно сменил язык на 🇷🇺")

    else:  # rus to eng
        Bot.SetUserLang(message.chat.id, True)
        Send_Message(message.chat.id, "You have successfully changed the language to 🇬🇧", "error")

    buttons = [["Get in", "Get out", "Show queue", "Skip one person", "Go back", "Help"],
               ["Встать в очередь", "Выйти из очереди", "Показать очередь", "Пропустить одного человека",
                "Уйти в конец", "Помощь - я овощ"]]

    Send_Buttoned_Message(message.chat.id, "Nice to meet you! 🙂\nUse /help to see the full list of commands...",
                          "Приятно познакомиться! 🙂\nИспользуй /help, чтобы увидеть полный список команд", buttons)


@bot.message_handler(commands=['Help', 'help'])
def Help(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    Send_Message(message.chat.id, "Here's a list of my commands\:\n"
                                  "/add \- stand into the end of the queue\n"
                                  "/remove \- remove yourself from the queue\n/show \- show current queue\n"
                                  "/swap \- skip one person from behind to stay in front of you\n"
                                  "/skipAll \- skip everyone and get to the end of the queue\n"
                                  "\nControl🤪me\n\n"
                                  "_Admin commands_\:\n"
                                  "/kick \- kick person from the queue\n"
                                  "/restart \- restart \(clear\) the queue\n\n"
                                  "_Сменить язык_\: /lang или /switch",
                                  "Вот список моих команд\:\n"
                                  "/add \- встать в очередь\n"
                                  "/remove \- выйти из очереди\n/show \- показать актуальную очередь\n"
                                  "/swap \- пропустить одного человека вперёд себя\n"
                                  "/skipAll \- уйти в конец очереди, находясь в ней\n"
                                  "\nВластвуй🤪мной\n\n"
                                  "_Команды админа_\:\n"
                                  "/kick \- кикнуть человека из очередь\n"
                                  "/restart \- перезапустить \(почистить\) очередь\n\n"
                                  "_Change language_\: /lang or /switch", 'MarkdownV2')


@bot.message_handler(commands=['Add', 'add'])
def Add(message):
    place = Bot.AddUser(message.from_user.first_name, message.from_user.username, message.chat.id)
    if place[1]:
        Send_Message(message.chat.id, f"You've been added to the queue.\n<b>Your place is {place[0]}</b>",
                                      f"Ты добавлен в очередь.\n<b>Твоё место в очереди - {place[0]}</b>", 'html')
    else:
        Send_Message(message.chat.id, f"Oops, you're already in queue.\n<b>Your place is {place[0]}</b>\n"
                                      f"Use /skipAll to get to the end of the queue\n"
                                      f"Use /swap to to swap with the person behind",
                                      f"Ой, а ты уже в очереди.\n<b>Твоё место в очереди - {place[0]}</b>\n"
                                      f"Используй /skipAll, чтобы оказаться в конце очереди\n"
                                      f"Используй /swap, чтобы пропустить одного человека вперёд себя", 'html')
    Show(message)


@bot.message_handler(commands=['Show', 'show'])
def Show(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    Send_Message(message.chat.id, Bot.FormList(True), Bot.FormList(False), 'MarkdownV2')


@bot.message_handler(commands=['Remove', 'remove'])
def Remove(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    place = Bot.RemoveUser(message.from_user.first_name, message.from_user.username)
    if place[1]:
        Send_Message(message.chat.id, "You've been removed from the queue.\nYour story is finished.",
                                      "Ты вышел из очереди.\nТвоя история окончена.")
        Bot.ShowUpdates(place[0] - 1, min(3, Bot.GetLength()))
        if place[0] == 1:
            Bot.CallFirst()
    else:
        Send_Message(message.chat.id, "Oops, you're not in the queue yet",
                                      "Ой, а ты ещё не в очереди")


@bot.message_handler(commands=['skipAll', 'skipall', 'SkipAll'])
def SkipAll(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    buttons = [["Skip", "Don't skip"], ["Пропустить всех", "Не пропускать"]]
    callbacks = ["skipall", "dontskip"]

    Send_Buttoned_Message(message.chat.id, "Do you really wanna skip everyone?",
                                           "Ты действительно хочешь всех пропустить?", buttons, callbacks)


@bot.message_handler(commands=['Swap', 'swap'])
def Swap(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    place = Bot.SwapBehind(message.from_user.first_name, message.from_user.username)
    if place[1]:
        Send_Message(Bot.GetChatId(place[0]), f"<b>Attention!</b>\nYour classmate decided to swap places with you "
                                              f"and now you're one step closer to the head of the queue.\n"
                                              f"<b>Now your place is {place[0]}</b>",
                                              f"<b>Внимание!</b>\nТвой одногруппник решил пропустить тебя "
                                              f"вперёд себя, и теперь ты на один шаг ближе к началу очереди.\n"
                                              f"<b>Теперь твоё место в очереди - {place[0]}</b>", 'html')
        Send_Message(Bot.GetChatId(place[0] + 1), f"You successfully swapped with the person from behind.\n"
                                                  f"<b>Now your place is {place[0] + 1}</b>",
                                                  f"Ты успешно поменялся местами с человеком позади тебя.\n"
                                                  f"<b>Теперь твоё место в очереди - {place[0] + 1}</b>", 'html')
        Bot.ShowUpdates(place[0] - 1, place[0] + 1)
    else:
        if place[0] == 0:
            Send_Message(message.chat.id, f"Oops, you're not in the queue yet. You can't swap places.\n"
                                          f"Use /Add to stand in",
                                          f"Ой, а ты ещё не в очереди. Ты не можешь поменяться местами.\n"
                                          f"Используй /add, чтобы встать в очередь")
        else:
            Send_Message(message.chat.id, f"Oops, you're the last in the queue <b>(your place is {place[0]})</b>.\n"
                                          f"There's nobody behind, you can't swap places",
                                          f"Ой, а ты последний в очереди <b>(твоё место в очереди - {place[0]})</b>.\n"
                                          f"Позади никого нет, ты не можешь поменяться местами", 'html')


@bot.message_handler(commands=['Restart', 'restart'])
def RestartTry(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    Bot.RestartTumbler()
    if message.from_user.username != "Fedorucho":
        Send_Message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...",
                                      "Требуются права админа, чтобы выполнить это действие.\n"
                                      "Пожалуйста, введи специальный код...")
    else:
        Bot.RestartQueue()
        Send_Message(message.chat.id, "The queue is successfully restarted",
                                      "Очередь успешно перезапущена")


@bot.message_handler(commands=['Kick', 'kick'])
def ChangeKickVar(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    if message.from_user.username != "Fedorucho":
        Bot.KickTryTumbler()
        Send_Message(message.chat.id, "You need admin roots to do this action.\nPlease, enter the special code...",
                                      "Требуются права админа, чтобы выполнить это действие.\n"
                                      "Пожалуйста, введи специальный код...")
    else:
        Bot.RealKickTumbler()
        Send_Message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                                      "Oк\, введи _место_ человека, которого ты хочешь кикнуть\.\.\.", 'MarkdownV2')


@bot.message_handler(content_types=['text'])
def Special(message):
    if not Bot.IfExists(message.chat.id):
        Start(message)

    if Bot.restart_try:
        if message.text == str(Bot.CODE):
            Bot.RestartQueue()
            Send_Message(message.chat.id, "The queue is successfully restarted",
                                          "Очередь успешно перезапущена")
        else:
            Send_Message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                          "try the command again",
                                          "Неверный специальный код.\nЕсли ты уверен, что ты админ, "
                                          "попробуй команду ещё раз")

    elif Bot.kick_try:
        if message.text == str(Bot.CODE):
            Send_Message(message.chat.id, "Ok\, enter the _position_ of the person you want to kick\.\.\.",
                                          "Oк\, введи _место_ человека, которого ты хочешь кикнуть\.\.\.", 'MarkdownV2')
            Bot.RealKickTumbler()
        else:
            Send_Message(message.chat.id, "The code is incorrect.\nIf you believe you're an admin, "
                                          "try the command again",
                                          "Неверный специальный код.\nЕсли ты уверен, что ты админ, "
                                          "попробуй команду ещё раз")
        Bot.KickTryTumbler()

    elif Bot.real_kick:
        kick_num = message.json['text']
        if not kick_num.isdigit():
            Send_Message(message.chat.id, "The number is expected, not letters or spaces",
                                          "Можно ввести только цифры, а не буквы или пробелы")
        else:
            kick_name = Bot.SuggestUserForKick(int(kick_num))

            if kick_name != "":
                buttons = [["Kick", "Don't kick"], ["Кикнуть", "Не кикать"]]
                callbacks = ["kick", "dontkick"]

                Send_Buttoned_Message(message.chat.id, f"Do you really want to kick {kick_name} from the "
                                                       f"{kick_num}th position?",
                                                       f"Ты действительно хочешь кикнуть {kick_name} с "
                                                       f"позиции №{kick_num}?", buttons, callbacks)
            else:
                Send_Message(message.chat.id, f"There's nobody with number {kick_num} in the queue.\n"
                                              f"No one has been kicked",
                                              f"В очереди нет человека с номером {kick_num}.\n"
                                              f"Никто не был исключён")
        Bot.RealKickTumbler()

    else:
        if (message.text.lower() == "start") or (message.text.lower() == "старт"):
            Start(message)
        elif (message.text.lower() == "get in") or (message.text.lower() == "встать в очередь"):
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
        elif (message.text.lower() == "теорвер"):
            Send_Message(message.chat.id, "Points:\n20 - exam\n10 - attendance\n10 - work during lessons\n"
                                          "60 or 80 - control tasks\n20 or 0 - tests in ЦДО\n"
                                          "additional points for olympiad tasks",
                                          "Баллы:\n20 - экзамен\n10 - посещение\n10 - работа на паре\n"
                                          "60 или 80 - контрольные\n20 или 0 - тесты в ЦДО\n"
                                          "доп баллы за конкурсные задачи")
        else:
            Send_Message(message.chat.id, "Sorry, I can't understand you. Please, use suggested commands.\n"
                                          "Go /Help to see the full list of commands",
                                          "Прости, я тебя не понимаю. Пожалуйста, используй предложенные команды.\n"
                                          "Нажми /Help, чтобы увидеть полный список команд")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:

            # kick or not
            if call.data == 'kick':
                kicked = Bot.KickUser(Bot.to_kick)
                Send_Message(kicked[0], "You've been kicked from the queue by the admin due to the bad behaviour.\n"
                                        "YOUR STORY IS FINISHED!",
                                        "Админ исключил тебя из очереди за плохое поведение.\n"
                                        "ТВОЯ ИСТОРИЯ ОКОНЧЕНА!")
                Send_Message(call.message.chat.id, f"{kicked[1]} has been kicked.", f"{kicked[1]} был исключён.")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            elif call.data == 'dontkick':
                Send_Message(call.message.chat.id, "No problem, nothing changed",
                                                   "Без проблем, ничего не изменилось")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            # skip or not
            if call.data == 'skipall':
                place = Bot.TrySkip(call.message.chat.first_name, call.message.chat.username, call.message.chat.id)
                if place[0] != 0:
                    Send_Message(call.message.chat.id, f"You've skipped everyone and got into the end of the queue.\n"
                                                       f"<b>Now your place is {place[0]}</b>",
                                                       f"Ты пропустил всех в очереди и встал в её конец.\n"
                                                       f"<b>Теперь твоё место в очереди - {place[0]}</b>", 'html')
                    Bot.ShowUpdates(place[1] - 1, min(3, Bot.GetLength()))
                    if place[1] == 1:
                        Bot.CallFirst()
                else:
                    Send_Message(call.message.chat.id, "Oops, you're not in the queue yet.\n"
                                                       "Use /add to stand in",
                                                       "Ой, а ты ещё не в очереди.\n"
                                                       "Используй /add, чтобы встать в очередь")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')
            elif call.data == 'dontskip':
                Send_Message(call.message.chat.id, "No problem, nothing changed",
                                                   "Без проблем, ничего не изменилось")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            # choosing language
            if call.data == 'ENG':
                Bot.SetUserLang(call.message.chat.id, True)
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')

            elif call.data == 'RUS':
                Bot.SetUserLang(call.message.chat.id, False)
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup='')
    except:
        pass


bot.polling(none_stop=True)
