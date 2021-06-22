import os 
from telegram.ext import Updater

TOKEN = os.environ.get('BOT_TOKEN')
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
