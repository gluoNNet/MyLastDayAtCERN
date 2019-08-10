import json5
import time
import os
import pickle


def team_info(header, data, setPeople, setParticipants):
    info = data.get(header, "NULL")
    if info != "NULL":
        if isinstance(info, list):
            number = len(info)
            for person in range(number):
                personInfo = (info[person]["fullName"], info[person]["affiliation"], info[person]["emailHash"])
                setPeople.add(personInfo)
                setParticipants.add(info[person]["fullName"])
        if isinstance(info, dict):
            personInfo = (info["fullName"], info["affiliation"], info["emailHash"])
            setPeople.add(personInfo)
            setParticipants.add(info["fullName"])


def json_to_dic(filename, headersEvents):

    with open(filename, "r") as infile:
        data = json5.load(infile)

    arrayRatings = []
    dicEvent = {}
    dicPeople = {}

    setPeople = set()

    count = data["count"]
    for i in range(count):
        id = str(data["results"][i].get("id"))
        dicEvent[id] = {}
        setParticipants = set()

        for header in headersEvents:

            if header == "participants":
                team_info("creator", data["results"][i], setPeople, setParticipants)
                team_info("chairs", data["results"][i], setPeople, setParticipants)

            elif header == "contributions":
                contributionsInfo = data["results"][i].get(header, "NULL")

                if contributionsInfo != "NULL":
                    numberContributions = len(contributionsInfo)
                    idContributions = []
                    for contribution in range(numberContributions):
                        idContributions.append(contributionsInfo[contribution]["id"])

                        team_info("speakers", data["results"][i][header][contribution], setPeople, setParticipants)
                        team_info("primaryauthors", data["results"][i][header][contribution], setPeople, setParticipants)
                        team_info("coauthors", data["results"][i][header][contribution], setPeople, setParticipants)

            else:
                dicEvent[id][header] = data["results"][i].get(header, "NULL")

        for participant in setParticipants:
            name = participant.replace(",", "{comma}")
            arrayRatings.append([name, id])

    for person in setPeople:
        name = person[0].replace(",", "{comma}")
        dicPeople[name] = {}
        dicPeople[name]["affiliation"] = person[1].replace(",", "{comma}")
        dicPeople[name]["emailHash"] = person[2]

    return arrayRatings, dicEvent, dicPeople


def save_list_as_csv(lis, headers, savename):

    file = open(savename, 'w')

    top = ""
    for header in headers:
        if header == headers[-1]:
            top += str(header).replace(",", "/").replace("\n", "").replace("\r", "")
        else:
            top += str(header).replace(",", "/").replace("\n", "").replace("\r", "") + ","
    top += "\n"
    file.write(top)

    for i in range(len(lis)):
        line = ""
        for item in lis[i]:
            line += str(item) + ","
        line += "1\n"

        try:
            line.encode("utf-8")
        except UnicodeEncodeError as e:
            if e.reason == 'surrogates not allowed':
                line = line.encode('utf-8', "backslashreplace").decode('utf-8')
        file.write(line)
    file.close()


headersRating = ["personId", "eventId", "rating"]
headersEvents = ["title", "location", "type", "description", "participants", "contributions"] # key ["eventId"]
headersPeople = ["personId"]  # content ["fullName", "affiliation", "emailHash"]

for i in range(0,19):
    filename = "indico_api/data_{num}.json".format(num=i)
    #filename = "indico_api/data_100.json"

    print("Creating set {num}".format(num=i))
    print("Loading " + filename)
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    a, b, c = json_to_dic(filename, headersEvents)
    #print(c)

    print("Created dictionary from .json")
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    if not os.path.exists("data_csv/ratings"): os.mkdir("data_csv/ratings")
    save_list_as_csv(a, headersRating, "data_csv/ratings/ratings_{num}.csv".format(num=i))

    if not os.path.exists("data_json/ratings"): os.mkdir("data_json/ratings")
    if not os.path.exists("data_json/events"): os.mkdir("data_json/events")
    if not os.path.exists("data_json/people"): os.mkdir("data_json/people")
    with open("data_json/ratings/ratings_{num}.json".format(num=str(i)), "wb") as outfile:
        pickle.dump(a, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data_json/events/events_{num}.json".format(num=str(i)), "wb") as outfile:
        pickle.dump(b, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data_json/people/people_{num}.json".format(num=str(i)), "wb") as outfile:
        pickle.dump(c, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    print("Saved .csv and .json files")
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)
