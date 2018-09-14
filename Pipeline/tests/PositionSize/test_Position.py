from Pipeline.main.PositionSize.Position import Position
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml


resPath = 'Pipeline/resources/testPosition'
CCD = CreateCleanDir([resPath])


def before():
    CCD.create()
    capDict = {'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
               'paperPnL': 0, 'percentAllocated': 0}
    with open('%s/%s/capital.yml' % (Settings.BASE_PATH, resPath), 'w') as capFile:
        yaml.dump(capDict, capFile)
    configDict = {'positionSize': {'name': 'Basic', 'percent': 0.05}}
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(configDict, configFile)


def test_Positon():
    before()
    P = Position(stratName='testPosition')
    assert P.getSize() == 0.5
    CCD.clean()


if __name__ == '__main__':
    test_Positon()