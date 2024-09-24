from flask import Flask, request, Response, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from waitress import serve
from dotenv import load_dotenv
import eciglogistica, os, vaperalia

load_dotenv()
app = Flask(__name__)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_dir, filename)


@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form['Body']
    user_number = request.values.get('From', '')
    if incoming_msg == "1":
        print("Comenzando Scraping en Eciglogistica.")
        message = client.messages.create(
            body = "Por favor espere, la operación puede tardar algunos segundos.",
            from_ = "whatsapp:+12138949330",
            to = user_number,
        )
        productos_info = eciglogistica.scrape_page()
        message = client.messages.create(
            body = "Datos extraídos anclados al excel",
            from_ = "whatsapp:+12138949330",
            to = user_number,
            media_url='https://twilio-scraping.onrender.com/static/productos_eciglogistica.xlsx'
        )
        return Response(status=200)
    elif incoming_msg == "2":
        print("Comenzando Scraping en Vaperalia.")
        message = client.messages.create(
            body = "Por favor espere, la operación puede tardar algunos segundos.",
            from_ = "whatsapp:+12138949330",
            to = user_number,
        )
        vaperalia.scrape_page()
        message = client.messages.create(
            body = "Datos extraídos anclados al excel",
            from_ = "whatsapp:+12138949330",
            to = user_number,
            media_url='https://twilio-scraping.onrender.com/static/productos_vaperalia.xlsx'
        )
        return Response(status=200)
    elif incoming_msg == "3":
        print("Comenzando Scraping en LCA Distribution.")
        resp = MessagingResponse()
        resp.message("En Desarrollo...")
        return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("="*10+" Comandos "+"="*10+"\n (1) Scrapear Eciglogistica \n (2) Scrapear Vaperalia \n (3) Scrapear LCA Distribution")
        return str(resp)


if __name__ == "__main__":
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    #print(static_dir)
    print("API Online!")
    serve(app, host="0.0.0.0", port=5000)