from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyBoxLayout(BoxLayout):
    def start_script(self):
       import index
       index.run()

    def stop_script(self):
        # Implement logic to stop the script (if necessary)
        pass

class MyApp(App):
    def build(self):
        layout = MyBoxLayout(orientation='vertical')
        start_button = Button(text='Start')
        stop_button = Button(text='Stop')

        # Bind the buttons to their respective functions
        start_button.bind(on_press=lambda x: layout.start_script())
        stop_button.bind(on_press=lambda x: layout.stop_script())

        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        return layout

if __name__ == '__main__':
    MyApp().run()
