import sympy
import re


def calculate(calc_command, language):
    # Define the words and their replacements
    words = {
        'Fr': ['moins', 'plus', 'divisé', 'x', 'fois', 'multiplié', 'au carré', 'puissance deux',\
               'puissance 2', 'sinusoide', 'cosinus', 'tangente', 'racine', 'intégrale', 'intégral', 'dérivée'],
        'En': ['minus', 'plus', 'divided', 'x', 'times', 'multiplied', 'squared', 'power of two', 'power 2', 'sine',\
               'cosine', 'tangent', 'root', 'integral', 'derivative']
    }
    replacements = {
        'Fr': ['-', '+', '/', '*', '*', '*', '**2', '**2', '**2', 'sin', 'cos', 'tan', 'sqrt', 'integrate', 'integrate', 'diff'],
        'En': ['-', '+', '/', '*', '*', '*', '**2', '**2', '**2', 'sin', 'cos', 'tan', 'sqrt', 'integrate', 'diff']
    }
    
    # Extraction of numbers, mathematical operators and mathematical functions
    calc_command = re.findall(r"[\d]+|[\+\-\*\/]|" + "|".join(words[language]), calc_command)
    calc_command = ' '.join(calc_command)
    
    # Replacing words with their respective mathematical symbols
    for word, replacement in zip(words[language], replacements[language]):
        calc_command = calc_command.replace(word, replacement)
    
    # Added parentheses around arguments of mathematical functions
    calc_command = re.sub(r"(sin|cos|tan|sqrt|integrate|diff) (\d+)", r"\1(\2)", calc_command)
    
    try:
        result = sympy.sympify(calc_command)
        result = round(result, 2)
        return f"Cela fait {result}" if language == 'Fr' else f"This makes {result}"
    except Exception as e:
        return "Désolé, je n'ai pas pu effectuer le calcul." if language == 'Fr' else "Sorry, I couldn't do the calculation."
    
class CalculCommands:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk

    def calcul_command(self):
        # Calcul
        calc_keywords = ['lumen calcule', 'lumen calcul', 'lumen compute', 'lumen calculate']
        if any(keyword in self.listen for keyword in calc_keywords):
            calc_command = self.listen.replace('lumen calcule', '').replace('lumen calcul', '').replace('lumen compute', '').replace('lumen calculate', '')
            self.talk(calculate(calc_command, self.language))