from Pipeline.main.PositionSize.Position import Position
import Settings
import yaml

dbPath = 'Pipeline/tests/test_DB'
with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath)) as capFile:
    capDict = yaml.load(capFile)
with open('%s/%s/Configs/testStrat.yml' % (Settings.BASE_PATH, dbPath)) as stratFile:
    stratDict = yaml.load(stratFile)


def test_Positon():
    P = Position(stratConfig=stratDict, capConfig=capDict)
    assert P.getSize() == 0.5


if __name__ == '__main__':
    test_Positon()