import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTextBrowser, QLabel
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QPixmap


class MainScreen(QObject):

    submit_id = Signal(str)
    open_story = Signal()

    def __init__(self, ui_file, parent=None):
        super(MainScreen, self).__init__(parent)

        self.window = QUiLoader().load(ui_file)
        self.extract_items()
        self.connect_signals()
        self.inStory = False

        image = QPixmap("images/main.jpg")
        self.base_image.setPixmap(image)

        self.window.show()

    def extract_items(self):
        self.submit_button = self.window.findChild(QPushButton, "submit_button")
        self.input_line = self.window.findChild(QLineEdit, "input_line")
        self.base_image = self.window.findChild(QLabel, "base_image")

    def connect_signals(self):
        self.submit_button.clicked.connect(self.submit_id_number)
        self.submit_button.clicked.connect(self.input_line.clear)

    def open_window(self):
        self.window.show()

    def close_window(self):
        self.window.hide()

    @Slot()
    def set_story_false(self):
        self.inStory = False
        self.window.show()

    def submit_id_number(self):
        if self.inStory:
            return
        id = self.input_line.text()
        self.submit_id.emit(id)
        self.open_story.emit()
        self.inStory = True
        self.window.hide()


class StoryScreen(QObject):

    story_finish = Signal()

    def __init__(self, ui_file, parent=None):
        super(StoryScreen, self).__init__(parent)
        self.window = QUiLoader().load(ui_file)

        self.extract_items()
        self.connect_signals()
        self.scene = 0
        self.storyText = []
        self.storyBegin = False

        image = QPixmap("images/cern_color.jpg")
        self.bottom_image.setPixmap(image)

        self.window.hide()

    def extract_items(self):
        self.next_button = self.window.findChild(QPushButton, "next_button")
        self.story_box = self.window.findChild(QTextBrowser, "story_box")
        self.story_image = self.window.findChild(QLabel, "story_image")
        self.bottom_image = self.window.findChild(QLabel, "bottom_image")

    def connect_signals(self):
        self.next_button.clicked.connect(self.go_next_screen)

    @Slot()
    def open_window(self):
        self.window.show()

    @Slot()
    def close_window(self):
        self.window.hide()

    def set_story_start(self):
        self.storyBegin = True
        self.scene += 1
        self.update_screen()

    def go_next_screen(self):
        if not self.storyBegin:
            return
        if self.scene == 6:
            self.window.hide()
            self.scene = 0
            self.update_screen()
            self.storyBegin = False
            self.story_finish.emit()
        else:
            self.scene += 1
            self.update_screen()

    def update_screen(self):
        self.story_box.setText(self.storyText[self.scene])

        image = QPixmap("images/image_{}.jpg".format(self.scene))
        self.story_image.setPixmap(image)
