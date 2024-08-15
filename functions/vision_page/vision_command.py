from functions.vision_page.vision_mode import start_vision


class VisionCommand:
    def __init__(self, listen, device, language, talk, model_path, hist_dir):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk
        self.model_path = model_path
        self.hist_dir = hist_dir
        
    def launch_vision_mode(self):
        llm_vision_start_keywords = ['lumen passe en mode analyse', 'lumen passe en analyse', 'lumen passage en mode analyse', 'lumen passage en mode vision',
                                     'lumen mode vision', 'lumen passage en vision', 'lumen passe en vision', 'lumen passe en mode vision', 
                                     'lumen switch to analysis mode', 'lumen switch to analyse', 'lumen switch to vision', 'lumen switch to vision mode', 
                                     'lumen switch to analysis', 'lumen switch to analyse mode', 'lumen vision mode']
        if any(keyword in self.listen for keyword in llm_vision_start_keywords):
            if self.language == 'Fr':
                self.talk("Mode Vision Activé")
            else: 
                self.talk("Vision Mode Activated")
            start_vision(self.device, self.language, self.talk, self.model_path, self.hist_dir)