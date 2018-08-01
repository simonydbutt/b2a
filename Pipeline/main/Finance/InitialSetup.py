import yaml
import Settings
import os
from tinydb import TinyDB


class InitalSetup:

    def __init__(self, initialCapital):
        filePath = '%s/Pipeline/DB/Capital.yml' % Settings.BASE_PATH
        response = '1'
        if os.path.exists(filePath):
            print('Capital file already exists')
            print('User input required')
            print('1   \t-\tReplace existing file')
            print('Else\t-\tIgnore request')
            response = str(input())
        if response == '1':
            with open(filePath, 'w') as file:
                yaml.dump(
                    {
                        'initialCapital': initialCapital,
                        'liquidCurrent': initialCapital,
                        'paperCurrent': initialCapital,
                        'percentAllocated': 0,
                        'paperPnL': 0,
                    }, file
                )
            TinyDB('%s/Pipeline/DB/PerformanceLogs/DailyCapitalLog.ujson' % Settings.BASE_PATH)
