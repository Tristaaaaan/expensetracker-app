from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle
from kivymd.uix.imagelist import MDSmartTile
KV = '''
MDBottomSheet:
    id: bottom_sheet
    elevation: 2
    shadow_softness: 6
    bg_color: "white"
    type: "standard"
    max_opening_height: self.height
    default_opening_height: self.max_opening_height
    adaptive_height: True
    on_open: asynckivy.start(app.generate_content())
    MDBottomSheetDragHandle:
        drag_handle_color: "grey"
        MDBottomSheetDragHandleTitle:
            text: "Select type map"
            adaptive_height: True
            bold: True
            pos_hint: {"center_y": .5}
        MDBottomSheetDragHandleButton:
            icon: "close"
            _no_ripple_effect: True
            on_release: bottom_sheet.dismiss()
    MDBottomSheetContent:
        id: content_container
        padding: 0, 0, 0, "16dp"

'''

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        return Builder.load_string(KV)
Example().run()
