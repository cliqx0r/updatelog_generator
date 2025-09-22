from kivy.config import Config

screenwidth = 1280
screenheight = 768

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', str(screenwidth))
Config.set('graphics', 'height', str(screenheight))

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

import sqlite3

connection = ""

### Font-Sizes:
headline_1 = 20
headline_2 = 16
textblock_size = 12

#widget-hights
header_height = 30
buttons_height = 40
labels_height = 40
main_window_height = int(screenheight) - header_height - buttons_height

class UpdatelogGenerator(App):
    
    def build(self):

        layout_main = BoxLayout(orientation='vertical', spacing=10)

        headline = Label(
            text="Updatelog Generator",
            font_size = headline_1,
            size_hint_y= None, 
            height= header_height
            )
        
        main_window = TabbedPanel(do_default_tab=False, size_hint_y = 1)
        # Tab 1
        tab1 = TabbedPanelItem(text="New Entry")
        tab1_layout = BoxLayout(orientation='vertical', spacing=10)
        
        tab1_main = BoxLayout(orientation = "vertical")
        
        tab1_main.add_widget(Label(text="Version",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height=labels_height,
                                  
                                   ))

        tab1_version = BoxLayout(orientation = "horizontal",
                                 size_hint= (None,None),
                                 height=labels_height,
                                 width= screenwidth)

        tab1_version_selector = Spinner(text="Select Version",
                                        size_hint=(1,None),
                                        height=labels_height,
                                        values=("5.2.0.6366", "5.3.0.6366", "5.2.0.34366", "None")  #TODO: get values from Versions Tabel of DB
            )

        ##### deactivates the textinput and "add" button until "None" is selected #####
        tab1_version_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "None", tab1_version_textfield)
        )
        
        tab1_version_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "None", tab1_add_version_button)
        )

        #TODO: select latest added version-number automatically after adding to database / implement adding textinput value to database Version Tabel
        tab1_version_textfield = TextInput(multiline=False,
                                           size_hint=(1,None),
                                           height=40,
                                           text="new Version-number",
                                           disabled = True)
        
        tab1_add_version_button = Button(text="Add",
                                         size_hint=(1,None),
                                         height=40,
                                         disabled = True
                                         )

        tab1_version.add_widget(tab1_version_selector)
        tab1_version.add_widget(tab1_version_textfield)
        tab1_version.add_widget(tab1_add_version_button)
        
        tab1_main.add_widget(tab1_version)

        tab1_main.add_widget(Label(text="Category",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height=40,
                                   ))
        
        tab1_category = BoxLayout(orientation = "horizontal",
                                  size_hint= (None,None),
                                  height=40,
                                  width= screenwidth)

        tab1_category_selector =Spinner(text="Select Category",
                                        values=("General", "Homag", "Biesse", "None"),
                                        size_hint=(1,None),
                                        height=40
                                        )
        #deactivate textinput and add button until "None" is selected

        tab1_category_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "None", tab1_category_textfield)
        )
        
        tab1_category_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "None" ,tab1_add_category_button)
        )

        tab1_category_textfield = TextInput(multiline=False,
                                           size_hint=(1,None),
                                           height=40,
                                           text="new Category",
                                           disabled = True)
        
        tab1_add_category_button = Button(text="Add",
                                         size_hint=(1,None),
                                         height=40,
                                         disabled = True
                                         )
        
        tab1_category.add_widget(tab1_category_selector)
        tab1_category.add_widget(tab1_category_textfield)
        tab1_category.add_widget(tab1_add_category_button)

        tab1_main.add_widget(tab1_category)

        tab1_main.add_widget(Label(text="Language",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height = labels_height,
                                   ))
        
        tab1_main.add_widget(Spinner(text="Select Language",
                                     values=("German", "English"),
                                     size_hint_y= None,
                                     height = buttons_height
                                    ))

        tab1_update_text = BoxLayout(orientation = "vertical")

        tab1_updatetext_label = Label(text="Updatetext",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height=labels_height, 
                                   )
        
        tab1_updatetex_textfield = TextInput(multiline=True)
        
        tab1_update_text.add_widget(tab1_updatetex_textfield)
        tab1_update_text.add_widget(tab1_updatetext_label)

        tab1_main.add_widget(tab1_update_text)

        tab1_layout.add_widget(tab1_main)
        
        tab1_layout.add_widget(Button(text="Submit",
                                      size_hint= (1, None),
                                      height = buttons_height,
                                      on_release = lambda instance: self.button_press(instance, tab1_updatetex_textfield.text)))    

        tab1.add_widget(tab1_layout)
        main_window.add_widget(tab1)

        # Tab 2
        tab2 = TabbedPanelItem(text="Overview")
        tab2.add_widget(Label(text="Overview"))
        main_window.add_widget(tab2)

        # Tab 3
        tab3 = TabbedPanelItem(text="Settings")

        tab3_main = BoxLayout(orientation = "vertical",
                              size_hint=(None,None),
                              width = screenwidth)
        
        tab3_database_settings_headline = Label(text="Settings",
                                                font_size = headline_1,
                                                size_hint=(None,None),
                                                height=labels_height,
                                                width = screenwidth)

        tab3_database_settings = BoxLayout(orientation = "horizontal",
                                           size_hint=(None,None),
                                           height = buttons_height,
                                           width = screenwidth)
                                           
        tab3_database_path_label = Label(text="Database Path",
                                         font_size = headline_2,
                                         size_hint=(1,None),
                                         height=labels_height)
        
        ### TODO: set Database Path via file-selector
        tab3_database_path_input = TextInput(text="Path",
                                             size_hint=(1,None),
                                             height=buttons_height)
        
        tab3_main.add_widget(tab3_database_settings_headline)
        tab3_main.add_widget(tab3_database_settings)
        tab3_database_settings.add_widget(tab3_database_path_label)
        tab3_database_settings.add_widget(tab3_database_path_input)
        
        tab3.add_widget(tab3_main)


        main_window.add_widget(tab3)

        layout_main.add_widget(headline)
        layout_main.add_widget(main_window)

        return layout_main



#Function to disable a widget unti a specifiv value is selected 
    def on_spinner_select(self, spinner, value, expected_value ,disable_widget):
       
        if value == expected_value:
            # Eingabe aktivieren
            disable_widget.disabled = False
            disable_widget.disabled = False
        else:
            # Eingabe deaktivieren
            disable_widget.disabled = True
            disable_widget.disabled = True

    def button_press(self, button, value):
        if value:
            print(value)
        else:
            pass


if __name__ == '__main__':
    UpdatelogGenerator().run()