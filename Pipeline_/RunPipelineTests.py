import py
import Settings
import os


class RunPipelineTests:

    def __init__(self):
        currentDir = os.getcwd()
        os.chdir('%s/Pipeline_' % Settings.BASE_PATH)
        py.test.cmdline.main()
        os.chdir(currentDir)