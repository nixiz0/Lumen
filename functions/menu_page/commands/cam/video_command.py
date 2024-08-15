from functions.menu_page.commands.cam.video_capture import video_capture


class VideoCommand:
    def __init__(self, listen, device, language, talk):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk

    def start_video(self):
        video_keywords = ['lumen commence à filmer', 'lumen lance la vidéo', 'lumen film', 'lumen filme', 
                           'lumen start filming', 'lumen start video capture', 'lumen start a video']
        for keyword in video_keywords:
            if keyword in self.listen:
                if self.language == 'Fr':
                    self.talk("Lancement de la vidéo")
                else: 
                    self.talk("Starting the video")
                video_capture(self.listen, self.device, self.language, self.talk)