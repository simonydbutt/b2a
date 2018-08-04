from Pipeline.main.Audit.EmailLogs import EmailLogs
from Pipeline.main.Strategies.CheapVol_ProfitRun.RunStrat import RunStrat
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

"""
    TODO: Find delay on Binance kline and adjust accordingly
    TODO: Auto schedule jobs to avoid others
"""

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(RunStrat(gran='1d', consoleLogLevel=logging.INFO).run, trigger='cron', hour='0', minute='15',
                  coalesce=True, misfire_grace_time=600)
    sched.add_job(RunStrat(gran='6h').run, trigger='cron', hour='0, 6, 12, 18',
                  minute='10', coalesce=True, misfire_grace_time=600)
    sched.add_job(RunStrat(gran='2h').run, trigger='cron', hour='0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22',
                  minute='2', coalesce=True, misfire_grace_time=300)
    sched.add_job(EmailLogs, trigger='cron', hour='0, 6, 12, 18', minute='45', coalesce=True, misfire_grace_time=600)
    try:
        print('Starting Job Scheduler')
        sched.start()
    except KeyboardInterrupt:
        print('Scheduler stopping')
        sched.shutdown()
        pass
