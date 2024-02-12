import asyncio
import pymysql
import requests
from telethon import TelegramClient, events, sync
#from keys import api_id, api_hash
from re import search
import telebot
from datetime import datetime
import psycopg2

api_id = 24512328
api_hash = "cc5f63b55d33f6a97b1f60336201ff22"

api_key = "w2zvYwzp3mBbOaWmPp"
api_secret = "7qyF3nAAIDVxymR4BeUgpSu5AKvH7mOkKtlv"

trade_pairs_bybit = ['1INCHUSDT', '1SOLUSDT', '3PUSDT', '5IREUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ACSUSDT',
                   'ADAUSDT', 'AFCUSDT', 'AFGUSDT', 'AGIUSDT', 'AGIXUSDT', 'AGLAUSDT', 'AGLDUSDT',
                   'AIOZUSDT', 'AKIUSDT', 'ALGOUSDT', 'ANKRUSDT', 'APEUSDT', 'APEXUSDT', 'APPUSDT',
                   'APTUSDT', 'ARBUSDT', 'ARKMUSDT', 'ARTYUSDT', 'ARUSDT', 'ATOMUSDT', 'AVAUSDT',
                   'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'AZYUSDT', 'BABYDOGEUSDT', 'BARUSDT', 'BATUSDT',
                   'BCHUSDT', 'BEAMUSDT', 'BELUSDT', 'BICOUSDT', 'BLURUSDT', 'BNBUSDT', 'BNTUSDT', 'BOBAUSDT', 'BOBUSDT', 'BONKUSDT',
                   'BTGUSDT', 'BTTUSDT', 'C98USDT', 'CAKEUSDT', 'CANDYUSDT', 'CAPOUSDT',
                   'CAPSUSDT', 'CATUSDT', 'CBKUSDT', 'CBXUSDT', 'CELOUSDT', 'CELUSDT', 'CGPTUSDT', 'CHRPUSDT', 'CHZUSDT', 'CITYUSDT',
                   'CMPUSDT', 'COMPUSDT', 'COMUSDT', 'COQUSDT', 'COREUSDT', 'COTUSDT', 'COUSDT', 'CRDSUSDT', 'CRVUSDT', 'CTCUSDT',
                   'CTTUSDT', 'CULTUSDT', 'CUSDUSDT', 'CWARUSDT', 'CYBERUSDT', 'DAIUSDT', 'DCRUSDT', 'DEFIUSDT', 'DEFYUSDT', 'DEVTUSDT',
                   'DFIUSDT', 'DGBUSDT', 'DICEUSDT', 'DLCUSDT', 'DMAILUSDT', 'DOGEUSDT', 'DOMEUSDT',
                   'DOTUSDT', 'DPXUSDT', 'DSRUNUSDT', 'DUELUSDT', 'DYDXUSDT', 'DZOOUSDT', 'ECOXUSDT',
                   'EGLDUSDT', 'EGOUSDT', 'ELDAUSDT', 'ELTUSDT', 'ENJUSDT', 'ENSUSDT', 'EOS2LUSDT', 'EOS2SUSDT', 'EOSUSDT', 'ERTHAUSDT',
                   'ETC2LUSDT', 'ETCUSDT', 'EVERUSDT', 'FAMEUSDT',
                   'FARUSDT', 'FBUSDT', 'FETUSDT', 'FIDAUSDT', 'FILUSDT', 'FIREUSDT', 'FITFIUSDT', 'FLIPUSDT', 'FLOKIUSDT', 'FLOWUSDT',
                   'FLRUSDT', 'FMBUSDT', 'FMCUSDT', 'FONUSDT', 'FORTUSDT', 'FTMUSDT', 'FTTUSDT', 'FXSUSDT',
                   'GALAUSDT', 'GALFTUSDT', 'GALUSDT', 'GCAKEUSDT', 'GENEUSDT', 'GGMUSDT', 'GGUSDT', 'GLMRUSDT', 'GMTUSDT', 'GMUSDT', 'GMXUSDT', 'GNSUSDT', 'GODSUSDT', 'GPTUSDT', 'GRAPEUSDT', 'GRTUSDT',
                   'GSTSUSDT', 'GSTUSDT', 'GSWIFTUSDT', 'GTAIUSDT', 'HBARUSDT', 'HEROUSDT', 'HFTUSDT', 'HNTUSDT', 'HONUSDT',
                   'HOOKUSDT', 'HOTUSDT', 'HVHUSDT', 'ICPUSDT', 'ICXUSDT', 'IDUSDT', 'IMXUSDT', 'INJUSDT', 'INSPUSDT',
                   'INTERUSDT', 'IRLUSDT', 'IZIUSDT', 'JASMYUSDT', 'JEFFUSDT', 'JSTUSDT', 'JTOUSDT', 'JUPUSDT', 'JUVUSDT',
                   'KARATEUSDT', 'KASTAUSDT', 'KASUSDT', 'KAVAUSDT', 'KCALUSDT', 'KCSUSDT', 'KDAUSDT', 'KLAYUSDT', 'KMONUSDT',
                   'KOKUSDT', 'KONUSDT', 'KRLUSDT', 'KSMUSDT', 'KUBUSDT', 'KUNCIUSDT', 'LADYSUSDT', 'LDOUSDT', 'LEVERUSDT',
                   'LFWUSDT', 'LGXUSDT', 'LINGUSDT', 'LINKUSDT', 'LISUSDT', 'LMWRUSDT', 'LOOKSUSDT',
                   'LRCUSDT', 'LTCUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MANTAUSDT',
                   'MASKUSDT', 'MATICUSDT', 'MBOXUSDT', 'MBSUSDT', 'MBXUSDT', 'MCRTUSDT', 'MCTUSDT',
                   'MDAOUSDT', 'MEEUSDT', 'MELOSUSDT', 'MEMEUSDT', 'METHUSDT', 'MIBRUSDT', 'MINAUSDT', 'MIXUSDT', 'MKRUSDT', 'MLKUSDT',
                   'MMCUSDT', 'MNTUSDT', 'MNZUSDT', 'MOVEZUSDT', 'MOVRUSDT', 'MPLXUSDT', 'MTCUSDT', 'MTKUSDT', 'MUSDUSDT', 'MVLUSDT',
                   'MVUSDT', 'MXMUSDT', 'MXUSDT', 'MYRIAUSDT', 'MYROUSDT', 'NEARUSDT', 'NEONUSDT', 'NESSUSDT', 'NEXOUSDT', 'NEXTUSDT',
                   'NFTUSDT', 'NYMUSDT', 'OASUSDT', 'OBXUSDT', 'OKGUSDT', 'OMGUSDT', 'OMNIUSDT', 'OMNUSDT', 'ONDOUSDT', 'ONEUSDT',
                   'OPUSDT', 'ORDIUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PEPE2USDT', 'PEPEUSDT', 'PERPUSDT',
                   'PIPUSDT', 'PLANETUSDT', 'PLAYUSDT', 'PLTUSDT', 'PLYUSDT', 'POKTUSDT', 'POLUSDT', 'PORT3USDT', 'PPTUSDT',
                   'PRIMALUSDT', 'PRIMEUSDT', 'PSGUSDT', 'PSPUSDT', 'PSTAKEUSDT', 'PTUUSDT', 'PUMLXUSDT', 'PYTHUSDT', 'PYUSDUSDT',
                   'QMALLUSDT', 'QNTUSDT', 'QTUMUSDT', 'RACAUSDT', 'RAINUSDT', 'RATSUSDT', 'RDNTUSDT', 'REALUSDT', 'RENUSDT',
                   'RLTMUSDT', 'RNDRUSDT', 'RONDUSDT', 'ROOTUSDT', 'ROSEUSDT', 'RPKUSDT', 'RPLUSDT', 'RSS3USDT', 'RUNEUSDT',
                   'RVNUSDT', 'SAILUSDT', 'SALDUSDT', 'SANDUSDT', 'SAROSUSDT', 'SATSUSDT', 'SCRTUSDT',
                   'SCUSDT', 'SEILORUSDT', 'SEIUSDT', 'SEORUSDT', 'SFUNDUSDT', 'SHIBUSDT', 'SHILLUSDT', 'SHRAPUSDT',
                   'SIDUSUSDT', 'SISUSDT', 'SLGUSDT', 'SLPUSDT', 'SNXUSDT', 'SOLOUSDT', 'SOLUSDT', 'SONUSDT', 'SOSUSDT',
                   'SPARTAUSDT', 'SPELLUSDT', 'SQRUSDT', 'SRMUSDT', 'SSVUSDT', 'STATUSDT', 'STETHUSDT', 'STGUSDT', 'STRMUSDT',
                   'STXUSDT', 'SUIAUSDT', 'SUIUSDT', 'SUNUSDT', 'SUSHIUSDT', 'SWEATUSDT', 'SYNRUSDT', 'TAMAUSDT', 'TAPUSDT',
                   'TAVAUSDT', 'TELUSDT', 'TENETUSDT', 'THETAUSDT', 'THNUSDT', 'TIAUSDT', 'TIMEUSDT', 'TOKENUSDT', 'TOMIUSDT',
                   'TOMSUSDT', 'TONUSDT', 'TRCUSDT', 'TRIBEUSDT', 'TRVLUSDT', 'TRXUSDT', 'TURBOSUSDT',
                   'TVKUSDT', 'TWTUSDT', 'UMAUSDT', 'UNIUSDT', 'USDCUSDT', 'USDDUSDT', 'USDYUSDT', 'USTCUSDT', 'VANRYUSDT',
                   'VEGAUSDT', 'VELAUSDT', 'VELOUSDT', 'VEXTUSDT', 'VICUSDT', 'VINUUSDT', 'VPADUSDT', 'VPRUSDT', 'VRAUSDT',
                   'VRTXUSDT', 'VVUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBTCUSDT', 'WEMIXUSDT', 'WLDUSDT', 'WLKNUSDT', 'WOOUSDT',
                   'WWYUSDT', 'XAIUSDT', 'XAVAUSDT', 'XCADUSDT', 'XDCUSDT', 'XECUSDT', 'XEMUSDT', 'XETAUSDT', 'XLMUSDT',
                   'XRP3LUSDT', 'XRP3SUSDT', 'XRPUSDT', 'XTZUSDT', 'XWGUSDT', 'XYMUSDT', 'YFIUSDT', 'ZAMUSDT', 'ZENUSDT',
                   'ZETAUSDT', 'ZIGUSDT', 'ZILUSDT', 'ZKFUSDT', 'ZRXUSDT', 'ZTXUSDT']

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
chat_id = -695765690

client = TelegramClient('session_name', api_id, api_hash, system_version="4.16.30-vxCUSTOM")
client.start()

chats = {}

for dialog in client.iter_dialogs():
    chats[dialog.id] = dialog.name

@client.on(events.NewMessage(chats=["Front & Back guys", "Турнички и Братишки", "CAZADOR CRYPTO", "Плечо Профессора", "Maloletoff | Crypto-Angel", "Crypto▫️Man💎", "Trade Community"]))
async def normal_handler(event):
    '''получение сообщения'''
    info = event.message.to_dict()
    mes = info['message']
    '''фиксация текущего времени'''
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        '''получение наименования чата'''
        chat = chats[event.chat_id]
    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id, f"ОШИБКА - {e}\n"
                                                            f"Не смог определить группу")
    try:
        '''берем куски сообщения для поиска крипты и дейсвтий c ней'''
        x = [i for i in trade_pairs_bybit if search(i[:-4], mes)]
        y = [i for i in ["LONG", "SHORT"] if search(i, mes)]

        if len(x) > 0 and len(y) > 0:
            result = sorted(x, key=lambda x: -len(x))[0]
            telebot.TeleBot(telega_token).send_message(chat_id, f"Закупаем - {result}\n"
                                                                f"Вид торговли - {y[0]}\n"
                                                                f"Группа - {chat}\n"
                                                                f"Время: {current_time}")
            '''Получаем цену'''
            a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
            price = a.json()["result"]["price"]
            values = (current_time, chat, result, price)
            try:
                connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                              database='invest')
                try:
                    with connection.cursor() as cursor:
                        insert_query = "INSERT INTO analize_orders (time, chat_title, name_cript, price_buy)" \
                                       "VALUES (%s, %s, %, %s) RETURNING id;"
                        cursor.execute(insert_query, (values))
                        id_change = cursor.fetchone()[0]
                        connection.commit()
                finally:
                    connection.close()

                '''Ждем час и записываем цену в базу'''
                await asyncio.sleep(3600)
                a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
                price = a.json()["result"]["price"]
                try:
                    connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                                  database='invest')
                    try:
                        with connection.cursor() as cursor:
                            insert_query = f"UPDATE analize_orders set price_in_1hour = {price} where id = {id_change}"
                            cursor.execute(insert_query)
                            connection.commit()

                    finally:
                        connection.close()
                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

                '''Ждем 2 часа и записываем цену в базу'''
                await asyncio.sleep(3600)
                a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
                price = a.json()["result"]["price"]
                try:
                    connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                                  database='invest')
                    try:
                        with connection.cursor() as cursor:
                            insert_query = f"UPDATE analize_orders set price_in_2hour = {price} where id = {id_change}"
                            cursor.execute(insert_query)
                            connection.commit()

                    finally:
                        connection.close()
                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

                '''Ждем 3 часа и записываем цену в базу'''
                await asyncio.sleep(3600)
                a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
                price = a.json()["result"]["price"]
                try:
                    connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                                  database='invest')
                    try:
                        with connection.cursor() as cursor:
                            insert_query = f"UPDATE analize_orders set price_in_3hour = {price} where id = {id_change}"
                            cursor.execute(insert_query)
                            connection.commit()

                    finally:
                        connection.close()
                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

                '''Ждем 5 часов и записываем цену в базу'''
                await asyncio.sleep(7200)
                a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
                price = a.json()["result"]["price"]
                try:
                    connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                                  database='invest')
                    try:
                        with connection.cursor() as cursor:
                            insert_query = f"UPDATE analize_orders set price_in_5hour = {price} where id = {id_change}"
                            cursor.execute(insert_query)
                            connection.commit()

                    finally:
                        connection.close()
                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

                '''Ждем 24 часа и записываем цену в базу'''
                await asyncio.sleep(68400)
                a = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={result}')
                price = a.json()["result"]["price"]
                try:
                    connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                                  database='invest')
                    try:
                        with connection.cursor() as cursor:
                            insert_query = f"UPDATE analize_orders set price_in_24hour = {price} where id = {id_change}"
                            cursor.execute(insert_query)
                            connection.commit()

                    finally:
                        connection.close()
                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

            except Exception as e:
                telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id, f"MESSAGE - {mes}\n"
                                                            f"ОШИБКА - {e}\n"
                                                            f"Группа - {chat}\n"
                                                            f"Время: {current_time}")



client.run_until_disconnected()


# for dialog in client.iter_dialogs():
#     pass
#
# mess = [message.text for message in client.iter_messages('CAZADOR CRYPTO', limit=10)]
#
# for i in mess[:9]:
#     if len(i) > 0:
#         d = i.split()[0][2:]
#         if d + "USDT" in trading_pairss:
#             print(d)
#
#
