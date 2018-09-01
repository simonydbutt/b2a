import Settings
import os
import shutil


class CreateCleanDir:

    def __init__(self, filePathList):
        self.filePathList = filePathList

    def create(self):
        for filePath in self.filePathList:
            path = '%s/%s' % (Settings.BASE_PATH, filePath)
            if not os.path.exists(path):
                os.mkdir(path)

    def clean(self):
        for filePath in self.filePathList:
            path = '%s/%s' % (Settings.BASE_PATH, filePath)
            if os.path.exists(path):
                shutil.rmtree(path)
