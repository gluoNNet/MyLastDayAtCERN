from PySide2.QtCore import QObject, Signal, Slot

import pickle
import csv


class ConsoleFunctions(QObject):
    """Game functions"""

    finished_calculating = Signal()

    def __init__(self, parent=None):
        super(ConsoleFunctions, self).__init__(parent)
        self.dicPeople = {}
        self.dicEvents = {}
        self.lisRatings = {}

        self.id = ""
        self.recommendations = ["", "", "", "", "", ""]
        self.storyText = ["", "", "", "", "", ""]

        self.import_files()

    def import_files(self):
        with open("data/people_all.json", "rb") as f:
            self.dicPeople.update(pickle.load(f))
        f.close()

        with open("data/events_all.json", "rb") as f:
            self.dicEvents.update(pickle.load(f))
        f.close()

        with open('data/ratings_all.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                name = row[0]
                event = row[1]
                self.lisRatings.append([name, event])

    @Slot(str)
    def calculate_recommendations(self, id):
        print("Calculate recommendations with id: {}".format(id))

        self.recommendations[0] = "Prof Famous"
        self.recommendations[1] = "Event Joy"
        self.recommendations[2] = "Table Colleagues"
        self.recommendations[3] = "Bar Stranger"
        self.recommendations[4] = "Best Friend"
        self.recommendations[5] = "Mysterioso"

        self.create_story()
        self.finished_calculating.emit()

    def create_story(self):
        self.storyText[0] = "You entered the cocktail party and met " + self.recommendations[0] + " with awe!"
        self.storyText[1] = "Then you walked right into your favorite " + self.recommendations[1] + "."
        self.storyText[2] = "In the corner was " + self.recommendations[2] + " waving at you cheerfully."
        self.storyText[3] = "You took a risk and went to talk with " + self.recommendations[3] + "."
        self.storyText[4] = "Of course, you cannot miss chatting with " + self.recommendations[4] + "."
        self.storyText[5] = "Finally, a surprise " + self.recommendations[5] + " appeared from nowhere!"
