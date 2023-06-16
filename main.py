
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

from kivy.lang import Builder
from datetime import datetime
from kivy.clock import Clock
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
import moneyFormat
from database import Database
from kivy.properties import StringProperty, ColorProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe

db = Database()


class ApproveExpense(MDBoxLayout):
    pass


class DeniedExpense(MDBoxLayout):
    pass


class CustomMDBoxLayout(MDBoxLayout):
    pass


class CustomIconLeftWidget(IconLeftWidget):
    pass


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''
    divider = None


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    md_bg_color = ColorProperty()
    icon_color = ColorProperty()

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def remove_item(self, instance):
        self.parent.remove_widget(instance)

        db.delete_expense(instance.pk)

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
                        self.identity = 'Food'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (253/255, 60/255, 74/255, 1)
                    elif task[3] == 'acads':
                        self.icon = 'school-outline'
                        self.identity = 'School'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (252/255, 172/255, 18/255, 1)
                    elif task[3] == 'bus':
                        self.identity = 'Transportation'
                        self.icon = 'bus'
                        self.icon_color = (0, 119/255, 1, 1)
                        self.md_bg_color = (189/255, 220/255, 1, 1)
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                        self.identity = 'Others'
                        self.icon_color = (0, 168/255, 107/255, 1)
                        self.md_bg_color = (207/255, 250/255, 234/255, 1)
                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = SwipeToDeleteItem(pk=task[0],
                                                     text=self.identity, secondary_text=convert_money, icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color)

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
                        self.identity = 'Food'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (253/255, 60/255, 74/255, 1)
                    elif spent[3] == 'acads':
                        self.icon = 'school-outline'
                        self.identity = 'School'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (252/255, 172/255, 18/255, 1)
                    elif spent[3] == 'bus':
                        self.identity = 'Transportation'
                        self.icon = 'bus'
                        self.icon_color = (0, 119/255, 1, 1)
                        self.md_bg_color = (189/255, 220/255, 1, 1)
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                        self.identity = 'Others'
                        self.icon_color = (0, 168/255, 107/255, 1)
                        self.md_bg_color = (207/255, 250/255, 234/255, 1)
                    convert_money = moneyFormat.money(int(spent[1]))
                    add_expenses = SwipeToDeleteItem(pk=spent[0],
                                                     text=self.identity, secondary_text=convert_money, icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color)

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
                        self.identity = 'Food'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (253/255, 60/255, 74/255, 1)
                    elif task[3] == 'acads':
                        self.icon = 'school-outline'
                        self.identity = 'School'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (252/255, 172/255, 18/255, 1)
                    elif task[3] == 'bus':
                        self.identity = 'Transportation'
                        self.icon = 'bus'
                        self.icon_color = (0, 119/255, 1, 1)
                        self.md_bg_color = (189/255, 220/255, 1, 1)
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                        self.identity = 'Others'
                        self.icon_color = (0, 168/255, 107/255, 1)
                        self.md_bg_color = (207/255, 250/255, 234/255, 1)
                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = SwipeToDeleteItem(pk=task[0],
                                                     text=self.identity, secondary_text=convert_money, icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color)

                    MDApp.get_running_app().root.first.ids.container.add_widget(add_expenses)

        except Exception:
            pass

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"


class AddExpenses(Screen):
    Builder.load_file('addexpense.kv')

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"

    def on_kv_post(self, base_widget):
        self.ids.food.text_color = [127/255, 61/255, 255/255, 1]
        self.category = "food"
        self.ids.food_bg.md_bg_color = [189/255, 181/255, 213/255, 1]
        self.ids.acads_bg.md_bg_color = [252/255, 238/255, 212/255, 1]
        self.ids.transpo_bg.md_bg_color = [189/255, 220/255, 1, 1]
        self.ids.others_bg.md_bg_color = [207/255, 250/255, 234/255, 1]

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
                        self.identity = 'Food'
                        self.md_bg_color = (253/255, 213/255, 215/255, 1)
                        self.icon_color = (253/255, 60/255, 74/255, 1)
                    elif task[3] == 'acads':
                        self.icon = 'school-outline'
                        self.identity = 'School'
                        self.md_bg_color = (252/255, 238/255, 212/255, 1)
                        self.icon_color = (252/255, 172/255, 18/255, 1)
                    elif task[3] == 'bus':
                        self.identity = 'Transportation'
                        self.icon = 'bus'
                        self.icon_color = (0, 119/255, 1, 1)
                        self.md_bg_color = (189/255, 220/255, 1, 1)
                    else:
                        self.icon = 'dots-horizontal-circle-outline'
                        self.identity = 'Others'
                        self.icon_color = (0, 168/255, 107/255, 1)
                        self.md_bg_color = (207/255, 250/255, 234/255, 1)
                    convert_money = moneyFormat.money(int(task[1]))
                    add_expenses = SwipeToDeleteItem(pk=task[0],
                                                     text=self.identity, secondary_text=convert_money, icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color)

                    MDApp.get_running_app().root.first.ids.container.add_widget(add_expenses)

        except Exception:
            pass

    def color(self, identity, background):
        self.ids.food.text_color = [253/255, 60/255, 74/255, 1]
        self.ids.acads.text_color = [252/255, 172/255, 18/255, 1]
        self.ids.transpo.text_color = [0, 119/255, 1, 1]
        self.ids.others.text_color = [0, 168/255, 107/255, 1]
        self.ids.food_bg.md_bg_color = [253/255, 213/255, 215/255, 1]
        self.ids.acads_bg.md_bg_color = [252/255, 238/255, 212/255, 1]
        self.ids.transpo_bg.md_bg_color = [189/255, 220/255, 1, 1]
        self.ids.others_bg.md_bg_color = [207/255, 250/255, 234/255, 1]
        identity.text_color = [127/255, 61/255, 255/255, 1]
        background.md_bg_color = [189/255, 181/255, 213/255, 1]
        self.category = str(identity.text)

    def add_task(self):

        date = str(datetime.now().strftime('%A, %B %d, %Y'))

        try:
            price = float(self.ids.price.text)
            if price != 0:
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

                self.listed.add_widget(SwipeToDeleteItem(
                    pk=select_expense[0], text=convert_money, secondary_text=select_expense[2], icon=self.icon))

                expenses_sum = db.expenses_sum()

                MDApp.get_running_app().root.first.ids.expense.text = str(
                    moneyFormat.money(expenses_sum))

                self.ids.price.text = ''
                self.input_added()
            else:
                self.input_denied()
        except:
            self.input_denied()

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

    def input_denied(self):
        self.dialog = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            radius=[20, 20, 20, 20],
            content_cls=DeniedExpense()
        )
        self.dialog.open()
        self.ids.price.text = '0'
        # Schedule the dialog dismissal after 3 seconds
        Clock.schedule_once(lambda dt: self.dialog.dismiss(), 3)


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
