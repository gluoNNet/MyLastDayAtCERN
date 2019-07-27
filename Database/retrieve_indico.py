import requests
import json5
import time
import os

API_KEY = "879b1354-896f-4647-a021-86de07666f78"
SECRET_KEY = "d79d0c29-5c7d-4e8a-9efe-0b183e773854"


if __name__ == '__main__':

    for i in range(19):
        print("Loop batch " + str(i))
        t = time.localtime()
        currentTime = time.strftime("%H:%M:%S", t)
        print(currentTime)

        # path = "https://indico.cern.ch/export/event/817571.json"
        # path = "https://indico.cern.ch/exprot/categ/345.json"
        path = "https://indico.cern.ch/export/categ/6725.json"
        parameters = {
            "pretty": "yes",
            "onlypublic": "yes",
            "detail": "contributions",
            "limit": 100,
            "offset": 100*i
        }
        response = requests.get(path, parameters)

        data = {}
        if response.status_code != 200:
            print('Failed to get data:', response.status_code)
        else:
            data = response.json()
            print(data["url"])

        os.mkdir("data_json")
        with open("data_json/data_{num}.json".format(num=str(i)), "w") as outfile:
            json5.dump(data, outfile, sort_keys=True, indent=4)

        print("Saved " + str(type(data)))
        t = time.localtime()
        currentTime = time.strftime("%H:%M:%S", t)
        print(currentTime)

