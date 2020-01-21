from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
import requests
import re

presentation = Builder.load_string("""
#: import FloatLayout kivy.uix.floatlayout

FloatLayout
    TextInput:
        id: url_text_input
        size_hint: 0.9, 0.05
        multiline: False
        pos_hint:  { "x": 0.05, "y": 0.9 }
        text: "Enter URL"
        on_text_validate: app.extract_links('url_text_input')

    ScrollView
        id: sv
        size_hint: 0.9, 0.8
        pos_hint:  { "x": 0.05, "y": 0.05 }
        bar_width: 10
        scroll_type: ['bars']
        TextInput:
            id: output
            size_hint: 5, None
            height: max(self.minimum_height, sv.height)
""")


class MainApp(App):

    def build(self):
        Window.maximize()
        # Window.bind(on_key_down=self.key_action)
        return presentation

    # def key_action(self, *args):
    #     if len(args[-1]) > 0 and args[-1][0] == 'alt' and args[-2] == 's':
    #         self.extract_links(presentation.ids['url_text_input'].text)

    def on_start(self):
        self.init_config()

    def init_config(self):
        self.set_focus('url_text_input')
        self.select_text('url_text_input')

    @staticmethod
    def set_focus(widget_id):
        presentation.ids[widget_id].focus = True

    @staticmethod
    def select_text(widget_id):
        presentation.ids[widget_id].select_all()

    def extract_links(self, widget_id):
        try:
            self.set_output("Extracting links...")
            url = presentation.ids[widget_id].text
            raw_page = self.download_page(url)
            extracted_links = self.extract_links_from_raw_page(raw_page)
            self.set_output(extracted_links)
        except Exception as e:
            self.set_output(f"Unable to parse link. Error - {str(e)}")

    @staticmethod
    def set_output(content):
        presentation.ids['output'].text = content

    def extract_links_from_raw_page(self, raw_page):
        patterns = [
            r'"(ed2k://[^"]+)"',
            r'"(thunder://[^"]+)"',
            r'"(magnet:[^"]+)"',
        ]
        results = []
        for pattern in patterns:
            match_iter = re.finditer(pattern, raw_page)
            for matched_index in match_iter:
                result = raw_page[matched_index.start()+1: matched_index.end()-1]
                if result not in results:
                    results.append(result)

        extracted_links = '\n'.join(results)
        return extracted_links

    @staticmethod
    def download_page(url):
        response = requests.get(url=url)
        return response.content.decode()


if __name__ == '__main__':
    MainApp().run()

