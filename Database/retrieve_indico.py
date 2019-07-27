import requests
import json5
import time

API_KEY = "879b1354-896f-4647-a021-86de07666f78"
SECRET_KEY = "d79d0c29-5c7d-4e8a-9efe-0b183e773854"


if __name__ == '__main__':

    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)
    #path = "https://indico.cern.ch/export/event/817571.json"
    path = "https://indico.cern.ch/categ/345.json"
    parameters = {
        "pretty": "yes",
        "onlypublic": "yes",
        "limit": 10
    }
    response = requests.get("https://indico.cern.ch/export/categ/345.json?pretty=yes&onlypublic=yes")

    data = {}
    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
    else:
        data = response.json()
        print(data["url"])

    with open("data.json", "w") as outfile:
        json5.dump(data, outfile, sort_keys=True, indent=4)

    with open("data.json", "r") as infile:
        data2 = json5.load(infile)

    print(type(data2))
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

