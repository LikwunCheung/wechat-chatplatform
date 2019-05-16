# -*- coding: utf-8 -*-

import requests
import time
import ujson


DOMAIN = 'http://api.k780.com'
APP_KEY = '39410'
APP_SIGN = 'b1ba8672d7a34cb6073953d6fdec7bcf'


class Currency(object):

    last_update = 0
    rate = 0

    def __init__(self, scur='AUD', tcur='CNY'):
        self.params = dict(
            app='finance.rate',
            scur=scur,
            tcur=tcur,
            appkey=APP_KEY,
            sign=APP_SIGN,
            format='json'
        )
        self.get_newest()

    def get_newest(self):
        self.last_update = time.time()
        resp = requests.get(DOMAIN, params=self.params)
        resp = ujson.loads(resp.content)
        self.rate = float(resp['result']['rate']) + 0.05

    def get(self):
        if time.time() - self.last_update > 1800:
            self.get_newest()
        return self.rate


AUD_CNY = Currency('AUD', 'CNY')


if __name__ == '__main__':
    currency = Currency('AUD', 'CNY')
    print(currency.get())