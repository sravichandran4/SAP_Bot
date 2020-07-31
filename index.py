from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import datetime

app = Flask(__name__)

def get_current_count():
    data = {}
    URL = "https://corona.lmao.ninja/v2/all"
    r = requests.get(url = URL)
    data = r.json()
    latest = {}
    latest['date'] = datetime.datetime.fromtimestamp((data['updated'] / 1000.0)).strftime('%c')
    latest['confirmed'] = data['cases']
    latest['deaths'] = data['deaths']
    latest['recovered'] = data['recovered']
    return latest

@app.route('/')
def index():
    data = {}
    current = {}
    daybefore = {}
    confirmed = {}
    deaths = {}
    recovered = {}
    latest = get_current_count()
    with open('data/global.json') as f:
        d = json.load(f)
        current = d[-1]
        daybefore = d[-2]
    #
    confirmed['total'] = current['Confirmed']
    deaths['total'] = current['Deaths']
    recovered['total'] = current['Recovered']

    #
    compare_confirmed = int(current['Confirmed']) - int(daybefore['Confirmed'])
    compare_deaths = int(current['Deaths']) - int(daybefore['Deaths'])
    compare_recovered = int(current['Recovered']) - int(daybefore['Recovered'])
    if compare_confirmed > 0:
        confirmed['status'] = "increased"
    else:
        confirmed['status'] = "decreased"
    if compare_deaths > 0:
        deaths['status'] = "increased"
    else:
        deaths['status'] = "decreased"
    if compare_recovered > 0:
        recovered['status'] = "increased"
    else:
        recovered['status'] = "decreased"
    confirmed['diffence'] = str(compare_confirmed).replace("-","")
    deaths['diffence'] = str(compare_deaths).replace("-","")
    recovered['diffence'] = str(compare_recovered).replace("-","")
    data['confirmed'] = confirmed
    data['deaths'] = deaths
    data['recovered'] = recovered
    data['date'] = current['Date']

    dates = []
    cases = []
    deaths = []
    recovered = []
    totallen = len(d)
    for entry in d[-15:]:
        dates.append((entry['Date'].split('-'))[-1])
        cases.append(entry['Confirmed'])
        deaths.append(entry['Deaths'])
        recovered.append(entry['Recovered'])


    country = {}
    with open("data/timeseries.json") as f:
        countrydata = json.load(f)
    country["US"] = countrydata["US"][-1]
    country["Spain"] = countrydata["Spain"][-1]
    country["Italy"] = countrydata["Italy"][-1]
    country["France"] = countrydata["France"][-1]
    country["Germany"] = countrydata["Germany"][-1]
    country["UK"] = countrydata["United Kingdom"][-1]
    country["China"] = countrydata["China"][-1]
    country["Turkey"] = countrydata["Turkey"][-1]
    country["Iran"] = countrydata["Iran"][-1]
    country["Belgium"] = countrydata["Belgium"][-1]
    country["India"] = countrydata["India"][-1]

    casesmax=int(max(cases) * 1.1)
    deathsmax=int(max(deaths) * 1.1)
    recoveredmax=int(max(recovered) * 1.1)

    globaltable = []
    globaltabledates = []
    for key,vals in countrydata.items():
        coun = {}
        coun['country'] = key
        coun['data'] = vals[-7:]
        if coun['country'] == "Afghanistan":
            for e in coun['data']:
                globaltabledates.append(e['date'])
        globaltable.append(coun)


    return render_template(
        "home.html",
        latest=latest,
        casesmax=casesmax,
        deathsmax=deathsmax,
        recoveredmax=recoveredmax,
        data=data,
        dates=dates,
        cases=cases,
        deaths=deaths,
        recovered=recovered,
        country=country,
        globaltable=globaltable,
        globaltabledates=globaltabledates
    )
    #return render_template('index.html')


@app.route('/country/<c>')
def country(c):
    country = {}
    data = {}
    current = {}
    daybefore = {}
    confirmed = {}
    deaths = {}
    recovered = {}

    with open("data/timeseries.json") as f:
        countrydata = json.load(f)

        if c == "UK":
            countryname = "United Kingdom"
        else:
            countryname = c
        ############################
        current = countrydata[countryname][-1]
        daybefore = countrydata[countryname][-2]

        confirmed['total'] = current['confirmed']
        deaths['total'] = current['deaths']
        recovered['total'] = current['recovered']
        #
        compare_confirmed = int(current['confirmed']) - int(daybefore['confirmed'])
        compare_deaths = int(current['deaths']) - int(daybefore['deaths'])
        compare_recovered = int(current['recovered']) - int(daybefore['recovered'])

        if compare_confirmed > 0:
            confirmed['status'] = "increased"
        else:
            confirmed['status'] = "decreased"
        if compare_deaths > 0:
            deaths['status'] = "increased"
        else:
            deaths['status'] = "decreased"
        if compare_recovered > 0:
            recovered['status'] = "increased"
        else:
            recovered['status'] = "decreased"

        confirmed['diffence'] = str(compare_confirmed).replace("-","")
        deaths['diffence'] = str(compare_deaths).replace("-","")
        recovered['diffence'] = str(compare_recovered).replace("-","")

        data['confirmed'] = confirmed
        data['deaths'] = deaths
        data['recovered'] = recovered


        ############################
        dates = []
        cases = []
        deaths = []
        recovered = []
        tabledata = []
        for cont in countrydata[countryname][-10:]:
            tabledata.append(cont)
            dates.append((cont['date'].split('-'))[-1])
            #dates.append(cont['date'])
            cases.append(cont['confirmed'])
            deaths.append(cont['deaths'])
            recovered.append(cont['recovered'])

        ############################

        casesmax=int(max(cases) * 1.1)
        deathsmax=int(max(deaths) * 1.1)
        recoveredmax=int(max(recovered) * 1.1)

        tabledatafinal = tabledata[::-1]

        cc = "_United Nations"
        if countryname == "US":
            cc = "us"
        elif countryname == "Spain":
            cc = "es"
        elif countryname == "Italy":
            cc = "it"
        elif countryname == "France":
            cc = "fr"
        elif countryname == "Germany":
            cc = "de"
        elif countryname == "United Kingdom":
            cc = "gb"
        elif countryname == "China":
            cc = "cn"
        elif countryname == "Turkey":
            cc = "tr"
        elif countryname == "Iran":
            cc = "ir"
        elif countryname == "Belgium":
            cc = "be"
        elif countryname == "India":
            cc = "in"
        else:
            cc = "_United Nations"

        ############################
    return render_template(
        "country.html",
        casesmax=casesmax,
        deathsmax=deathsmax,
        recoveredmax=recoveredmax,
        data=data,
        dates=dates,
        cases=cases,
        deaths=deaths,
        recovered=recovered,
        tabledata=tabledatafinal,
        country=countryname,
        cc=cc
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run( host='0.0.0.0', debug=True )
