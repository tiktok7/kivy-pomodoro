import kivy
kivy.require("1.10.0")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from plyer import notification

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Config.set('graphics', 'minimum_width', '150')
Config.set('graphics', 'minimum_height', '100')
Config.set('kivy', 'window_icon', 'resources/tomato_icon2.png')
Config.set('kivy', 'exit_on_escape', 1)

bell_sound = SoundLoader.load("resources/Ship_Bell-Mike_Koenig-1911209136.wav")


class PomodoroUI(Widget):
    time_str = StringProperty("00:00")
    remaining_sec = NumericProperty(0)

    def __init__(self):
        super().__init__()
        self.event = None
        self.pomodoro_length = int(25 * 60)
        self.break_length = int(5 * 60)
        self.remaining_sec = self.pomodoro_length
        self.app = App.get_running_app()

    def on_timer_start(self):
        self.on_timer_stop()
        self.start_timer(self.pomodoro_length)

    def on_break_start(self):
        self.on_timer_stop()
        self.start_timer(self.break_length)

    def start_timer(self, duration_sec):
        self.remaining_sec = duration_sec
        self.event = Clock.schedule_interval(self.text_update, 1)

    def on_timer_stop(self):
        self.remaining_sec = self.pomodoro_length
        if self.event:
            self.event.cancel()

    def text_update(self, dt):
        self.remaining_sec -= 1
        if not self.remaining_sec:
            bell_sound.play()
            self.on_timer_stop()
            kwargs = {
                'title': "title",
                'message': "timer stopped",
                'ticker': "Pomodoro!"
            }
            self.app.notify(kwargs)
            return

    def on_remaining_sec(self, *args):
        minutes = int(self.remaining_sec // 60)
        seconds = int(self.remaining_sec % 60)
        self.time_str = f"{minutes:02}:{seconds:02}"


class PomodoroApp(App):
    def build(self):
        print(self.get_application_icon())
        return PomodoroUI()

    def notify(self, kwargs):
        # kwargs['app_icon'] = join(dirname(realpath(__file__)),
        #                                   'plyer-icon.ico')
        kwargs['timeout'] = 15
        notification.notify(**kwargs)


if __name__ == '__main__':
    PomodoroApp().run()
