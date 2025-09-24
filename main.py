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
from kivy.uix.popup import Popup

from db_handler import init_db, get_versions, get_categorys, add_category, add_version, add_entry

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

    init_db()
    
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
                                        values= get_versions() + ["New Version"])

        ##### deactivates the textinput and "add" button until "None" is selected #####
        tab1_version_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "New Version", tab1_version_textfield)
        )
        
        tab1_version_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "New Version", tab1_add_version_button)
        )

        #TODO: select latest added version-number automatically after adding to database / implement adding textinput value to database Version Tabel
        tab1_version_textfield = TextInput(multiline=False,
                                           size_hint=(1,None),
                                           height=40,
                                           text="new Version-number",
                                           disabled = True)
        
        tab1_version_textfield.bind(focus=self.on_focus_clear_textinput)
        
        
        tab1_add_version_button = Button(text="Add",
                                         size_hint=(1,None),
                                         height=40,
                                         disabled = True,
                                         )
        
        tab1_add_version_button.bind(on_release= lambda instance: ((add_version(tab1_version_textfield.text)),
                                                                    (setattr(tab1_version_selector, "values", get_versions() + ["New Version"])),
                                                                    (setattr(tab1_version_selector, "text", get_versions()[(len(get_versions()) - 1)]))
                                                                    )) 
        
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
                                        values= get_categorys() + ["New Category"],
                                        size_hint=(1,None),
                                        height=40)
        #deactivate textinput and add button until "None" is selected

        tab1_category_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "New Category", tab1_category_textfield)
        )
        
        tab1_category_selector.bind(
            text=lambda spinner, value: self.on_spinner_select(spinner, value, "New Category" ,tab1_add_category_button)
        )

        tab1_category_textfield = TextInput(multiline=False,
                                           size_hint=(1,None),
                                           height=40,
                                           text="new Category",
                                           disabled = True)
        
        tab1_category_textfield.bind(focus=self.on_focus_clear_textinput)

        
        tab1_add_category_button = Button(text="Add",
                                         size_hint=(1,None),
                                         height=40,
                                         disabled = True
                                         )

        tab1_add_category_button.bind(on_release= lambda instance: ((add_category(tab1_category_textfield.text)),
                                                                    (setattr(tab1_category_selector, "values", get_categorys() + ["New Category"])),
                                                                    (setattr(tab1_category_selector, "text", get_categorys()[(len(get_categorys()) - 1)]))
                                                                    )) 
        
        tab1_category.add_widget(tab1_category_selector)
        tab1_category.add_widget(tab1_category_textfield)
        tab1_category.add_widget(tab1_add_category_button)

        tab1_main.add_widget(tab1_category)

        tab1_language_label = Label(text="Language of Updatetext",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height = labels_height,
                                   )
        
        tab1_language_selector = Spinner(text="Select Language",
                                     values=("German", "English"),
                                     size_hint_y= None,
                                     height = buttons_height
                                    )
        
        tab1_main.add_widget(tab1_language_label)
        tab1_main.add_widget(tab1_language_selector)

        tab1_update_text = BoxLayout(orientation = "vertical")

        tab1_updatetext_label = Label(text="Updatetext",
                                   font_size = headline_1,
                                   size_hint=(None,None),
                                   height=labels_height, 
                                   )
        
        tab1_updatetex_textfield = TextInput(multiline=True)
        
        tab1_update_text.add_widget(tab1_updatetext_label)
        tab1_update_text.add_widget(tab1_updatetex_textfield)

        tab1_main.add_widget(tab1_update_text)

        tab1_layout.add_widget(tab1_main)
        
        succcess_popup = Popup(title="Success",
                               title_size = headline_1,
                               content = Label(text= "Entry successfully added",
                                               font_size = headline_2),
                               size_hint =(None,None),
                               size=(300,150))

        

        tab1_layout.add_widget(Button(text="Submit",
                                      size_hint= (1, None),
                                      height = buttons_height,
                                      on_release = lambda instance: (add_entry(tab1_version_selector.text, 
                                                                              tab1_category_selector.text,
                                                                              tab1_updatetex_textfield.text,
                                                                              tab1_language_selector.text
                                                                              ), succcess_popup.open() ))) 
        ## TODO:check if text has value then call function add entry if not show error popup, that not all information were filled
         

        tab1.add_widget(tab1_layout)
        main_window.add_widget(tab1)
        ### Logic and Database handling

        def addNewVersionNumber(version):
            version

     


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

# clear textinput on select
    def on_focus_clear_textinput(self, instance, value):
        if value:  # True, wenn TextInput den Fokus bekommt
            instance.text = ""  # Text leeren

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

if __name__ == '__main__':
    UpdatelogGenerator().run()