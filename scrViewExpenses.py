
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
import moneyFormat
from database import Database
from kivy.properties import StringProperty
from kivymd.app import MDApp

db = Database()


class CustomIconLeftWidget(IconLeftWidget):
    pass


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''

    icon = StringProperty()

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)

        db.delete_expense(the_list_item.pk)

        try:
            length = db.all_data()
            if length != []:

                expenses = int(db.expenses_sum())

                MDApp.get_running_app().root.first.ids.expense.text = str(
                    (moneyFormat.money(expenses)))
                MDApp.get_running_app().root.view_expenses.ids.overall.text = str(
                    (moneyFormat.money(expenses)))
            else:
                MDApp.get_running_app().root.first.ids.expense.text = str((moneyFormat.money(0)))
                MDApp.get_running_app().root.view_expenses.ids.overall.text = str(
                    (moneyFormat.money(0)))
        except ValueError:
            pass


class ViewExpenses(Screen):
    Builder.load_file('viewexpense.kv')

    def on_enter(self):
        self.ids.listexpenses.clear_widgets()

        all_expenses = db.all_data()
        try:
            if all_expenses != []:
                expenses = int(db.expenses_sum())
                self.ids.overall.text = str((moneyFormat.money(expenses)))
                for spent in reversed(all_expenses):
                    if spent[3] == 'food':
                        self.icon = "food"
                    elif spent[3] == 'acads':
                        self.icon = 'school-outline'
                    elif spent[3] == 'bus':
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'

                    convert_money = moneyFormat.money(int(spent[1]))
                    add_expenses = ListItemWithIcon(
                        pk=spent[0], text=convert_money, secondary_text=spent[2], icon=self.icon, divider=None)

                    self.ids.listexpenses.add_widget(add_expenses)
            else:
                self.ids.overall.text = str((moneyFormat.money(0)))
        except Exception:
            pass

    def on_leave(self):
        MDApp.get_running_app().root.first.ids.container.clear_widgets()
        self.ids.listexpenses.clear_widgets()

        try:
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            day_expenses = db.obtain_expenses(current_date)

            if day_expenses != []:

                for task in reversed(day_expenses):

                    if task[3] == 'food':
                        self.icon = "food"
                    elif task[3] == 'acads':
                        self.icon = 'school-outline'
                    elif task[3] == 'bus':
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'

                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = ListItemWithIcon(
                        pk=task[0], text=convert_money, secondary_text=task[2], icon=self.icon, divider=None)

                    MDApp.get_running_app().root.first.ids.container.add_widget(add_expenses)

        except Exception:
            pass

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"
