from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

KV = '''
<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"

        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}
            on_release: app.remove_item(root)

    MDCardSwipeFrontBox:

        ListItemWithIcon:
            id: content
            text: root.text
            secondary_text: root.secondary_text
            _no_ripple_effect: True
            CustomIconLeftWidget:
                icon: root.icon
                disabled: True
                theme_text_color: 'Custom'
                radius: [10, 5, 10, 20]
                disabled_color: [253/255, 60/255, 74/255, 1]

Screen:

    BoxLayout:
        orientation: "vertical"
        
        BoxLayout:
            orientation: "vertical"
            spacing: "10dp"
    
    
            ScrollView:
    
                MDList:
                    id: md_list
                    padding: 0
'''


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''
    divider = None


class CustomIconLeftWidget(IconLeftWidget):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()


class TestCard(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return self.screen

    def remove_item(self, instance):
        self.screen.ids.md_list.remove_widget(instance)

    def on_start(self):
        for i in range(20):
            self.screen.ids.md_list.add_widget(
                SwipeToDeleteItem(
                    text=f"One-line item {i}", secondary_text='Hehe', icon="trash-can")
            )


TestCard().run()
