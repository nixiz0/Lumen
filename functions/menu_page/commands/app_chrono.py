import platform
import subprocess


class ChronoCommand:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk
        self.os = platform.system()

    def start_chrono(self):
        start_chronometer_keywords = ['lumen démarre le chronomètre', 'lumen démarre le chrono', 
                                      'lumen start the chronometer', 'lumen start the chrono']
        if any(keyword in self.listen for keyword in start_chronometer_keywords):
            if self.os == 'Windows':
                if self.language == 'Fr':
                    self.talk("Chronomètre ouvert.")
                else:
                    self.talk("Chronometer open.")
                subprocess.Popen('start explorer.exe shell:AppsFolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App', shell=True)
            elif self.os == 'Linux':
                if self.language == 'Fr':
                    self.talk("Chronomètre ouvert.")
                else:
                    self.talk("Chronometer open.")
                subprocess.Popen(['gnome-clocks'])
            elif self.os == 'Darwin':
                if self.language == 'Fr':
                    self.talk("Chronomètre ouvert.")
                else:
                    self.talk("Chronometer open.")
                subprocess.Popen(['open', '/Applications/Clock.app'])
