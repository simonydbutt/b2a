import py
import Settings
import os
import logging


class RunPipelineTests:

    def __init__(self):
        logging.info('Starting Pipeline pytests')
        currentDir = os.getcwd()
        os.chdir('%s/Pipeline' % Settings.BASE_PATH)
        py.test.cmdline.main()
        os.chdir(currentDir)
