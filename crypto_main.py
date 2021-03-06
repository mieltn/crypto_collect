import requests
from bs4 import BeautifulSoup

from database import connect, insert

from config import REQ, CURRENCIES
from config import DATABASE, USER


def getCurrency(url, cur):
    '''
    Gets specified currency's rate and market cap
    '''

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rate = (
        soup
        .find('div', attrs={'class': 'priceValue'})
        .find('span')
        .text
    )

    market_cap = (
        soup
        .find('div', attrs={'class': 'statsValue'})
        .text
    )

    return {
        'rate': float(rate[1:].replace(',', '')),
        'market_cap': float(market_cap[1:].replace(',', '')),
        'crypto_name': cur
    }


def runCryptoUpdate():
    '''
    Handles data updates
    '''

    conn = connect(DATABASE, USER)
    cursor = conn.cursor()

    for CUR in CURRENCIES:

        url = '/'.join([REQ, CUR])
        data = getCurrency(url, CUR)
        print(data)
        print(insert(cursor, data))
        conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    runCryptoUpdate()
