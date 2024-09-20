from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import eciglogistica

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form['Body']
    if incoming_msg == "1":
        excel = eciglogistica.scrape_page()
        with open(excel, 'rb') as f:
            file_data = f.read()
        resp = MessagingResponse()
        resp.message("Aquí está la información").media(file_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return str(resp)
    elif incoming_msg == "2":
        resp = MessagingResponse()
        resp.message("Por implementar...")
        return str(resp)
    elif incoming_msg == "3":
        resp = MessagingResponse()
        resp.message("Por implementar...")
        return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("Comandos: \n 1.Scrapear Eciglogistica \n 2.Scrapear Vaperalia \n 3.Scrapear LCA Distribution")
        return str(resp)


if __name__ == "__main__":
    app.run(debug=True)