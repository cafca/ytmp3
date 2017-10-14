from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from ytmp3 import main

sched = BlockingScheduler()

trigger = CronTrigger(minute='*')
sched.add_job(main, trigger)
sched.start()
