from flask import Flask, request, Response, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from waitress import serve
from dotenv import load_dotenv
import eciglogistica, re, os

load_dotenv()
app = Flask(__name__)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form['Body']
    user_number = request.values.get('From', '')
    if incoming_msg == "1":
        print("Eciglogistica")
        productos_info = eciglogistica.scrape_page()
        message = client.messages.create(
            body = "Excel anclado",
            from_ = "whatsapp:+12138949330",
            to = user_number,
            media_url='https://twilio-scraping.onrender.com/static/productos.xlsx'
        )
        
        """ for p in productos_info:
            ans = ""
            for key, value in p.items():
                ans += f"{key}: {value}\n"
                    
            message = client.messages.create(
                body = ans,
                from_ = "whatsapp:+12138949330",
                to = user_number,
            ) """
        return Response(status=200)
    elif incoming_msg == "2":
        print("Vaperalia ")
        resp = MessagingResponse()
        resp.message("Por implementar...")
        return str(resp)
    elif incoming_msg == "3":
        print("LCA Distribution")
        resp = MessagingResponse()
        resp.message("Por implementar...")
        return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("="*10+" Comandos "+"="*10+"\n (1) Scrapear Eciglogistica \n (2) Scrapear Vaperalia \n (3) Scrapear LCA Distribution")
        return str(resp)


if __name__ == "__main__":
    print("API Online!")
    serve(app, host="0.0.0.0", port=5000)