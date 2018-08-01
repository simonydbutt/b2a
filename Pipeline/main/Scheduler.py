from Pipeline.main.Audit.EmailLogs import EmailLogs
from Pipeline.main.Strategies.CheapVol_ProfitRun.RunStrat import RunStrat
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

"""
    TODO: Find delay on Binance kline and adjust accordingly
    TODO: Auto schedule jobs to avoid others
"""

def run24():
    print('Run 24 second job')


def run12():
    print('Run 12 second job')


def run2():
    print('Run 2 second job')


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(RunStrat(gran='1d', consoleLogLevel=logging.INFO).run, trigger='cron', hour='0', minute='30', coalesce=True, misfire_grace_time=600)
    sched.add_job(RunStrat(gran='12h').run, trigger='cron', hour='0, 12', minute='12', coalesce=True, misfire_grace_time=600)
    sched.add_job(RunStrat(gran='6h').run, trigger='cron', hour='0, 6, 12, 18', minute='7', coalesce=True, misfire_grace_time=600)
    sched.add_job(RunStrat(gran='2h').run, trigger='cron', minute='2', coalesce=True, misfire_grace_time=300)
    sched.add_job(EmailLogs, trigger='cron', hour='7, 19', minute='45', coalesce=True, misfire_grace_time=600)

    try:
        print('Starting Job Scheduler')
        sched.start()
    except KeyboardInterrupt:
        print('Scheduler stopping')
        sched.shutdown()
        pass
