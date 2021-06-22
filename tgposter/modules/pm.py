from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton 
from tgposter import dispatcher
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, run_async, CallbackQueryHandler

start_string = "Just a simple hidden atm bot! made by @DontKnowWhoRU, check help!!"
help_string = "Just set the channel where to store by `/setchannel <channel id>` and then whenever someone use #post on something it will get forwarded to the channel which was set, and then the buttons can be used to mark something as post which would give a notification to the user who used the #post and then delete the post itself from the storage channel, and an alternative button to reject the post\n\n If there are some bugs that u find, just leave a msg to @DontKnowWhoRU (Try to give everything in one message)"

def start(update: Update, context: CallbackContext):
  global start_string
  bot = context.bot
  chat = update.effective_chat
  msg = update.effective_message
  user = update.effective_user
  if chat.type == "private":
    markup = InlineKeyboardMarkup[InlineKeyboardButton(text="Help?", callback_data = "help_me")]
    msg.reply_text(start_string, reply_markup = markup, parse_mode = ParseMode.MARKDOWN)
    text = f"#START\n[{user.first_name}](tg://user?id={user.id}) started the bot!"
    m = bot.send_message(chat_id = -1001423499801, text = text, parse_mode = ParseMode.MARKDOWN)
  else:
    msg.reply_text("Yes Im doin' my job sar!!!")


def helpcall(update: Update, context: CallbackContext):
  query = update.callback_query
  msg = update.effective_message
  msg.edit_text(text=help_string, parse_mode=ParseMode.MARKDOWN)
  context.bot.answer_callback_query(query.id)
  
  
START_HANDLER = CommandHandler("start", start, run_async=True)
HELP_CALLBACK = CallbackQueryHandler(helpcall, pattern=r'help_me', run_async=True)
dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(HELP_CALLBACK)