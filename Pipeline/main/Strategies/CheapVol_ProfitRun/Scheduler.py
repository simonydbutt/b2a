from Pipeline.main.Audit.EmailLogs import EmailLogs
from Pipeline.main.Strategies.CheapVol_ProfitRun.RunStrat import RunStrat
from apscheduler.schedulers.blocking import BlockingScheduler
from Pipeline.RunPipelineTests import RunPipelineTests
import logging

"""
    TODO: Run tests before start to make sure everything is running correctly
        - Email results
    TODO: Find delay on Binance kline and adjust accordingly
    TODO: Auto schedule jobs to avoid other
"""

if __name__ == '__main__':

    # Tests and initial run
    RunPipelineTests()
    RunStrat(gran='6h').run()
    EmailLogs()

    # Starting scheduler
    sched = BlockingScheduler()
    sched.add_job(RunStrat(gran='6h', consoleLogLevel=logging.INFO).run, trigger='cron', hour='0, 6, 12, 18', minute='2',
                  coalesce=True, misfire_grace_time=600)
    sched.add_job(EmailLogs, trigger='cron', hour='6, 18', minute='30', coalesce=True, misfire_grace_time=600)
    try:
        print('\nStarting Job Scheduler')
        sched.start()
    except KeyboardInterrupt:
        print('Scheduler stopping')
        sched.shutdown()
        pass
