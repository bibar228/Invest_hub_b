from telethon import TelegramClient, events, sync
from keys import api_id, api_hash
from re import search
import telebot
from datetime import datetime


trade_pairs_bybit = ['1INCHUSDT', '1SOLUSDT', '3PUSDT', '5IREUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ACSUSDT',
                   'ADA2LUSDT', 'ADA2SUSDT', 'ADAUSDT', 'AFCUSDT', 'AFGUSDT', 'AGIUSDT', 'AGIXUSDT', 'AGLAUSDT', 'AGLDUSDT',
                   'AIOZUSDT', 'AKIUSDT', 'ALGOUSDT', 'ANKRUSDT', 'APE2LUSDT', 'APE2SUSDT', 'APEUSDT', 'APEXUSDT', 'APPUSDT',
                   'APTUSDT', 'ARBUSDT', 'ARKMUSDT', 'ARTYUSDT', 'ARUSDT', 'ATOM2LUSDT', 'ATOM2SUSDT', 'ATOMUSDT', 'AVAUSDT',
                   'AVAX2LUSDT', 'AVAX2SUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'AZYUSDT', 'BABYDOGEUSDT', 'BARUSDT', 'BATUSDT',
                   'BCHUSDT', 'BEAMUSDT', 'BELUSDT', 'BICOUSDT', 'BLURUSDT', 'BNBUSDT', 'BNTUSDT', 'BOBAUSDT', 'BOBUSDT', 'BONKUSDT',
                   'BTC3LUSDT', 'BTC3SUSDT', 'BTCUSDT', 'BTGUSDT', 'BTTUSDT', 'C98USDT', 'CAKEUSDT', 'CANDYUSDT', 'CAPOUSDT',
                   'CAPSUSDT', 'CATUSDT', 'CBKUSDT', 'CBXUSDT', 'CELOUSDT', 'CELUSDT', 'CGPTUSDT', 'CHRPUSDT', 'CHZUSDT', 'CITYUSDT',
                   'CMPUSDT', 'COMPUSDT', 'COMUSDT', 'COQUSDT', 'COREUSDT', 'COTUSDT', 'COUSDT', 'CRDSUSDT', 'CRVUSDT', 'CTCUSDT',
                   'CTTUSDT', 'CULTUSDT', 'CUSDUSDT', 'CWARUSDT', 'CYBERUSDT', 'DAIUSDT', 'DCRUSDT', 'DEFIUSDT', 'DEFYUSDT', 'DEVTUSDT',
                   'DFIUSDT', 'DGBUSDT', 'DICEUSDT', 'DLCUSDT', 'DMAILUSDT', 'DOGE2LUSDT', 'DOGE2SUSDT', 'DOGEUSDT', 'DOMEUSDT',
                   'DOT3LUSDT', 'DOT3SUSDT', 'DOTUSDT', 'DPXUSDT', 'DSRUNUSDT', 'DUELUSDT', 'DYDXUSDT', 'DZOOUSDT', 'ECOXUSDT',
                   'EGLDUSDT', 'EGOUSDT', 'ELDAUSDT', 'ELTUSDT', 'ENJUSDT', 'ENSUSDT', 'EOS2LUSDT', 'EOS2SUSDT', 'EOSUSDT', 'ERTHAUSDT',
                   'ETC2LUSDT', 'ETC2SUSDT', 'ETCUSDT', 'ETH3LUSDT', 'ETH3SUSDT', 'ETHUSDT', 'ETHWUSDT', 'EVERUSDT', 'FAMEUSDT',
                   'FARUSDT', 'FBUSDT', 'FETUSDT', 'FIDAUSDT', 'FILUSDT', 'FIREUSDT', 'FITFIUSDT', 'FLIPUSDT', 'FLOKIUSDT', 'FLOWUSDT',
                   'FLRUSDT', 'FMBUSDT', 'FMCUSDT', 'FONUSDT', 'FORTUSDT', 'FTM2LUSDT', 'FTM2SUSDT', 'FTMUSDT', 'FTTUSDT', 'FXSUSDT',
                   'GALAUSDT', 'GALFTUSDT', 'GALUSDT', 'GCAKEUSDT', 'GENEUSDT', 'GGMUSDT', 'GGUSDT', 'GLMRUSDT', 'GMT2LUSDT',
                   'GMT2SUSDT', 'GMTUSDT', 'GMUSDT', 'GMXUSDT', 'GNSUSDT', 'GODSUSDT', 'GPTUSDT', 'GRAPEUSDT', 'GRTUSDT',
                   'GSTSUSDT', 'GSTUSDT', 'GSWIFTUSDT', 'GTAIUSDT', 'HBARUSDT', 'HEROUSDT', 'HFTUSDT', 'HNTUSDT', 'HONUSDT',
                   'HOOKUSDT', 'HOTUSDT', 'HVHUSDT', 'ICPUSDT', 'ICXUSDT', 'IDUSDT', 'IMXUSDT', 'INJUSDT', 'INSPUSDT',
                   'INTERUSDT', 'IRLUSDT', 'IZIUSDT', 'JASMYUSDT', 'JEFFUSDT', 'JSTUSDT', 'JTOUSDT', 'JUPUSDT', 'JUVUSDT',
                   'KARATEUSDT', 'KASTAUSDT', 'KASUSDT', 'KAVAUSDT', 'KCALUSDT', 'KCSUSDT', 'KDAUSDT', 'KLAYUSDT', 'KMONUSDT',
                   'KOKUSDT', 'KONUSDT', 'KRLUSDT', 'KSMUSDT', 'KUBUSDT', 'KUNCIUSDT', 'LADYSUSDT', 'LDOUSDT', 'LEVERUSDT',
                   'LFWUSDT', 'LGXUSDT', 'LINGUSDT', 'LINK2LUSDT', 'LINK2SUSDT', 'LINKUSDT', 'LISUSDT', 'LMWRUSDT', 'LOOKSUSDT',
                   'LRCUSDT', 'LTC2LUSDT', 'LTC2SUSDT', 'LTCUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MANTAUSDT',
                   'MASKUSDT', 'MATIC2LUSDT', 'MATIC2SUSDT', 'MATICUSDT', 'MBOXUSDT', 'MBSUSDT', 'MBXUSDT', 'MCRTUSDT', 'MCTUSDT',
                   'MDAOUSDT', 'MEEUSDT', 'MELOSUSDT', 'MEMEUSDT', 'METHUSDT', 'MIBRUSDT', 'MINAUSDT', 'MIXUSDT', 'MKRUSDT', 'MLKUSDT',
                   'MMCUSDT', 'MNTUSDT', 'MNZUSDT', 'MOVEZUSDT', 'MOVRUSDT', 'MPLXUSDT', 'MTCUSDT', 'MTKUSDT', 'MUSDUSDT', 'MVLUSDT',
                   'MVUSDT', 'MXMUSDT', 'MXUSDT', 'MYRIAUSDT', 'MYROUSDT', 'NEARUSDT', 'NEONUSDT', 'NESSUSDT', 'NEXOUSDT', 'NEXTUSDT',
                   'NFTUSDT', 'NYMUSDT', 'OASUSDT', 'OBXUSDT', 'OKGUSDT', 'OMGUSDT', 'OMNIUSDT', 'OMNUSDT', 'ONDOUSDT', 'ONEUSDT',
                   'OPUSDT', 'ORDIUSDT', 'ORTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PEPE2USDT', 'PEPEUSDT', 'PERPUSDT',
                   'PIPUSDT', 'PLANETUSDT', 'PLAYUSDT', 'PLTUSDT', 'PLYUSDT', 'POKTUSDT', 'POLUSDT', 'PORT3USDT', 'PPTUSDT',
                   'PRIMALUSDT', 'PRIMEUSDT', 'PSGUSDT', 'PSPUSDT', 'PSTAKEUSDT', 'PTUUSDT', 'PUMLXUSDT', 'PYTHUSDT', 'PYUSDUSDT',
                   'QMALLUSDT', 'QNTUSDT', 'QTUMUSDT', 'RACAUSDT', 'RAINUSDT', 'RATSUSDT', 'RDNTUSDT', 'REALUSDT', 'RENUSDT',
                   'RLTMUSDT', 'RNDRUSDT', 'RONDUSDT', 'ROOTUSDT', 'ROSEUSDT', 'RPKUSDT', 'RPLUSDT', 'RSS3USDT', 'RUNEUSDT',
                   'RVNUSDT', 'SAILUSDT', 'SALDUSDT', 'SAND2LUSDT', 'SAND2SUSDT', 'SANDUSDT', 'SAROSUSDT', 'SATSUSDT', 'SCRTUSDT',
                   'SCUSDT', 'SDUSDT', 'SEILORUSDT', 'SEIUSDT', 'SEORUSDT', 'SFUNDUSDT', 'SHIBUSDT', 'SHILLUSDT', 'SHRAPUSDT',
                   'SIDUSUSDT', 'SISUSDT', 'SLGUSDT', 'SLPUSDT', 'SNXUSDT', 'SOLOUSDT', 'SOLUSDT', 'SONUSDT', 'SOSUSDT',
                   'SPARTAUSDT', 'SPELLUSDT', 'SQRUSDT', 'SRMUSDT', 'SSVUSDT', 'STATUSDT', 'STETHUSDT', 'STGUSDT', 'STRMUSDT',
                   'STXUSDT', 'SUIAUSDT', 'SUIUSDT', 'SUNUSDT', 'SUSHIUSDT', 'SWEATUSDT', 'SYNRUSDT', 'TAMAUSDT', 'TAPUSDT',
                   'TAVAUSDT', 'TELUSDT', 'TENETUSDT', 'THETAUSDT', 'THNUSDT', 'TIAUSDT', 'TIMEUSDT', 'TOKENUSDT', 'TOMIUSDT',
                   'TOMSUSDT', 'TONUSDT', 'TRCUSDT', 'TRIBEUSDT', 'TRVLUSDT', 'TRXUSDT', 'TURBOSUSDT', 'TUSDT', 'TUSDUSDT',
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
print(chats)

@client.on(events.NewMessage(chats=["Пит", "Турнички и Братишки", "CAZADOR CRYPTO", "Плечо Профессора", "Maloletoff | Crypto-Angel", "Crypto▫️Man💎", "Trade Community"]))
async def normal_handler(event):
    info = event.message.to_dict()
    print(info)
    mes = info['message'].split()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
        ch = chats[event.chat_id]
    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id, f"ОШИБКА - {e}\n"
                                                            f"Не смог определить группу")
    try:
        true_mes = mes[0]+mes[1]+mes[2]+mes[3]+mes[4]+mes[5]+mes[6]
        x = [i for i in trade_pairs_bybit if search(i[:-4], true_mes)]
        print(true_mes)
        result = sorted(x, key=lambda x: -len(x))[0]
        telebot.TeleBot(telega_token).send_message(chat_id, f"Закупаем - {result}\n"
                                                            f"Группа - {ch}\n"
                                                            f"Время: {current_time}")
    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id, f"ОШИБКА - {e}\n"
                                                            f"Группа - {ch}\n"
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
