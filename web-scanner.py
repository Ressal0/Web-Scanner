from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import subprocess
import threading
import queue

class WebsiteScanner(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_queue = queue.Queue()
        self.current_thread = None
        self.scanning = False

    def build(self):
        Window.size = (600, 800)
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.input_field = TextInput(
            hint_text='Enter website URLs separated by space',
            multiline=False,
            size_hint_y=None,
            height=40
        )

        scan_type_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.nmap_button = ToggleButton(text='Nmap', group='scan_type', state='down')
        self.sqlmap_button = ToggleButton(text='SQLMap', group='scan_type')
        self.both_button = ToggleButton(text='Both', group='scan_type')
        
        scan_type_layout.add_widget(self.nmap_button)
        scan_type_layout.add_widget(self.sqlmap_button)
        scan_type_layout.add_widget(self.both_button)

        self.scan_button = Button(
            text='Scan',
            size_hint_y=None,
            height=50,
            background_color=(0, 0.6, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        self.scan_button.bind(on_press=self.start_scan)

        self.cancel_button = Button(
            text='Cancel',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0, 0, 1),
            color=(1, 1, 1, 1),
            disabled=True
        )
        self.cancel_button.bind(on_press=self.cancel_scan)

        self.output_field = TextInput(
            text='',
            multiline=True,
            readonly=True,
            size_hint=(1, 1)
        )

        layout.add_widget(self.input_field)
        layout.add_widget(scan_type_layout)
        layout.add_widget(self.scan_button)
        layout.add_widget(self.cancel_button)
        layout.add_widget(self.output_field)

        return layout

    def start_scan(self, instance):
        websites = self.input_field.text.strip().split()
        if not websites:
            self.show_popup("Input Error", "Please enter one or more website URLs.")
            return

        self.scanning = True
        self.scan_button.disabled = True
        self.cancel_button.disabled = False
        self.output_field.text = ''  # Clear previous results

        for website in websites:
            if self.nmap_button.state == 'down' or self.both_button.state == 'down':
                self.scan_queue.put(('nmap', website))
            if self.sqlmap_button.state == 'down' or self.both_button.state == 'down':
                self.scan_queue.put(('sqlmap', website))

        self.current_thread = threading.Thread(target=self.process_scan_queue)
        self.current_thread.start()

        Clock.schedule_interval(self.check_scan_complete, 1)

    def process_scan_queue(self):
        while not self.scan_queue.empty() and self.scanning:
            scan_type, website = self.scan_queue.get()
            result = f"Scanning {website} with {scan_type}...\n"
            if scan_type == 'nmap':
                result += self.run_nmap(website)
            else:
                result += self.run_sqlmap(website)
            Clock.schedule_once(lambda dt, r=result: self.update_output(r))

    def check_scan_complete(self, dt):
        if self.scan_queue.empty() and not self.current_thread.is_alive():
            self.scanning = False
            self.scan_button.disabled = False
            self.cancel_button.disabled = True
            Clock.unschedule(self.check_scan_complete)
            Clock.schedule_once(lambda dt: self.update_output("Scan complete.\n"))

    def cancel_scan(self, instance):
        self.scanning = False
        with self.scan_queue.mutex:
            self.scan_queue.queue.clear()
        self.scan_button.disabled = False
        self.cancel_button.disabled = True
        Clock.schedule_once(lambda dt: self.update_output("Scan cancelled.\n"))

    def update_output(self, text):
        self.output_field.text += text

    def run_nmap(self, website):
        try:
            command = ["nmap", "-v", website]
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                return f"Error scanning {website} with nmap: {result.stderr}\n"
            return f"Nmap scan results for {website}:\n{result.stdout}\n"
        except subprocess.TimeoutExpired:
            return f"Nmap scan for {website} timed out after 5 minutes.\n"
        except Exception as e:
            return f"An error occurred while scanning {website} with nmap: {e}\n"

    def run_sqlmap(self, website):
        try:  
            command = ["sqlmap", "-u", website, "--batch", "--crawl=1"]
            result = subprocess.run(command, capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                return f"Error testing {website} with sqlmap: {result.stderr}\n"
            return f"SQLMap scan results for {website}:\n{result.stdout}\n"
        except subprocess.TimeoutExpired:
            return f"SQLMap scan for {website} timed out after 10 minutes.\n"
        except Exception as e:
            return f"An error occurred while testing {website} with sqlmap: {e}\n"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    WebsiteScanner().run()
