from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton 
from telegram.ext import Filter, CommandHandler, MessageHandler, CallbackContext, run_async, CallbackQueryHandler 
from tgposter.sql import channel_sql as sql
import re
from tgposter.modules import is_admin

@user_admin
def set_channel(update: Update, context: CallbackContext): 
  msg = update.effective_message 
  chat = update.effective_chat 
  user = update.effective_user 
  bot = context.bot 
  arg = msg.text.split(" ", 1)
  if len(arg) < 2:
     markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "How to get channel id?", callback_data = "channel_help")]])
    msg.reply_text("Please include the channel id that you want to use", reply_markup = markup)
    return
  else: 
    channel = arg[1]
    if channel.startswith("-100"):
      pass 
    else: 
      markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "How to get channel id?", callback_data = "channel_help")]])
      msg.reply_text("That channel wont work!!", reply_markup = markup)
      return 
    sql.set_poster(chat.id, channel)
    msg.reply_text("Done!")
    
    
def post(update: Update, context: CallbackContext): 
  msg = update.effective_message 
  chat = update.effective_chat 
  user = update.effective_user 
  if sql.is_on(chat_id): 
    pass
  else: 
    return 
  reply = msg.reply_to_message
  if reply: 
    if reply.photo:
      text = ""
      photo_id = reply.photo.file_id
      channel = sql.channel(chat_id)
      if chat.username: 
        link = f"https://t.me/{chat.username}/{msg.id}"
        text = f"Submitted by: [{user.first_name}](tg://user? id={user.id}) \nMessage: {link}"
      else: 
        text = f"Submitted by: [{user.first_name}](tg://user?id={user.id}"
      markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Accept", callback_data = f"accp_{msg.id}_{chat.id}"), InlineKeyboardButton(text = "Reject", callback_data = "accp_reject")], [InlineKeyboardButton(text = "Posted!", callback_data = f"accp_a_{msg.id}_{chat.id}")]])
      bot.send_photo(chat_id = int(channel), photo = photo_id, reply_markup = markup)
    else:
      msg.reply_text("That is not a photo, to post something else tag an admim!")
      return 
  else: 
    msg.reply_text("Ahh baka! we don't post people's here!, reply to something..")
  
  
  
def accp_call(update: Update, context: CallbackContext): 
  query = update.callback_query
  msg = update.effective_message 
  accept_match = re.match(r"accp_(.*)", query.data)
  reject_match = re.match(r"accp_reject", query.data)
  posted_match = re.match(r"accp_a_(.*)", query.data)
  if accept_match: 
    spl = query.data.split("_", 5)
    msg_id = spl[1]
    chat = spl[2]
    query.answer("Trying to send a notif to user...")
    try:
      bot.send_message(chat_id = int(chat), text = "Your post was accepted!", reply_to_message_id = int(msg_id))
    except Exception: 
      query.answer("Cant find message! Can't notif!")
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Posted!", callback_data = f"accp_a_{msg_id}_{chat}")]])
    msg.edit_reply_markup(markup)
  elif reject_match:
    msg.delete()
    query.answer("Success...")
  elif posted_match: 
    spl = query.data.split("_", 5)
    chat = spl[3]
    msg_id = spl[2]
    query.answer("Trying to send a notif...")
    try: 
      bot.send_message(chat_id = int(chat), text = "Your post was posted!!", reply_to_message_id = int(msg_id))
    except Exception: 
      query.answer("Can't find message! Notif Failed")
    msg.delete()
    query.answer("Done!")

def helpcal(update: Update, context: CallbackContext): 
  query = update.callback_query
  query.answer("First use plus messanger an then go to channel and get the id from the channel profile, after that add '*-100*' before, and that's the channel id!", show_alert = True)
  
  
SET_HANDLER = CommandHandler("setchannel", set_channel) 
POST_HANDLER = MessageHandler(Filters.regex(r'^#post'), post)
CALLBACK = CallbackQueryHandler(accp_call, pattern = r'accp_(.*)')
HELP_BACK = CallbackQueryHandler(helpcal, pattern = "channel_help")

dispatcher.add_handler(SET_HANDLER)
dispatcher.add_handler(CALLBACK)
dispatcher.add_handler(POST_HANDLER)
dispatcher.add_handler(HELP_BACK)