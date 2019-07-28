from windows.Screens import *
from ConsoleFunctions import *


class ConsoleInstance(ConsoleFunctions):

    def __init__(self):
        ConsoleFunctions.__init__(self)

        app = QApplication(sys.argv)
        self.main_screen = MainScreen("windows/main_window.ui")
        self.story_screen = StoryScreen('windows/story_window.ui')
        self.connect_signals_and_slots()
        sys.exit(app.exec_())

    def connect_signals_and_slots(self):
        self.main_screen.submit_id.connect(self.calculate_recommendations)
        self.main_screen.open_story.connect(self.story_screen.open_window)
        self.story_screen.story_finish.connect(self.main_screen.set_story_false)
        self.finished_calculating.connect(self.start_story)

    @Slot()
    def start_story(self):
        self.story_screen.storyText = self.storyText
        self.story_screen.set_story_start()


if __name__ == '__main__':
    ConsoleInstance()
