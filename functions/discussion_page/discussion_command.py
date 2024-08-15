from functions.discussion_page.discussion_mode import start_discussion


class DiscussionCommand:
    def __init__(self, listen, device, lang, talk, model_path, hist_dir):
        self.listen = listen
        self.device = device
        self.lang = lang
        self.talk = talk
        self.model_path = model_path
        self.hist_dir = hist_dir
        
    def launch_discussion_mode(self):
        text_llm_keywords = ['lumen passe en mode discussion', 'lumen passe en discussion', 'lumen passage en mode discussion',
                             'lumen mode discussion', 'lumen switch to discussion mode', 'lumen switch to discussion', 'lumen discussion mode']
        if any(keyword in self.listen for keyword in text_llm_keywords):
            self.talk("Mode Discussion Activé" if self.lang == 'Fr'else "Discussion Mode Activated")
            start_discussion(self.device, self.lang, self.talk, self.model_path, self.hist_dir)