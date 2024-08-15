import datetime
import locale


def time_in_locale(language):
    if language == 'Fr':
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Set the locale to French
        formatted_time = datetime.datetime.now().strftime('%H:%M:%S')
        return formatted_time

    elif language == 'En':
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')  # Set the locale to English
        formatted_time = datetime.datetime.now().strftime('%H:%M:%S')
        return formatted_time

def date_in_locale(language):
    if language == 'Fr':
        locale.setlocale(locale.LC_TIME, 'fr_FR')  # Set the locale to French
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%A %d %B %Y')
        return formatted_datetime

    elif language == 'En':
        locale.setlocale(locale.LC_TIME, 'en_US')  # Set the locale to English
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%A %d %B %Y')
        return formatted_datetime
    
class TimeCommands:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk

    def time_command(self):
        # Current Time
        detect_time_keywords = ['lumen il est quelle heure', 'lumen quelle heure est-il', 'lumen l\'heure actuelle', 
                                'lumen what time is it', 'lumen actual time']
        if any(keyword in self.listen for keyword in detect_time_keywords):
            formatted_time = time_in_locale(self.language)
            self.talk(formatted_time)

    def date_command(self):       
        # Current Date
        detect_datetime_keywords = ['lumen date actuelle', 'lumen date d\'aujourd\'hui',
                                    'lumen current date', 'lumen today\'s date', 'lumen date of today']
        if any(keyword in self.listen for keyword in detect_datetime_keywords):
            formatted_datetime = date_in_locale(self.language)
            self.talk(formatted_datetime)