from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import sqlite3
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton
from kivy.properties import StringProperty
import moneyFormat
from database import Database


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

                MDApp.get_running_app().root.first.ids.expense.text = str((moneyFormat.money(expenses)))
                MDApp.get_running_app().root.view_expenses.ids.overall.text = str((moneyFormat.money(expenses)))
            else:
                MDApp.get_running_app().root.first.ids.expense.text = str((moneyFormat.money(0)))
                MDApp.get_running_app().root.view_expenses.ids.overall.text = str((moneyFormat.money(0)))
        except ValueError:
            pass

# Customize Dialog
class DialogContent(MDBoxLayout):

    """Customize dialog box for user to insert their expenses"""
    # Initiliaze date to the current date
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A, %B %d, %Y'))
        self.ids.food.text_color = "skyblue"
        self.category = "food"
        
    def icon_color(self, instance):  
        self.ids.food.text_color = "gray"
        self.ids.acads.text_color = "gray"
        self.ids.transpo.text_color = "gray"
        self.ids.others.text_color = "gray"
        instance.text_color = "skyblue"

        self.category = str(instance.text)

    # Date Picker
    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)

        date_dialog.open()

    # Shows the picked date to the text label
    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts it to a user-friendly form"""

        date = value.strftime('%A, %B %d, %Y')
        self.ids.date_text.text = str(date)

    def cancel(self):
        MDApp.get_running_app().root.first.close_dialog()

    def add_task(self):
        try:
            if not self.ids.task_text.text:
                self.ids.error_message.text = "Invalid!"
            if not self.category:
                self.ids.error_message.text = "Invalid!"
            if not int(self.ids.task_text.text):
                self.ids.error_message.text = "Invalid!"

            select_expense = db.create_expenses(self.ids.task_text.text,
                                       self.ids.date_text.text,
                                       self.category)
            
            self.listed = MDApp.get_running_app().root.first.ids.container

            if select_expense[3] == 'food':
                self.icon = "food"
            elif select_expense[3] == 'acads':
                self.icon = 'school-outline'
            elif select_expense[3] == 'bus':
                self.icon = 'bus'
            else:
                self.icon = 'dots-horizontal-circle-outline'
    
            convert_money = moneyFormat.money(int(select_expense[1]))
            
            self.listed.add_widget(ListItemWithIcon(pk=select_expense[0], text=convert_money, secondary_text=select_expense[2], icon=self.icon, divider=None))

            expenses_sum = db.expenses_sum()

            MDApp.get_running_app().root.first.ids.expense.text = str(moneyFormat.money(expenses_sum))
            
            self.ids.task_text.text = ''  

            self.cancel()

        except ValueError:
            pass


class FirstWindow(Screen):

    Builder.load_file('main.kv')
    # Do not forget to initialize if you want to load a data on start of the application
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_once(self.todays_expenses)

    def todays_expenses(self, *args):
        try:
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            day_expenses = db.obtain_expenses(current_date)

            if day_expenses != []:
                expenses = int(db.expenses_sum())
                self.ids.expense.text = str((moneyFormat.money(expenses)))
                
                for task in day_expenses:
                    if task[3] == 'food':
                        self.icon = "food"
                    elif task [3] == 'acads':
                        self.icon = 'school-outline'
                    elif task [3] == 'bus':
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                    
                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = ListItemWithIcon(pk=task[0],text=convert_money, secondary_text=task[2],icon=self.icon, divider=None)

                    self.ids.container.add_widget(add_expenses)
            else:
                self.ids.expense.text = str((moneyFormat.money(0)))
        except Exception:
            pass

    def on_leave(self):
        self.ids.container.clear_widgets()
    # Opening Custom Task Dialog
    def show_task_dialog(self):
        self.task_list_dialog = MDDialog(
            title="Good Day!",
            type="custom",
            size_hint_x=0.9,
            size_hint_y=None,
            content_cls=DialogContent(),
        )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def view(self):
        self.manager.current = "view_expenses"
        self.manager.transition.direction = "up"


class ViewExpenses(Screen):
    Builder.load_file('expenses.kv') 

    def on_enter(self):
        self.ids.listexpenses.clear_widgets()

        all_expenses = db.all_data()
        try:
            if all_expenses != []:
                expenses = int(db.expenses_sum())
                self.ids.overall.text = str((moneyFormat.money(expenses)))
                for spent in all_expenses:
                    if spent[3] == 'food':
                        self.icon = "food"
                    elif spent[3] == 'acads':
                        self.icon = 'school-outline'
                    elif spent[3] == 'bus':
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                    
                    convert_money = moneyFormat.money(int(spent[1]))
                    add_expenses = ListItemWithIcon(pk=spent[0],text=convert_money, secondary_text=spent[2],icon=self.icon, divider=None)

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
                
                for task in day_expenses:
                
                    if task[3] == 'food':
                        self.icon = "food"
                    elif task [3] == 'acads':
                        self.icon = 'school-outline'
                    elif task [3] == 'bus':
                        self.icon = 'bus'
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                    
                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = ListItemWithIcon(pk=task[0],text=convert_money, secondary_text=task[2],icon=self.icon, divider=None)

                    MDApp.get_running_app().root.first.ids.container.add_widget(add_expenses)

        except Exception:
            pass

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"

class AddExpenses(Screen):
    Builder.load_file('add.kv')


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()

if __name__ == '__main__':
    rawApp().run()
