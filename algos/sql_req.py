
import psycopg2
import telebot
telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
chat_id = -695765690

def get_crypto() -> list:
    try:
        connection = psycopg2.connect(host='127.0.0.1', port=5432, user='mag_user', password='warlight123',
                                             database='invest')
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from analize_orders")
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR get top cripto connect: {e}\n")

