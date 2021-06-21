import os 
from telegram import Updater

TOKEN = os.environ.get('BOT_TOKEN')
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
