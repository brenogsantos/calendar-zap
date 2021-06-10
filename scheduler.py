from apscheduler.schedulers.blocking import BlockingScheduler
from calendarzap import *

receiver_list = os.environ['adm']

scheduler = BlockingScheduler()


def the_funct():
    for numb in receiver_list:
        #print(f"sending message to {numb}")
        daily_reminder(numb, 'messages')


scheduler.add_job(the_funct, 'cron', minutes=2)
scheduler.start()
