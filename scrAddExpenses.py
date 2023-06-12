from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem
import moneyFormat
from database import Database
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
db = Database()


class CustomMDBoxLayout(MDBoxLayout):
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


class ApproveExpense(MDBoxLayout):
    pass


class AddExpenses(Screen):
    Builder.load_file('addexpense.kv')

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"

    def on_kv_post(self, base_widget):
        self.ids.food.text_color = [253/255, 60/255, 74/255, 1]
        self.category = "food"

        return super().on_kv_post(base_widget)

    def on_leave(self):
        MDApp.get_running_app().root.first.ids.container.clear_widgets()
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

    def icon_color(self, instance):
        self.ids.food.text_color = "gray"
        self.ids.acads.text_color = "gray"
        self.ids.transpo.text_color = "gray"
        self.ids.others.text_color = "gray"
        instance.text_color = [253/255, 60/255, 74/255, 1]

        self.category = str(instance.text)

    def add_task(self):

        date = str(datetime.now().strftime('%A, %B %d, %Y'))

        try:
            price = float(self.ids.price.text)

            select_expense = db.create_expenses(price,
                                                date,
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

            self.listed.add_widget(ListItemWithIcon(
                pk=select_expense[0], text=convert_money, secondary_text=select_expense[2], icon=self.icon, divider=None))

            expenses_sum = db.expenses_sum()

            MDApp.get_running_app().root.first.ids.expense.text = str(
                moneyFormat.money(expenses_sum))

            self.ids.price.text = ''
            self.input_added()
        except:
            self.invalid_input()

    def invalid_input(self):
        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            text='[color=#000000]There was an error processing your data. Please make sure to fill in all the required information correctly before proceeding to the next step. We appreciate your cooperation in ensuring a smooth experience. Thank you![/color]',
            size_hint=(0.85, None),
            radius=[20, 7, 20, 7],
            buttons=[close_button],
            auto_dismiss=False
        )
        self.dialog.open()

    def input_added(self):
        self.dialog = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            radius=[20, 20, 20, 20],
            content_cls=ApproveExpense()
        )
        self.dialog.open()
        self.ids.price.text = '0'
        # Schedule the dialog dismissal after 3 seconds
        Clock.schedule_once(lambda dt: self.dialog.dismiss(), 3)
    # Close operation

    def close_dialog(self, *args):
        self.dialog.dismiss()
