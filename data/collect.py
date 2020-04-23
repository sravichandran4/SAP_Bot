import requests
import json

def get_global():
    #URL = "https://pkgstore.datahub.io/core/covid-19/worldwide-aggregated_json/data/c43a5b5958c15e7277c3cfe727159b28/worldwide-aggregated_json.json"
    URL = "https://datahub.io/core/covid-19/r/worldwide-aggregated.json"
    r = requests.get(url = URL)
    data = r.json()
    with open("global.json", 'w') as json_file:
        json.dump(data, json_file)
    return 0

def get_by_country():
    URL = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(url = URL)
    data = r.json()
    with open("timeseries.json", 'w') as json_file:
        json.dump(data, json_file)
    return 0

def show_by_country(country):
    data = {}
    with open("timeseries.json") as f:
        data = json.load(f)
        for key,val in data.items():
            print(key)

if __name__ == '__main__':
    get_global()
    get_by_country()
    #show_by_country("US")
