from kivy.app import App
from airtable import Airtable
import pprint
from kivy.factory import Factory as F
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.config import Config
import webbrowser


def callback(link):
    webbrowser.open(link)


def generate_data_model(pages):
    menu = {}
    for page in pages:
        for record in page:
            # pp.pprint(record["fields"])
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
                    btn.bind(on_press=lambda x: callback(link=menu_option["URL"]))
                else:
                    btn = Button(text="NO TITLE FOUND", size_hint_y=None, height=44)
                    btn.bind(on_press=lambda x: callback(link=menu_option["URL"]))

                dropdown.add_widget(btn)

            sub_menu_menu.bind(on_release=dropdown.open)

            ag.add_widget(sub_menu_menu)

        av.add_widget(ag)

    actionbar.add_widget(av)
    av.use_separator = True

    return actionbar


class TestApp(App):
    def build(self):
        api_key = 'keyq710GTffnK4vfA'
        table_name = 'Config'
        base_key = 'appdqzfZoeTcXC7VD'
        airtable = Airtable(base_key=base_key, table_name=table_name, api_key=api_key)

        pages = airtable.get_iter(maxRecords=100)
        menus = generate_data_model(pages)
        return generate_GUI(menus)


TestApp().run()
