import webbrowser
from functions.menu_page.commands.web.check_connection import is_connected

if is_connected():
    import pywhatkit


class WebCommands:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk

    def search_ytb(self):
        # Search on YouTube
        youtube_keywords = ['lumen cherche sur youtube', 'lumen recherche sur youtube', 'lumen rechercher sur youtube', 
                            'lumen find on youtube', 'lumen find in youtube']
        if any(keyword in self.listen for keyword in youtube_keywords):
            ytb_command = self.listen.replace('Open YouTube and find', '')
            self.talk(f"Je cherche cela de suite !") if self.language == 'Fr' else self.talk(f"I'm looking for that right away !")
            pywhatkit.playonyt(ytb_command)
            
    def search_google(self):
        # Google
        google_keywords = ['lumen cherche sur google', 'lumen recherche sur google', 'lumen find on google', 'lumen find in google']
        for keyword in google_keywords:
            if keyword in self.listen:
                search = self.listen.replace(keyword, '').strip()
                if search.startswith('re '):
                    search = search[3:]
                url = "https://www.google.com/search?q=" + search
                self.talk(f"Recherche sur Google...{search}") if self.language == 'Fr' else self.talk(f"Search on Google...{search}")
                webbrowser.open(url)
                break

    def search_wikipedia(self):
        # Wikipedia
        wikipedia_keywords = ['lumen cherche sur wikipédia', 'lumen recherche sur wikipédia', 'lumen recherche wikipédia',
                            'lumen cherche wikipédia', 'lumen find on wikipedia', 'lumen find in wikipedia']
        for keyword in wikipedia_keywords:
            if keyword in self.listen:
                search = self.listen.replace(keyword, '').strip()
                if search.startswith('re '):
                    search = search[3:]
                url = "https://fr.wikipedia.org/wiki/" + search
                self.talk(f"Recherche sur Wikipédia...{search}") if self.language == 'Fr' else self.talk(f"Search on Wikipedia...{search}")
                webbrowser.open(url)
                break

    def search_bing(self):    
        # Bing
        bing_keywords = ['lumen cherche sur bing', 'lumen recherche sur bing', 'lumen find on bing', 'lumen find in bing']
        for keyword in bing_keywords:
            if keyword in self.listen:
                search = self.listen.replace(keyword, '').strip()
                if search.startswith('re '):
                    search = search[3:]
                url = "https://www.bing.com/search?q=" + search
                self.talk(f"Recherche sur Bing...{search}") if self.language == 'Fr' else self.talk(f"Search on Bing...{search}")
                webbrowser.open(url)
                break
            
    def search_gpt(self):
        # Chat GPT
        openai_keywords = ['lumen ouvre chat ia', 'lumen ouvre chat gpt', 'lumen ouvre le chat gpt', 'lumen recherche sur chat ia', 
                           'lumen search on ai chat', 'lumen cherche sur chat ia', 'lumen search in ai chat', 'lumen start ai chat']
        if any(keyword in self.listen for keyword in openai_keywords):
            url = "https://chat.openai.com/"
            self.talk(f"Ouverture de Chat GPT...") if self.language == 'Fr' else self.talk(f"Open Chat GPT...")
            webbrowser.open(url)