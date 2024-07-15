from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from datetime import datetime

class Task:
    def __init__(self, title="", description="", priority="", due_date=""):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

class ToDoListApp(App):
    def build(self):
        self.tasks = []

        main_layout = BoxLayout(orientation='vertical')

        self.task_list_layout = StackLayout(size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll_view.add_widget(self.task_list_layout)

        main_layout.add_widget(self.scroll_view)

        add_task_button = Button(text='Add Task', size_hint_y=None, height=50)
        add_task_button.bind(on_release=self.show_add_task_popup)
        main_layout.add_widget(add_task_button)

        return main_layout

    def show_add_task_popup(self, instance):
        content = BoxLayout(orientation='vertical')

        title_input = TextInput(hint_text='Title')
        content.add_widget(title_input)

        description_input = TextInput(hint_text='Description')
        content.add_widget(description_input)

        priority_spinner = Spinner(
            text='Priority',
            values=('Low', 'Medium', 'High'),
        )
        content.add_widget(priority_spinner)

        due_date_button = Button(text='Select Due Date')
        due_date_button.bind(on_release=lambda x: self.show_date_picker(due_date_button))
        content.add_widget(due_date_button)

        save_button = Button(text='Save', size_hint_y=None, height=50)
        save_button.bind(on_release=lambda x: self.add_task(title_input.text, description_input.text, priority_spinner.text, due_date_button.text))
        content.add_widget(save_button)

        self.add_task_popup = Popup(title='Add Task', content=content, size_hint=(0.8, 0.8))
        self.add_task_popup.open()

    def show_date_picker(self, button):
        content = BoxLayout(orientation='vertical')

        # Year picker
        year_spinner = Spinner(text='Year', values=[str(i) for i in range(2020, 2031)])
        content.add_widget(year_spinner)

        # Month picker
        month_spinner = Spinner(text='Month', values=[str(i).zfill(2) for i in range(1, 13)])
        content.add_widget(month_spinner)

        # Day picker
        day_spinner = Spinner(text='Day', values=[str(i).zfill(2) for i in range(1, 32)])
        content.add_widget(day_spinner)

        # Hour picker
        hour_spinner = Spinner(text='Hour', values=[str(i).zfill(2) for i in range(0, 24)])
        content.add_widget(hour_spinner)

        # Minute picker
        minute_spinner = Spinner(text='Minute', values=[str(i).zfill(2) for i in range(0, 60)])
        content.add_widget(minute_spinner)

        save_button = Button(text='Save', size_hint_y=None, height=50)
        save_button.bind(on_release=lambda x: self.set_due_date(button, year_spinner.text, month_spinner.text, day_spinner.text, hour_spinner.text, minute_spinner.text))
        content.add_widget(save_button)

        self.date_picker_popup = Popup(title='Select Due Date and Time', content=content, size_hint=(0.8, 0.8))
        self.date_picker_popup.open()

    def set_due_date(self, button, year, month, day, hour, minute):
        try:
            due_date = datetime.strptime(f"{year}-{month}-{day} {hour}:{minute}", '%Y-%m-%d %H:%M')
            button.text = due_date.strftime('%Y-%m-%d %H:%M')
            self.date_picker_popup.dismiss()
        except ValueError as e:
            button.text = 'Invalid Date/Time'
            print(f"Error: {e}")
            print(f"Provided Date: {year}-{month}-{day}, Provided Time: {hour}:{minute}")

    def add_task(self, title, description, priority, due_date):
        if not title or not description or priority == 'Priority' or due_date == 'Select Due Date':
            print("Invalid task details. Task not added.")
            return  # Basic validation failed

        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.update_task_list()
        self.add_task_popup.dismiss()  # Ensure popup dismissal after adding task

        print(f"Task added: {task.title} - {task.description} - {task.priority} - {task.due_date}")

    def update_task_list(self):
        self.task_list_layout.clear_widgets()

        for task in self.tasks:
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

            checkbox = CheckBox(active=task.completed)
            checkbox.bind(active=lambda checkbox, value, task=task: self.mark_task_completed(task, value))
            task_box.add_widget(checkbox)

            task_label = Label(text=f"{task.title} - {task.description} - {task.priority} - {task.due_date}")
            task_box.add_widget(task_label)

            edit_button = Button(text='Edit')
            edit_button.bind(on_release=lambda x, task=task: self.show_edit_task_popup(task))
            task_box.add_widget(edit_button)

            delete_button = Button(text='Delete')
            delete_button.bind(on_release=lambda x, task=task: self.delete_task(task))
            task_box.add_widget(delete_button)

            self.task_list_layout.add_widget(task_box)

    def mark_task_completed(self, task, value):
        task.completed = value
        print("Task '{task.title}' marked as {'completed' if value else 'active'}.")
        
    def show_edit_task_popup(self, task):
        content = BoxLayout(orientation='vertical')

        title_input = TextInput(text=task.title)
        content.add_widget(title_input)

        description_input = TextInput(text=task.description)
        content.add_widget(description_input)

        priority_spinner = Spinner(
            text=task.priority,
            values=('Low', 'Medium', 'High'),
        )
        content.add_widget(priority_spinner)

        due_date_button = Button(text=task.due_date)
        due_date_button.bind(on_release=lambda x: self.show_date_picker(due_date_button))
        content.add_widget(due_date_button)

        save_button = Button(text='Save', size_hint_y=None, height=50)
        save_button.bind(on_release=lambda x: self.edit_task(task, title_input.text, description_input.text, priority_spinner.text, due_date_button.text))
        content.add_widget(save_button)

        self.edit_task_popup = Popup(title='Edit Task', content=content, size_hint=(0.8, 0.8))
        self.edit_task_popup.open()

    def edit_task(self, task, title, description, priority, due_date):
        if not title or not description or priority == 'Priority' or due_date == 'Select Due Date':
            print("Invalid task details. Task not edited.")
            return  # Basic validation

        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        self.update_task_list()
        self.edit_task_popup.dismiss()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.update_task_list()

    def dismiss_popup(self):
        for widget in self.root_window.children:
            if isinstance(widget, Popup):
                widget.dismiss()

if __name__ == '__main__':
    ToDoListApp().run()
