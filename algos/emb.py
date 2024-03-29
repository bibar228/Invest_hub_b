import requests
import pandas as pd

a = requests.get("https://api.bybit.com/spot/v3/public/symbols")
df = pd.DataFrame(a.json()["result"]["list"])
all_crypts_bybit = sorted([i for i in df["name"].values if i[-4:] == "USDT"])


with open("sigs.txt", "r", encoding="utf-8") as file:
    sigs = file.readlines()

gg = []

ignor = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

for i in range(len(sigs)):
    try:
        '''берем куски сообщения для поиска крипты и дейсвтий c ней'''
        bybit_sig = []
        bybit_sig2 = []
        for j in sigs[i].split():
            if j.upper() + "USDT" in all_crypts_bybit and j.upper() + "USDT" not in ignor:

                bybit_sig.append([j.upper() + "USDT", sigs[i+1][:-1]])

        for g in sigs[i].split():
            for j in all_crypts_bybit:
                if g.upper() == j[:-4] and g.upper() + "USDT" not in ignor:
                    bybit_sig2.append([g.upper() + "USDT", sigs[i+1][:-1]])

        res = []
        for i in bybit_sig:
            if i not in res:
                res.append(i)

        for i in bybit_sig2:
            if i not in res:
                res.append(i)

        for m in res:
            if m[0] not in [i[0] for i in gg]:
                gg.append(m)
    except:
        pass

for i in gg:
    print(i)


