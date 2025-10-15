from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
import database

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class RootWidget(ScreenManager):
    pass

class SolveItApp(App):
    def build(self):
        self.title = "SolveIt"
        self.user_id = None
        return RootWidget()

    def login(self, username, password):
        username = username.strip()
        password = password.strip()
        if not username or not password:
            print("Enter both username and password")
            return

        # Check if user exists
        user = database.get_user_by_username(username)
        if user:
            user_id, stored_password = user
            if password == stored_password:
                self.user_id = user_id
                self.root.current = "home"
                self.root.get_screen("home").bind(on_enter=lambda x: self.update_questions())
            else:
                print("Wrong password!")
        else:
            # If user doesn't exist, create new
            user_id = database.add_user(username, password)
            self.user_id = user_id
            self.root.current = "home"
            self.root.get_screen("home").bind(on_enter=lambda x: self.update_questions())

    def update_questions(self, search_text=""):
        questions_list = self.root.get_screen("home").ids.questions_list
        questions_list.clear_widgets()
        questions = database.get_questions()
        for q in questions:
            q_id, title, desc, user = q
            if search_text.lower() not in title.lower() and search_text.lower() not in desc.lower():
                continue

            box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10, spacing=5)

            # white background
            with box.canvas.before:
                Color(1, 1, 1, 1)
                bg_rect = Rectangle(pos=box.pos, size=box.size)
                box.bind(pos=lambda inst, val: setattr(bg_rect, 'pos', inst.pos))
                box.bind(size=lambda inst, val: setattr(bg_rect, 'size', inst.size))

            # deep red border
            with box.canvas.after:
                Color(0.5, 0, 0, 1)
                border_rect = Rectangle(pos=box.pos, size=box.size)
                box.bind(pos=lambda inst, val: setattr(border_rect, 'pos', inst.pos))
                box.bind(size=lambda inst, val: setattr(border_rect, 'size', inst.size))

            box.add_widget(Label(text=f"{title} (by {user})", bold=True, color=(0.5, 0, 0, 1), font_size=16))
            box.add_widget(Label(text=desc, font_size=12, color=(0,0,0,1)))
            questions_list.add_widget(box)

    def add_question(self, title, desc):
        if title.strip() and self.user_id:
            database.add_question(self.user_id, title, desc)
            self.update_questions()

    def search_questions(self, text):
        self.update_questions(text)

if __name__ == "__main__":
    database.init_db()
    SolveItApp().run()
