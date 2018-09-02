from Pipeline.main.Utils.RunPipelineTests import RunPipelineTests
from apscheduler.schedulers.blocking import BlockingScheduler
from Pipeline.main.Utils.EmailUtil import EmailUtil
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.main.Strategy.Close.Exit import Exit
import Settings
import yaml


class Schedule:

    """
        *TODO: create way to run more than one strat at a time
        **TODO: create schedule function from gran to schedule
    """

    def __init__(self, db, strat):
        self.stratPath = 'Pipeline/DB/%s/%s' % (db, strat)
        with open('%s/%s/config.yml' % (Settings.BASE_PATH, self.stratPath)) as configFile:
            self.config = yaml.load(configFile)
        self.logger = AddLogger(stratName=strat, db=db,
                                fileLogLevel=self.config['logging']['file'],
                                consoleLogLevel=self.config['logging']['console']).logger
        self.Enter = Enter(db=db, stratName=strat)
        self.Exit = Exit(db=db, stratName=strat)
        self.RunTests = RunPipelineTests
        self.emailNotifications = EmailUtil(db=self.config['dbName'])

    def run(self):
        # Before starting scheduler
        self.RunTests()
        self.Enter.run()
        self.emailNotifications.statsMessage()

        # Schedule
        sched = BlockingScheduler()
        sched.add_job(self.Enter.run, trigger='cron', hour='0, 6, 12, 18', minute='2',
                      coalesce=True, misfire_grace_time=600)
        sched.add_job(self.Exit.run, trigger='cron', minute='15, 45', coalesce=True, misfire_grace_time=60)
        sched.add_job(self.emailNotifications.statsMessage, trigger='cron', hour='2, 8, 14, 20', minute='30',
                      coalesce=True, misfire_grace_time=1200)
        try:
            print('\nStarting Job Scheduler')
            sched.start()
        except KeyboardInterrupt:
            print('Scheduler Stopping')
            sched.shutdown()
            pass


Schedule(db='sandbox', strat='CheapVol_ProfitRun').run()