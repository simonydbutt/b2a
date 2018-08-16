from telnetlib import Telnet
import time

# Don't want to add any email/password to git codebase so only testing the gmail server connection


def test_connection():
    T = Telnet()
    T.open('smtp.gmail.com', port=587)
    time.sleep(0.5)
    assert T.read_eager().decode().split(' ')[0] == '220'
    T.close()


if __name__ == '__main__':
    test_connection()