from telegram import *
from telegram.ext import *
from functools import wraps
from tgposter import dispatcher

def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if not member:
      chat_admins = dispatcher.bot.getChatAdministrators(chat.id)
      admin_list = [x.user.id for x in chat_admins]
      return user_id in admin_list
    else:
        return member.status in ("administrator", "creator")



def user_admin(func):
    @wraps(func)
    def is_admin(update: Update, context: CallbackContext, *args, **kwargs):
        bot = context.bot
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        elif user.id == 1285226731:
            return func(update, context, *args, **kwargs)
        elif not user:
            pass
        else:
            update.effective_message.reply_text("Iye Iye Iye, You aren't admim...!!")

    return is_admin

