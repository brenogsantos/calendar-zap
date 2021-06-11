from apscheduler.schedulers.blocking import BlockingScheduler
from calendarzap import *

receiver_list = [os.environ['adm'], os.environ['User1'],
                 os.environ['User2'], os.environ['User3']]

scheduler = BlockingScheduler()


# def the_funct():
#   for numb in receiver_list:
#print(f"sending message to {numb}")
#      daily_reminder(numb, 'messages')


#scheduler.add_job(the_funct, 'cron', minutes=2)

#@scheduler.scheduled_job('interval', minutes=2)
#def timed_job():
    # for numb in receiver_list:
    #   daily_reminder(numb, 'teste')
 #   pass


@scheduler.scheduled_job('cron', hour=16)
def scheduled_job2():
    for numb in receiver_list:
        daily_reminder(numb, 'teste')


scheduler.start()
