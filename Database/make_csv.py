import json5
import time


def json_to_dic(filename):

    with open(filename, "r") as infile:
        data = json5.load(infile)

    print("Loaded " + filename + " as " + str(type(data)))
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    headersEvents = ["id", "room", "title", "startDate", "endDate", "chairs", "creator", "type", "categoryId", "description", "url"]
    headersPeople = ["emailHash", "fullName", "affiliation"]
    headersVenue = ["room", "location"]
    headersCateg = ["id", "name"]

    dicEvent = {}
    dicPeople = {}
    dicVenue = {}
    dicCateg = {}

    setPeople = set()
    setVenue = set()

    count = data["count"]
    for i in range(50):
        dicEvent[i+1] = {}
        for header in headersEvents:
            if (header == "id") or (header == "categoryId"):
                dicEvent[i+1][header] = int(data["results"][i].get(header, "NULL"))
            elif (header == "startDate") or (header == "endDate"):
                dateInfo = data["results"][i].get(header, "NULL")
                dicEvent[i + 1][header] = dateInfo
                if dateInfo != "NULL":
                    timestamp = dateInfo["date"] + " " + dateInfo["time"]
                    dicEvent[i+1][header] = timestamp
            elif header == "creator":
                creatorInfo = data["results"][i].get(header, "NULL")
                dicEvent[i+1][header] = creatorInfo
                if creatorInfo != "NULL":
                    dicEvent[i+1][header] = creatorInfo["fullName"]
                    personInfo = (creatorInfo["emailHash"], creatorInfo["fullName"], creatorInfo["affiliation"])
                    setPeople.add(personInfo)
            elif header == "chairs":
                chairsInfo = data["results"][i].get(header, "NULL")
                dicEvent[i+1][header] = chairsInfo
                if chairsInfo != "NULL":
                    numberChairs = len(chairsInfo)
                    nameChairs = []
                    for chair in range(numberChairs):
                        nameChairs.append(chairsInfo[chair]["fullName"])
                        personInfo = (chairsInfo[chair]["emailHash"], chairsInfo[chair]["fullName"], chairsInfo[chair]["affiliation"])
                        setPeople.add(personInfo)
                    dicEvent[i+1][header] = tuple(nameChairs)
            else:
                dicEvent[i+1][header] = data["results"][i].get(header, "NULL")
        venueInfo = (data["results"][i].get("room", "NULL"), data["results"][i].get("location", "NULL"))

    print("Created dictionary")
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print(currentTime)

    return dicEvent

def save_as_csv(dic):
    headers = ["id", "room", "title", "startDate", "endDate", "chairs", "creator", "type", "categoryId",
                     "description", "url"]

    file = open('summer_dic.csv', 'w')
    for i in range(len(dic.keys())):
        line = ""
        for header in headers:
            if header == headers[-1]: line += str(dic[i+1][header]).replace(",", "").replace("\n", "").replace("\r", "")
            else: line += str(dic[i+1][header]).replace(",", "").replace("\n", "").replace("\r", "") + ","
        print(line)
        line += "\n"
        file.write(line)
    file.close()

summerEvent = json_to_dic("dataLess.json")
save_as_csv(summerEvent)

