from apscheduler.schedulers.blocking import BlockingScheduler
from calendarzap import *

receiver_list = [os.environ['adm'], os.environ['User1'],
                 os.environ['User2'], os.environ['User3']]

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=2)
def timed_job():
    for numb in receiver_list:
        check_udpates(numb, 'teste')
 


@scheduler.scheduled_job('cron', hour=16)
def scheduled_job2():
    for numb in receiver_list:
        daily_reminder(numb, 'teste')


scheduler.start()
