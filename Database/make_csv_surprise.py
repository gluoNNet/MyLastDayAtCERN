import json5
import time
import os


def team_info(header, data, setPeople, setParticipants):
    info = data.get(header, "NULL")
    if info != "NULL":
        if isinstance(info, list):
            number = len(info)
            for person in range(number):
                personInfo = (info[person]["id"], info[person]["fullName"], info[person]["affiliation"], info[person]["emailHash"])
                setPeople.add(personInfo)
                setParticipants.add(info[person]["id"])
        if isinstance(info, dict):
            personInfo = (info["id"], info["fullName"], info["affiliation"], info["emailHash"])
            setPeople.add(personInfo)
            setParticipants.add(info["id"])


def json_to_dic(filename, headersEvents):

    with open(filename, "r") as infile:
        data = json5.load(infile)

    arrayRatings = []
    dicEvent = {}
    dicContributions = {}
    dicPeople = {}

    setPeople = set()

    count = data["count"]
    for i in range(count):
        dicEvent[i+1] = {}
        setParticipants = set()

        for header in headersEvents:

            if header == "eventId":
                dicEvent[i+1][header] = int(data["results"][i].get("id", "NULL"))
            elif header == "participants":

                team_info("creator", data["results"][i], setPeople, setParticipants)
                team_info("chairs", data["results"][i], setPeople, setParticipants)

            elif header == "contributions":
                contributionsInfo = data["results"][i].get(header, "NULL")
                dicEvent[i+1][header] = contributionsInfo
                dicContributions[int(data["results"][i].get("id", "NULL"))] = {}

                if contributionsInfo != "NULL":
                    numberContributions = len(contributionsInfo)
                    idContributions = []
                    for contribution in range(numberContributions):
                        idContributions.append(contributionsInfo[contribution]["id"])
                        dicContributions[int(data["results"][i].get("id", "NULL"))][contributionsInfo[contribution]["id"]] = {}

                        people = set()
                        for person in contributionsInfo[contribution]["speakers"]:
                            people.add(person["fullName"])
                        for person in contributionsInfo[contribution]["coauthors"]:
                            people.add(person["fullName"])
                        for person in contributionsInfo[contribution]["primaryauthors"]:
                            people.add(person["fullName"])

                        dicContributions[int(data["results"][i].get("id", "NULL"))][contributionsInfo[contribution]["id"]]["people"] = people
                        dicContributions[int(data["results"][i].get("id", "NULL"))][contributionsInfo[contribution]["id"]]["title"] = contributionsInfo[contribution]["title"]
                        dicContributions[int(data["results"][i].get("id", "NULL"))][contributionsInfo[contribution]["id"]]["description"] = contributionsInfo[contribution]["description"]

                        team_info("speakers", data["results"][i][header][contribution], setPeople, setParticipants)
                        team_info("primaryauthors", data["results"][i][header][contribution], setPeople, setParticipants)
                        team_info("coauthors", data["results"][i][header][contribution], setPeople, setParticipants)

                    dicEvent[i+1][header] = tuple(idContributions)

            else:
                dicEvent[i+1][header] = data["results"][i].get(header, "NULL")

        dicEvent[i+1]["participants"] = setParticipants
        for participant in setParticipants:
             arrayRatings.append([participant, int(data["results"][i].get("id", "NULL"))])

    for person in setPeople:
        dicPeople[person[0]] = [person[1], person[2], person[3]]

    return arrayRatings, dicEvent, dicContributions, dicPeople


def save_dic_as_csv(dic, headers, savename):

    file = open(savename, 'w')

    top = ""
    for header in headers:
        if header == headers[-1]:
            top += str(header).replace(",", "/").replace("\n", "").replace("\r", "")
        else:
            top += str(header).replace(",", "/").replace("\n", "").replace("\r", "") + ","
    top += "\n"
    file.write(top)

    for i in range(len(dic.keys())):
        line = ""
        for header in headers:
            if header == headers[-1]: line += str(dic[i+1][header]).replace(",", "/").replace("\n", "").replace("\r", "")
            else: line += str(dic[i+1][header]).replace(",", "/").replace("\n", "").replace("\r", "") + ","
        line += "\n"
        file.write(line)
    file.close()


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
        file.write(line)
    file.close()


headersRating = ["personId", "eventId", "rating"]
headersEvents = ["eventId", "title", "location", "participants", "type", "contributions", "description", "url"]
headersContributions = ["people", "title", "description"]  # key ["eventId"]["contributionId"]
headersPeople = ["personId"]  # content ["fullName", "affiliation", "emailHash"]

for i in range(19):
    filename = "data_{num}.json".format(num=i)

    print("Creating set {num}".format(num=i))
    print("Loaded " + filename)
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    a, b, c, d = json_to_dic(filename, headersEvents)
    # print(a)

    print("Created dictionary")
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    os.mkdir("ratings")
    os.mkdir("events")
    os.mkdir("contributions")
    os.mkdir("people")
    save_list_as_csv(a, headersRating, "ratings/ratings_{num}.csv".format(num=i))
    save_dic_as_csv(b, headersEvents, "events/events_{num}.csv".format(num=i))
    save_dic_as_csv(c, headersContributions, "contributions/contributions_{num}.csv".format(num=i))
    save_dic_as_csv(d, headersPeople, "people/people_{num}.csv".format(num=i))



