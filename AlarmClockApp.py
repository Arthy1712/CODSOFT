import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.filechooser import FileChooserListView


class Alarm:
    def __init__(self, time, tone, active=True):
        self.time = time
        self.tone = tone
        self.active = active


class AlarmClockApp(App):
    def build(self):
        self.alarms = []
        self.current_alarm = None

        self.root = BoxLayout(orientation='vertical')
        self.time_label = Label(text=self.get_time(), font_size='48sp')
        self.date_label = Label(text=self.get_date(), font_size='24sp')

        self.root.add_widget(self.time_label)
        self.root.add_widget(self.date_label)

        set_alarm_button = Button(text='Set New Alarm', size_hint=(1, 0.1))
        set_alarm_button.bind(on_press=self.show_alarm_popup)
        self.root.add_widget(set_alarm_button)

        self.alarm_list = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        self.root.add_widget(self.alarm_list)

        Clock.schedule_interval(self.update_time, 1)
        return self.root

    def get_time(self):
        return datetime.now().strftime('%H:%M:%S')

    def get_date(self):
        return datetime.now().strftime('%A, %B %d, %Y')

    def update_time(self, dt):
        self.time_label.text = self.get_time()
        self.date_label.text = self.get_date()
        self.check_alarms()

    def show_alarm_popup(self, instance):
        content = FloatLayout()

        self.hour_spinner = Spinner(
            text='Hour',
            values=[str(i) for i in range(24)],
            size_hint=(0.3, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6}
        )
        content.add_widget(self.hour_spinner)

        self.minute_spinner = Spinner(
            text='Minute',
            values=[str(i) for i in range(60)],
            size_hint=(0.3, 0.1),
            pos_hint={'x': 0.4, 'y': 0.6}
        )
        content.add_widget(self.minute_spinner)

        self.second_spinner = Spinner(
            text='Second',
            values=[str(i) for i in range(60)],
            size_hint=(0.3, 0.1),
            pos_hint={'x': 0.7, 'y': 0.6}
        )
        content.add_widget(self.second_spinner)

        choose_tone_button = Button(text='Choose Alarm Tone', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'y': 0.4})
        choose_tone_button.bind(on_press=self.show_tone_chooser)
        content.add_widget(choose_tone_button)

        set_button = Button(text='Set Alarm', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'y': 0.2})
        set_button.bind(on_press=self.set_alarm)
        content.add_widget(set_button)

        cancel_button = Button(text='Cancel', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'y': 0.1})
        cancel_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(cancel_button)

        self.popup = Popup(title='Set New Alarm', content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def show_tone_chooser(self, instance):
        content = FileChooserListView(filters=['*.mp3', '*.wav'], size_hint=(1, 1))
        content.bind(on_submit=self.select_tone)

        self.tone_popup = Popup(title='Choose Alarm Tone', content=content, size_hint=(0.8, 0.8))
        self.tone_popup.open()

    def select_tone(self, chooser, selection, touch):
        if selection:
            self.selected_tone = selection[0]
            self.tone_popup.dismiss()

    def set_alarm(self, instance):
        hour = self.hour_spinner.text
        minute = self.minute_spinner.text
        second = self.second_spinner.text
        time_str = f"{hour}:{minute}:{second}"

        if hasattr(self, 'selected_tone'):
            alarm = Alarm(time=time_str, tone=self.selected_tone)
            self.alarms.append(alarm)
            self.add_alarm_to_list(alarm)
            self.popup.dismiss()

    def add_alarm_to_list(self, alarm):
        alarm_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        alarm_label = Label(text=alarm.time)
        alarm_layout.add_widget(alarm_label)

        alarm_toggle = Switch(active=alarm.active)
        alarm_toggle.bind(active=lambda instance, value: self.toggle_alarm(alarm, value))
        alarm_layout.add_widget(alarm_toggle)

        self.alarm_list.add_widget(alarm_layout)

    def toggle_alarm(self, alarm, value):
        alarm.active = value

    def check_alarms(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        for alarm in self.alarms:
            if alarm.active and alarm.time == current_time:
                self.trigger_alarm(alarm)

    def trigger_alarm(self, alarm):
        self.current_alarm = alarm
        content = BoxLayout(orientation='vertical')

        dismiss_button = Button(text='Dismiss', size_hint_y=0.2)
        dismiss_button.bind(on_press=self.dismiss_alarm)
        content.add_widget(dismiss_button)

        snooze_button = Button(text='Snooze', size_hint_y=0.2)
        snooze_button.bind(on_press=self.snooze_alarm)
        content.add_widget(snooze_button)

        self.alarm_popup = Popup(title='Alarm Ringing!', content=content, size_hint=(0.8, 0.8))
        self.alarm_popup.open()

        self.sound = SoundLoader.load(alarm.tone)
        if self.sound:
            self.sound.play()

    def dismiss_alarm(self, instance):
        self.alarm_popup.dismiss()
        if self.sound:
            self.sound.stop()

    def snooze_alarm(self, instance):
        self.alarm_popup.dismiss()
        if self.sound:
            self.sound.stop()

        snooze_time = (datetime.now() + timedelta(minutes=10)).strftime('%H:%M:%S')
        self.current_alarm.time = snooze_time
        self.current_alarm.active = True


if __name__ == '__main__':
    AlarmClockApp().run()
