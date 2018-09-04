from Pipeline.main.Utils.RunPipelineTests import RunPipelineTests
from apscheduler.schedulers.blocking import BlockingScheduler
from Pipeline.main.Utils.EmailUtil import EmailUtil
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.main.Strategy.Close.Exit import Exit
import numpy as np
import Settings
import yaml


class Schedule:

    """
        *TODO: create way to run more than one strat at a time
        **TODO: create schedule function from gran to schedule
    """

    def __init__(self, db, strat, periodDict):
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
        self.periodDict = self._compDict(periodDict)

    def _compDict(self, periodDict):
        for key in periodDict.keys():
            dict = periodDict[key]
            if 'hour' not in dict.keys():
                periodDict[key]['hour'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23'
            if 'minute' not in dict.keys():
                periodDict[key]['minute'] = np.random.randint(low=1, high=30)
        return periodDict

    def run(self):
        # Before starting scheduler
        self.RunTests()
        self.Enter.run()
        self.emailNotifications.statsMessage()
        # Schedule
        sched = BlockingScheduler()
        sched.add_job(self.Enter.run, trigger='cron', hour=self.periodDict['enter']['hour'],
                      minute=self.periodDict['enter']['minute'], coalesce=True, misfire_grace_time=600)
        sched.add_job(self.Exit.run, trigger='cron', hour=self.periodDict['exit']['hour'],
                      minute=self.periodDict['exit']['minute'], coalesce=True, misfire_grace_time=60)
        sched.add_job(self.emailNotifications.statsMessage, trigger='cron',
                      hour=self.periodDict['email']['hour'], minute=self.periodDict['email']['minute'],
                      coalesce=True, misfire_grace_time=1200)
        try:
            print('\nStarting Job Scheduler')
            sched.start()
        except KeyboardInterrupt:
            print('Scheduler Stopping')
            sched.shutdown()
            pass
