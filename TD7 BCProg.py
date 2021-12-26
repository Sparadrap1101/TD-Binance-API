import json
import requests

BaseURL = 'https://api.binance.com'


def availableCrypto():
    r = requests.get(BaseURL + "/api/v3/exchangeInfo")
    results = r.json()

    baseAssets = []
    for baseAsset in results['symbols']:
        baseAssets.append(baseAsset['baseAsset']) # On récupère que les baseAsset pour avoir toutes les cryptos disponibles.

    print("These are all available cryptocurrencies on Binance :")
    i = 0
    for allAssets in baseAssets:
        if baseAssets[i - 1] != allAssets: # On évite de répéter les assets qui ont déjà été display (dans la liste que fourni l'API ils sont à côté donc on compare les assets voisins).
            print("> " + allAssets)
        i = i + 1
    

def orderBook(symbol):
    r = requests.get(BaseURL + "/api/v3/depth", params={'symbol': symbol})
    results = r.json()

    print("\n\nBids in Order Book for " + symbol + " pair :\n")
    for bids in results["bids"]:
        print("Price : " + bids[0] + " | Quantity : " + bids[1])

    print("\n\nAsks in Order Book for " + symbol + " pair :\n")
    for asks in results["asks"]:
        print("Price : " + asks[0] + " | Quantity : " + asks[1])


def getDepth(direction, symbol, limit):
    r = requests.get(BaseURL + "/api/v3/depth", params={'symbol': symbol, 'limit': limit})
    results = r.json()

    print("\n\n" + direction + " in Order Book for " + symbol + " pair :\n")
    for sideWant in results[direction]:
        print("Price : " + sideWant[0] + " | Quantity : " + sideWant[1])


def refreshDataCandle(symbol, interval, limit):
    r = requests.get(BaseURL + "/api/v3/klines", params={'symbol': symbol, 'interval': interval, 'limit': limit})
    results = r.json()

    print("\n\nDetail des " + str(limit) + " dernières bougies en " + interval + " sur " + symbol + " :\n")
    for dataCandle in results:
        print("Open Time : " + str(dataCandle[0]) + " | Open : " + str(dataCandle[1]) + " | High : " + str(dataCandle[2]) + " | Low : " + str(dataCandle[3])
        + " | Close : " + str(dataCandle[4]) + " | Volume : " + str(dataCandle[5]) + " | Close Time : " + str(dataCandle[6]) + " | Nbre of trade : " + str(dataCandle[8]))


if __name__ == '__main__':
    continueLoop = True
    while continueLoop == True:
        print("Bonjour, que voulez-vous tester ?")
        print("\n1) Liste de toutes les cryptomonnaies.\n2) Liste des Asks ou Bids d'une paire.\n3) Le détail de l'Order Book d'une paire.\n4) Le détail des bougies d'une paire.\n0) Exit.")
        userGuess = int(input("> "))

        if userGuess == 1:
            availableCrypto()

        elif userGuess == 2:
            print("\n\nDéfinissez les paramètres que vous souhaités :\n")
            asksBids = input("Mettez 1 pour Asks ou 2 pour Bids > ")
            symbol = input("Notez le symbol de votre choix (tapez 1 pour avoir BTCUSDT) > ")
            limit = int(input("Notez le nbre de ligne à afficher que vous souhaitez (max 1.000) > "))
            if symbol == "1":
                symbol = "BTCUSDT"
            if asksBids == "1":
                getDepth("asks", symbol, limit)
            elif asksBids == "2":
                getDepth("bids", symbol, limit)
            else:
                print("Veuillez réessayer.")

        elif userGuess == 3:
            print("\n\nDéfinissez les paramètres que vous souhaités :\n")
            symbol = input("Notez le symbol de votre choix (tapez 1 pour avoir BTCUSDT) > ")
            if symbol == "1":
                symbol = "BTCUSDT"
            orderBook(symbol)

        elif userGuess == 4:
            print("\n\nDéfinissez les paramètres que vous souhaités :\n")
            symbol = input("Notez le symbol de votre choix (tapez 1 pour avoir BTCUSDT) > ")
            interval = input("Notez l'interval de votre choix (tapez 1 pour avoir 5m) > ")
            limit = int(input("Notez le nbre de ligne à afficher que vous souhaitez (max 1.000) > "))
            if symbol == "1":
                symbol = "BTCUSDT"
            if interval == "1":
                interval = "5m"

            refreshDataCandle(symbol, interval, limit)

        elif userGuess == 0:
            continueLoop = False

        else:
            "Votre réponse est erronée, veuillez réessayer."
    
        input("Press enter to continue")
        print("\n\n")