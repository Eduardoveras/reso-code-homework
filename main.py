import pprint
import webbrowser
from airtable import Airtable
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.config import Config

kv = '''
<Label>:
    font_size: dp(16)
'''
Builder.load_string(kv)


def generate_data_model(pages):
    menu = {}
    for page in pages:
        for record in page:
            if "Live" in record["fields"] and record["fields"]["Live"] is True:
                if record["fields"]["Main Menu"] in menu:

                    if "Sub-menu" in record["fields"]:
                        if record["fields"]["Sub-menu"] in menu[record["fields"]["Main Menu"]]:
                            menu[record["fields"]["Main Menu"]][record["fields"]["Sub-menu"]].append(record["fields"])
                        else:
                            menu[record["fields"]["Main Menu"]][record["fields"]["Sub-menu"]] = []
                            menu[record["fields"]["Main Menu"]][record["fields"]["Sub-menu"]].append(record["fields"])

                    elif '<EMPTY>' not in menu[record["fields"]["Main Menu"]]:
                        menu[record["fields"]["Main Menu"]]['<EMPTY>'] = []
                        menu[record["fields"]["Main Menu"]]['<EMPTY>'].append(record["fields"])
                    else:
                        menu[record["fields"]["Main Menu"]]['<EMPTY>'].append(record["fields"])

                else:
                    menu[record["fields"]["Main Menu"]] = {}
                    if "Sub-menu" in record["fields"]:
                        menu[record["fields"]["Main Menu"]][record["fields"]["Sub-menu"]] = []
                        menu[record["fields"]["Main Menu"]][record["fields"]["Sub-menu"]].append(record["fields"])
                    else:
                        menu[record["fields"]["Main Menu"]]['<EMPTY>'] = []
                        menu[record["fields"]["Main Menu"]]['<EMPTY>'].append(record["fields"])

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(menu)
    return menu


''' OLD GUI IMPLEMENTATION, IGNORE THIS
def generate_GUI(menus):
    actionbar = F.ActionBar(pos_hint={'top': 1})

    av = F.ActionView()
    av.add_widget(F.ActionPrevious(title='Resonance Menu', with_previous=False))
    av.add_widget(F.ActionOverflow())

    for menu_key, sub_menu in menus.items():
        ag = F.ActionGroup(text=menu_key)
        for sub_menu_key, items in sub_menu.items():
            dropdown = DropDown(width=440)
            sub_menu_menu = F.ActionButton(text=sub_menu_key)
            for menu_option in items:
                if "Name" in menu_option:
                    btn = Button(text=menu_option["Name"], size_hint_y=None, height=44)
                    btn.bind(on_press=lambda x: webbrowser.open(menu_option["URL"]))
                    dropdown.add_widget(btn)
                else:
                    btn = Button(text="<EMPTY>", size_hint_y=None, height=44)
                    btn.bind(on_press=lambda x: webbrowser.open(menu_option["URL"]))
                    dropdown.add_widget(btn)

            dropdown.add_widget(Button(text="___________________________", size_hint_y=None, height=44))
            sub_menu_menu.bind(on_release=dropdown.open)

            ag.add_widget(sub_menu_menu)

        av.add_widget(ag)

    actionbar.add_widget(av)
    av.use_separator = True

    return actionbar
    '''


def generate_layout(layout, menus, should_generate_menu):
    layout.clear_widgets()
    btn1 = Button(text='Generate Resonance Menu', size_hint=(1, 1))
    if should_generate_menu:
        inner_layout = generate_GUI(menus)
    else:
        inner_layout = BoxLayout(orientation='vertical')
    # Recursive call
    btn1.bind(on_press=lambda x: generate_layout(layout, menus, True))

    title_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
    title_layout.add_widget(Image(source='logo.jpg', size_hint=(0.15, 1)))
    title_layout.add_widget(btn1)

    layout.add_widget(title_layout)
    # layout.add_widget(Button(text='Generate Resonance Menu', size_hint=(1, 0.1)))
    layout.add_widget(inner_layout)
    return layout


def generate_GUI(menus):
    app_gui = TabbedPanel()
    app_gui.clear_tabs()
    app_gui.orientation = "vertical"
    app_gui.do_default_tab = False
    app_gui.tab_width = 150

    for menu_key, sub_menu in menus.items():
        main_menu = TabbedPanelHeader(text=menu_key)
        scroll_pane = ScrollView()
        scroll_pane.scroll_type = ['bars', 'content']
        scroll_pane.bar_pos_y = 'left'
        scroll_pane.bar_width = 6
        scroll_pane.do_scroll_y = True
        scroll_pane.do_scroll_x = False
        scroll_pane.scroll_y = 1

        menu_grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        menu_grid.orientation = "vertical"
        menu_grid.padding = 10
        menu_grid.row_default_height = 1
        menu_height = 0

        print(">>>" + menu_key)
        for sub_menu_key, items in sub_menu.items():
            menu_grid.add_widget(
                Label(text="     " + sub_menu_key, size_hint=(None, None), font_size=14, halign="left",
                      valign="middle"))
            print("\t" + sub_menu_key)
            for option in items:

                if "Name" in option:
                    print("\t\t" + option["Name"])
                    btn = Button(text=option["Name"], size_hint=(0.1, None), background_color=(0.2, 1, 1, 0.8))
                    btn.bind(on_press=lambda x: webbrowser.open(option["URL"]))
                else:
                    print("\t\t" + "<EMPTY>")
                    btn = Button(text="<EMPTY>", size_hint=(0.1, None), background_color=(0.2, 1, 1, 0.8))
                    btn.bind(on_press=lambda x: webbrowser.open(option["URL"]))
                btn.width = 250
                btn.height = 50
                menu_grid.add_widget(btn)
                menu_height += 80
            menu_height += 51
        menu_grid.height = menu_height
        scroll_pane.add_widget(menu_grid)
        main_menu.content = scroll_pane
        main_menu.orientation = "vertical"

        # Adding headers to main layout
        app_gui.add_widget(main_menu)
    return app_gui


class TestApp(App):
    def build(self):
        api_key = 'keyq710GTffnK4vfA'
        table_name = 'Config'
        base_key = 'appdqzfZoeTcXC7VD'
        airtable = Airtable(base_key=base_key, table_name=table_name, api_key=api_key)
        self.title = 'Resonance Menu'
        Config.set('kivy', 'window_icon', 'logo.ico')

        pages = airtable.get_iter(maxRecords=100)
        menus = generate_data_model(pages)

        return generate_layout(BoxLayout(orientation='vertical'), menus, False)


TestApp().run()
