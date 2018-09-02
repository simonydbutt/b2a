import requests

"""
    Don't want to make it extensive (especially when not using) as actual pull will be hella slow
"""


def test_connection():
    assert requests.get('https://coinmarketcap.com/all/views/all').status_code == 200


if __name__ == '__main__':
    test_connection()