import threading

from tgposter.sql import BASE, SESSION
from sqlalchemy import Column, String, distinct, func


class GroupLogs(BASE):
    __tablename__ = "log_channels"
    chat_id = Column(String(14), primary_key=True)
    log_channel = Column(String(14), nullable=False)

    def __init__(self, chat_id, log_channel):
        self.chat_id = str(chat_id)
        self.log_channel = str(log_channel)


GroupLogs.__table__.create(checkfirst=True)

LOGS_INSERTION_LOCK = threading.RLock()

CHANNELS = {}

def is_on(chat_id):
  try: 
    res = SESSION.query(GroupLogs).get(str(chat_id))
    if res: 
      return True
    else: 
      return False
  finally: 
    SESSION.close()
  
  
def set_poster(chat_id, log_channel):
    with LOGS_INSERTION_LOCK:
        res = SESSION.query(GroupLogs).get(str(chat_id))
        if res:
            res.log_channel = log_channel
        else:
            res = GroupLogs(chat_id, log_channel)
            SESSION.add(res)
        SESSION.commit()


def channel(chat_id):
    try: 
      res = SESSION.query(GroupLogs).get(str(chat_id))
      log_channel = res.log_channel
      return log_channel
    finally: 
      SESSION.close()


def stop_chat_logging(chat_id):
    with LOGS_INSERTION_LOCK:
        res = SESSION.query(GroupLogs).get(str(chat_id))
        if res:
            log_channel = res.log_channel
            SESSION.delete(res)
            SESSION.commit()
            return log_channel


def num_logchannels():
    try:
        return SESSION.query(func.count(distinct(GroupLogs.chat_id))).scalar()
    finally:
        SESSION.close()
