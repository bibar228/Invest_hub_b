import datetime
import time

import psycopg2
import requests

x = [['TOKENUSDT', '2024-03-21 07:16:36'],
['FLOKIUSDT', '2024-03-21 07:16:36'],
['ONDOUSDT', '2024-03-21 07:16:36'],
['LADYSUSDT', '2024-03-13 06:13:56'],
['RNDRUSDT', '2024-03-07 16:14:49'],
['SOLUSDT', '2024-03-07 14:23:51'],
['APEXUSDT', '2024-03-05 11:36:28'],
['PEPEUSDT', '2024-02-26 14:39:38'],
['C98USDT', '2024-02-15 03:54:58'],
['BONKUSDT', '2024-02-15 03:51:08'],
['SUIUSDT', '2024-02-15 03:46:17'],
['ENSUSDT', '2024-02-06 05:59:51'],
['CAKEUSDT', '2024-01-17 02:43:05'],
['SHIBUSDT', '2024-01-11 12:51:17'],
['PERPUSDT', '2024-01-02 06:11:03'],
['SEIUSDT', '2023-12-26 11:05:45'],
['VINUUSDT', '2023-12-25 06:43:34'],
['KSMUSDT', '2023-12-25 06:37:03'],
['WLDUSDT', '2023-12-19 06:49:36'],
['INJUSDT', '2023-12-14 01:59:47'],
['SHRAPUSDT', '2023-12-05 06:02:25'],
['TONUSDT', '2023-11-30 04:09:34'],
['EOSUSDT', '2023-11-30 04:09:34'],
['FTTUSDT', '2023-11-30 04:09:34'],
['HFTUSDT', '2023-11-30 04:09:34'],
['NFTUSDT', '2023-11-30 04:09:34'],
['DAIUSDT', '2023-11-25 06:04:17'],
['DYDXUSDT', '2023-11-15 16:16:17'],
['BNTUSDT', '2023-11-13 01:11:19'],
['LINKUSDT', '2023-11-10 23:57:02'],
['TIMEUSDT', '2023-10-13 01:20:29'],
['SPELLUSDT', '2023-10-12 07:54:11'],
['GALUSDT', '2023-10-12 07:54:11'],
['CYBERUSDT', '2023-09-19 06:35:31'],
['DOGEUSDT', '2023-08-30 07:32:13'],
['OPUSDT', '2023-08-30 07:32:13'],
['XLMUSDT', '2023-08-20 04:30:49'],
['XRPUSDT', '2023-08-18 11:27:51'],
['DOTUSDT', '2023-08-17 05:13:29'],
['GSWIFTUSDT', '2023-08-08 09:11:25'],
['BCHUSDT', '2023-08-07 06:40:31'],
['TUSDT', '2023-08-06 04:41:21']]
import pandas as pd

def kline(symb, tf):
    url = "https://api.bybit.com"
    path = "/v5/market/kline"
    URL = url + path
    params = {"category": "linear", "symbol": symb, "interval": tf, "limit": 1000}
    r = requests.get(URL, params=params)
    df = pd.DataFrame(r.json()["result"]["list"])
    m = pd.DataFrame()
    m["Date"] = pd.to_datetime(df.loc[:, 0], unit="ms")
    m["Open"] = df.iloc[:, 1].astype(float)
    return m
res = {}
for i in x:
    try:
        t = kline(i[0], "D")
        print(i[0], i[1].split()[0])
        num = int(str(t.loc[t['Date'] == i[1].split()[0]]["Open"])[0])
        print(num)
        a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={i[0]}')
        price = a.json()["result"]["price"]
        tm = list(reversed([str(i) for i in t["Date"][:num+1].tolist()]))
        pr = list(reversed([str(i) for i in t["Open"][:num+1].tolist()]))
        print(tm)
        print(pr)
        times = time.localtime(time.time())
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", times)
        # m = t["Open"].loc[num:]
        # print(m)
        #res[i[0]] = [str(t.loc[t['Date'] == i[1].split()[0]]["Open"]).split()[1], price]
        values = (i[0], i[1], formatted_time, "LONG", str(t.loc[t['Date'] == i[1].split()[0]]["Open"]).split()[1], price, 'CRYPTO-ANGEL: PRIVATE')
        try:
            connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                          database='invest')
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO analize_siggs (cryptocode, init_time, end_time, trade_position, trade_position_start, trade_position_end, signal_owner)" \
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
                    cursor.execute(insert_query, values)
                    id_change = cursor.fetchone()[0]
                    connection.commit()
            finally:
                connection.close()
        except Exception as e:
            print(e)
    except Exception as e:
        pass

print(res)
res = {'TOKENUSDT': ['0.0882', '0.22355'], 'ONDOUSDT': ['0.6578', '0.90564'], 'RNDRUSDT': ['9.32845', '11.473'], 'SOLUSDT': ['130.943', '195.18'], 'C98USDT': ['0.2834', '0.4129'], 'SUIUSDT': ['1.9084', '1.7949'], 'ENSUSDT': ['20.192', '23.114'], 'CAKEUSDT': ['2.966', '4.5042'], 'PERPUSDT': ['1.3917', '1.5999'], 'SEIUSDT': ['0.39356', '0.8609'], 'KSMUSDT': ['51.6', '51.0673'], 'WLDUSDT': ['3.945', '9.1581'], 'INJUSDT': ['29.293', '40.553'], 'TONUSDT': ['2.436', '5.287'], 'EOSUSDT': ['0.6797', '1.0969'], 'FTTUSDT': ['Name:', '2.2692'], 'HFTUSDT': ['0.3137', '0.4672'], 'DYDXUSDT': ['3.944', '3.686'], 'BNTUSDT': ['1.47155', '0.904'], 'LINKUSDT': ['14.615', '20.5376'], 'SPELLUSDT': ['0.000444', '0.00127411'], 'GALUSDT': ['1.146', '5.5386'], 'CYBERUSDT': ['4.9344', '14.3102'], 'DOGEUSDT': ['0.06636', '0.18501'], 'OPUSDT': ['1.4938', '3.9681'], 'XLMUSDT': ['0.1237', '0.13974'], 'XRPUSDT': ['0.506', '0.6461'], 'DOTUSDT': ['4.667', '9.994'], 'BCHUSDT': ['223.0', '489.6'], 'TUSDT': ['0.02364', '0.04561']}


