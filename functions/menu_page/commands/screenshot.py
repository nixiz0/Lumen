import os 
import pyautogui


class ScreenCommand:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk

    def screen(self):
        screen_keywords = ['lumen prends un screen', 'lumen prends une capture d\'écran', 'lumen capture d\'écran',
                        'lumen prend un screen', 'lumen prend une capture d\'écran',
                        'lumen take a screen', 'lumen take a screenshot', 'lumen screenshot']
        for keyword in screen_keywords:
            if keyword in self.listen:
                download_dir = str('photos/')
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                base_filename = 'screenshot'
                extension = '.png'
                filename = f"{base_filename}{extension}"
                screenshot = pyautogui.screenshot()
                screenshot.save(os.path.join(download_dir, filename))
                if self.language == 'Fr':
                    self.talk("Capture d'écran effectuée")
                else: 
                    self.talk("Screenshot taken")
                return True