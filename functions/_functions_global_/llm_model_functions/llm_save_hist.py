import os
import json
import nltk
import string
nltk.download('punkt')


def save_conversation(chat_history, directory):
    # Convert chat history to the desired format
    formatted_history = []
    user_text = ""
    for i in chat_history:
        formatted_history.append({
            "role": "user",
            "content": i[0]
        })
        formatted_history.append({
            "role": "assistant",
            "content": i[1]
        })
        # Concatenate user text
        user_text += " " + i[0]

    # Tokenize the text and extract the desired words
    words = nltk.word_tokenize(user_text)
    
    # Remove punctuation from the words
    words = [word for word in words if word not in string.punctuation]
    filename_words = words[3:13]  # Take words after the first 3 words, up to 10 words
    filename = '_'.join(filename_words) + '.json'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save to a json file in the specified directory
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
        json.dump(formatted_history, f, ensure_ascii=False, indent=4)
