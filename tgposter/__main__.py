import logging
from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton 
from tgposter import updater, dispatcher
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, run_async, CallbackQueryHandler
from tgposter import modules
import time
start_time = time.time()

# Enable logging
logging.basicConfig(
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 

logger = logging.getLogger(__name__)

#error handling

def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update @DontKnowWhoRU\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    if len(message) < 4000:
      m = context.bot.send_message(chat_id= -1001494443405, text=message, parse_mode=ParseMode.HTML)
    else: 
      context.bot.send_message(chat_id =-1001494443405, text = f"@DontKnowWhoRU\n\n`{context.error}\nFull traceback in logs`", parse_mode = ParseMode.MARKDOWN)
    #context.bot.pinChatMessage(-1001494443405, m.message_id)

def grt(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
    
def ping(update: Update, context: CallbackContext): 
  msg = update.effective_message 
  strt = datetime.now()
  m = msg.reply_text("pinging..")
  ed = datetime.now()
  pon = (ed - strt).microseconds / 1000
  n = time.time()
  awk = grt(n - start_time)
  m.edit_text(f"PONG!\nPing Time: {pon} ms\nAwake For: {awk}")


PING = CommandHandler("ping", ping)

dispatcher.add_error_handler(error_handler)
dispatcher.add_handler(PING)

dispatcher.bot.send_message(1285226731, "Im online!!")

logger.info("TelegraphPoster: Started polling....")

updater.start_polling()

updater.idle()