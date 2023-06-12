
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from datetime import datetime
from kivy.clock import Clock
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
import moneyFormat
from database import Database
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
db = Database()


class CustomIconLeftWidget(IconLeftWidget):
    pass


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''
    divider = None


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

    def remove_item(self, instance):
        self.parent.remove_widget(instance)


class FirstWindow(Screen):

    Builder.load_file('main.kv')
    # Do not forget to initialize if you want to load a data on start of the application

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.todays_expenses)

    def todays_expenses(self, *args):
        current_month = datetime.now().strftime('%B')
        self.ids.currentmonth.text = 'This month of ' + current_month
        try:
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            day_expenses = db.obtain_expenses(current_date)

            if day_expenses != []:
                expenses = int(db.expenses_sum())
                self.ids.expense.text = str((moneyFormat.money(expenses)))

                for task in reversed(day_expenses):
                    if task[3] == 'food':
                        self.icon = "food"
                        self.category = 'Food'
                    elif task[3] == 'acads':
                        self.icon = 'school-outline'
                        self.category = 'School'
                    elif task[3] == 'bus':
                        self.category = 'Transportation'
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                        self.category = 'Others'

                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = SwipeToDeleteItem(
                        text=self.category, secondary_text=convert_money, icon=self.icon)

                    self.ids.container.add_widget(add_expenses)
            else:
                self.ids.expense.text = str((moneyFormat.money(0)))
        except Exception:
            pass

    def on_leave(self):
        self.ids.container.clear_widgets()

    def view(self):
        self.manager.current = "view_expenses"
        self.manager.transition.direction = "up"
