import os
import tkinter
from tkinter.filedialog import askopenfilename
import rumps
from pycoingecko import CoinGeckoAPI


def translate_from_symbol(symbol):
    namesFromSymbols = [["btc", "bitcoin"], ["eth", "ethereum"], ["usdt", "tether"], ["usdc", "usd-coin"],
                        ["bnb", "binancecoin"], ["xrp", "ripple"], ["busd", "binance-usd"], ["ada", "cardano"],
                        ["sol", "solana"], ["dot", "polkadot"], ["doge", "dogecoin"], ["shib", "shiba-inu"],
                        ["dai", "dai"], ["steth", "staked-ether"], ["matic", "matic-network"], ["avax", "avalanche"],
                        ]

    for subarray in namesFromSymbols:
        if symbol == subarray[0]:
            return subarray[1]

    return "error"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class CryptoBar(object):
    def __init__(self):
        self.config = {
            "app_name": "CryptoBar",
            "add_coin": "Add Transaction",
            "interval": 60
        }

        self.app = rumps.App(self.config["app_name"])

        self.cg = CoinGeckoAPI()
        self.coins = []

        tkinter.Tk().withdraw()
        cryptofile = askopenfilename()
        crypto = open(cryptofile, "r").readlines()
        for line in crypto:
            array = line.split(" ")

            name = ""
            for content in array:
                if is_number(content):
                    self.coins.append([name.strip(), content.strip()])
                else:
                    name = name + content + " "

        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.calculatePrice()
        self.start_timer()

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            self.calculatePrice()
            self.start_timer()

        sender.count += 1

    def calculatePrice(self):
        finalBalance = 0

        for coin in self.coins:
            array = self.cg.get_price(ids=coin[0], vs_currencies='eur', include_market_cap='true')
            price = array[coin[0].lower()]
            finalBalance += float(price["eur"]) * float(coin[1])

        self.app.title = "{:.2f}".format(finalBalance) + "€"

    def start_timer(self):
        self.timer.count = 0
        self.timer.end = self.interval
        self.timer.start()


    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = CryptoBar()
    app.run()
