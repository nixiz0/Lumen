from functions.code_page.code_mode import start_code


class CodeCommand:
    def __init__(self, listen, device, language, talk, model_path, hist_dir):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk
        self.model_path = model_path
        self.hist_dir = hist_dir
        
    def launch_code_mode(self):
        code_llm_start_keywords = ['lumen passe en mode code', 'lumen passe en code', 'lumen passage en mode code',
                                   'lumen mode code', 'lumen switch to code mode', 'lumen switch to code', 'lumen code mode']
        if any(keyword in self.listen for keyword in code_llm_start_keywords):
            if self.language == 'Fr':
                self.talk("Mode Code Activé")
            else: 
                self.talk("Coding Mode Activated")
            start_code(self.device, self.language, self.talk, self.model_path, self.hist_dir)