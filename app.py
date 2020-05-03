
from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hi there!🙋🏽‍♂ I am Blue.i provide information on Coronavirus cases in various states in Nigeria ... try replying with  Lagos or Awka Ibom or summary or states \n_Developed by Jide_"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    # incoming_msg = incoming_msg.lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'Hi' in  incoming_msg or "hi" in incoming_msg:
        text = hello()
        msg.body(text)
        responded = True

    elif "states" in incoming_msg or "States" in incoming_msg:
        response = requests.get('https://ncdcapi.herokuapp.com/')
        if response.status_code == 200:
            states_list = str(list(response.json()["states"].keys()))[1:-1]
            text=states_list
        else:
            text='i cant get those details at this time'
        msg.body(text)
        responded = True

    elif "Summary" in incoming_msg  or "summary" in incoming_msg:
        response = requests.get('https://ncdcapi.herokuapp.com/')
        if response.status_code == 200:
                        samples_tested = response.json()["summary"]["Samples Tested"]
                        confirmed = response.json()["summary"]["Confirmed Cases"]
                        active = response.json()["summary"]["Active Cases"]
                        discharged = response.json()["summary"]["Discharged Cases"]
                        deaths = response.json()["summary"]["Death"]

                        print(samples_tested)
                        text = f'Coronavirus Summary in Nigeria \
                         \nSamples Tested  : *{samples_tested}* \
                         \nConfirmed Cases  : *{confirmed}*\
                         \nActive Cases  : *{active}*\
                         \nDischarged  : *{discharged}*\
                         \nDeaths  : *{deaths}*'
        else:
            text='i cant get those details at this time'
        msg.body(text)
        responded = True
    else:
        response = requests.get('https://ncdcapi.herokuapp.com/')     
        if response.status_code == 200:
            confirmed=response.json()["states"][incoming_msg][0]["confirmed"]
            discharged=response.json()["states"][incoming_msg][0]["discharged"]
            deaths=response.json()["states"][incoming_msg][0]["deaths"]
            text = f'Coronavirus cases in {incoming_msg} \nConfirmed Cases : *{confirmed}*  \nDischarged : *{discharged}*  \nDeaths : *{deaths}* '
        
        else:
            text = 'I could not retrieve the results at this time, sorry.'
        msg.body(text)
        responded = True
        
    if  resp.value== 500:
            text = "Reply with 'states' to check correct list of states"    
    return str(resp)

if __name__ == "__main__":
    app.run()