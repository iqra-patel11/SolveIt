from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label  # <-- needed for Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import database  # import database.py

# Root widget
class RootWidget(BoxLayout):
    pass

class SolveItApp(App):
    def build(self):
        self.title = "SolveIt"
        return RootWidget()  # link root widget

    def on_start(self):
        self.update_questions()

    def update_questions(self):
        questions_list = self.root.ids.questions_list
        questions_list.clear_widgets()
        questions = database.get_questions()
        for q in questions:
            q_id, title, desc = q
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
            box.add_widget(Label(text=title, bold=True))
            box.add_widget(Label(text=desc, font_size=12))
            questions_list.add_widget(box)

    def add_question(self):
        title_input = self.root.ids.question_title
        desc_input = self.root.ids.question_desc
        title = title_input.text.strip()
        desc = desc_input.text.strip()

        if title:
            database.add_question(title, desc)
            title_input.text = ""
            desc_input.text = ""
            self.update_questions()


if __name__ == "__main__":
    database.init_db()
    SolveItApp().run()
