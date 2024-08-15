from functions.precision_page.precision_mode import start_precision


class PrecisionCommand:
    def __init__(self, listen, device, language, talk, model_path, hist_dir):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk
        self.model_path = model_path
        self.hist_dir = hist_dir
        
    def launch_precision_mode(self):
        precision_llm_start_keywords = ['lumen passe en mode précision', 'lumen passe en précision', 'lumen passage en mode précision',
                                   'lumen mode précision', 'lumen switch to precision mode', 'lumen switch to precision', 'lumen precision mode']
        if any(keyword in self.listen for keyword in precision_llm_start_keywords):
            if self.language == 'Fr':
                self.talk("Mode Précision Activé")
            else: 
                self.talk("Precision Mode Activated")
            start_precision(self.device, self.language, self.talk, self.model_path, self.hist_dir)