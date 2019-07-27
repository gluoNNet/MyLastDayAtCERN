import json5
import time


if __name__ == '__main__':

    with open("dataLess.json", "r") as infile:
        data = json5.load(infile)

    print("Loaded " + filename + " as " + type(data))
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
        print(i)
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

    print(dicEvent)
