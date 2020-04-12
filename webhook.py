import json
import os
import requests
#it is microframework to develop a web app
from flask import Flask
from flask import request
from flask import make_response
from datetime import datetime

#Falsk app for our web app

app=Flask(__name__)

# app route decorator. when webhook is called, the decorator would call the functions which are e defined

@app.route('/webhook', methods=['POST'])

def webhook():
    # convert the data from json
    req = request.get_json(silent=True, force=True)

    print(json.dumps(req, indent=4))

    # extract the relevant information and use api and get the response and send it dialogflow.

    # helper function
    res=makeResponse(req)
    res=json.dumps(res, indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r

#extract parameter values, query weahter api, construct the resposne
def makeResponse(req):

    condition: str = "No Information Available"

    result=req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date-time")


    if not date == "" or date == None:
        if 'T' in date:
            new_date: str = date.split('T')[0]
        else:
            new_date: str = date[0:10]
    else:
        new_date = datetime.today().strftime("%Y-%m-%d")

    url_str: str = "http://api.openweathermap.org/data/2.5/forecast?q="+str(city)+",in&appid=db91df44baf43361cbf73026ce5156cb"

    r = requests.get(url_str)
    json_object = r.json()
    weather = json_object['list']

    for i in range(0,40):
        if new_date in weather[i]['dt_txt']:
            condition=weather[i]['weather'][0]['description']

    speech = "The forecast for " + city + " on " + new_date + " is " + condition
    return {"fulfillmentMessages": [{"text": {"text": speech}}]}

    # return { # "speech": speech, # "displayText":speech, # "source":"apiai-weather-webhook"}

if __name__=='__main__':
    port=int(os.getenv('PORT',5000))
    print("starting on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')