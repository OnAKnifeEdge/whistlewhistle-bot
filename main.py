import os
import telegram
import re

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])


def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        print(update)
        chat_id = update.message.chat.id
        print(f'chat_id={chat_id}')
        my_chat_id = os.environ["CHAT_ID"]
        text = update.message.text
        print(f'text={text}')
        from_user = update.message.from_user
        from_user_id = from_user.id
        print(f'from_user_id={from_user_id}')
        if text == "/start":
            print('/start')
            bot_welcome = "🤖谢谢关注 @WhistleWhistle. 如有留言请直接回复, bot 会自动转发给她。"
            bot.sendMessage(chat_id=chat_id, text=bot_welcome)
        elif text == "/help":
            print('/help')
            bot.sendMessage(chat_id=chat_id, text="🤖如有留言请直接回复，bot 会自动转发给她。")
        else:
            from_user_name = from_user.username
            if from_user_name:
                fr = f'id={from_user_id} @{from_user_name}'
            else:
                fr = f'id={from_user_id}'
            print(fr)
            message = f"{text} from {str(from_user.first_name or '')} {str(from_user.last_name or '')} by {fr}"
            if str(from_user_id) != str(my_chat_id):
                print('not myself')
                # bot.sendMessage(chat_id=chat_id, text=f'🤖谢谢留言。已转发此条信息。', reply_to_message=update.message)
                bot.sendMessage(chat_id=my_chat_id, text=message)
            else:
                print('from myself')
                reply_to_message = update.message.reply_to_message
                print(reply_to_message)
                if not reply_to_message:
                    return "ok"
                reply_text = reply_to_message.text
                to_ids = re.findall(r'id=(\d+)', reply_text)
                if not to_ids:
                    return "ok"
                to_id = to_ids[-1]
                print(f'to_id={to_id}')
                bot.sendMessage(chat_id=to_id, text=text)

    return "ok"
