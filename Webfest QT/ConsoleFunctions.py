from PySide2.QtCore import QObject, Signal, Slot

import pickle
import csv

#import network


class ConsoleFunctions(QObject):

    finished_calculating = Signal()

    def __init__(self, full, parent=None):
        super(ConsoleFunctions, self).__init__(parent)
        self.dicPeople = {}
        self.dicEvents = {}
        self.lisAttendance = {}

        self.id = ""
        self.recommendations = ["", "", "", "", "", ""]
        self.storyText = ["", "", "", "", "", "", ""]

        print(full)
        #self.import_files(full)

    def import_files(self, full):
        state = "all" if full  else "18"

        with open("data/people_{}.json".format(state), "rb") as f:
            self.dicPeople.update(pickle.load(f))

        with open("data/events_{}.json".format(state), "rb") as f:
            self.dicEvents.update(pickle.load(f))

        with open('data/attendance_{}.csv'.format(state)) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row == ["personId", "eventId", "rating"]: continue
                name = row[0]
                event = row[1]
                self.lisAttendance.append([name, event])

    @Slot(str)
    def calculate_recommendations(self, id):
        print("Calculate recommendations with id: {}".format(id))
        databaseName = id.replace(",", "{comma}")

        # backend network calculations
        # returns recommendation array
        #network.network_calculation("/Users/williamyam/PycharmProjects/CERNwebfest/old/sample network/descriptions/descriptions_18.csv")

        self.recommendations[0] = "Prof Famous"
        self.recommendations[1] = "Event Joy"
        self.recommendations[2] = "Table Colleagues"
        self.recommendations[3] = "Bar Stranger"
        self.recommendations[4] = "Best Friend"
        self.recommendations[5] = "Mysterioso"

        self.create_story()
        self.finished_calculating.emit()

    def create_story(self):
        self.storyText[0] = "Calculating... Your perfect day"
        self.storyText[1] = "Don't forget to attend an interesting lecture"  # "You entered the cocktail party and met " + self.recommendations[0] + " with awe!"
        self.storyText[2] = "It's exciting to explore in a workshop"  # "Then you walked right into your favorite " + self.recommendations[1] + "."
        self.storyText[3] = "Contribute your time to a webfest hackathon"  # In the corner was " + self.recommendations[2] + " waving at you cheerfully."
        self.storyText[4] = "In the summer student drink, your friends are waving at you cheerfully."  # "You took a risk and went to talk with " + self.recommendations[3] + "."
        self.storyText[5] = "Of course, you cannot miss visiting CMS"  # "Of course, you cannot miss chatting with " + self.recommendations[4] + "."
        self.storyText[6] = "Finally, a surprise, summer student photo appeared from nowhere!"  # "Finally, a surprise " + self.recommendations[5] + " appeared from nowhere!"
