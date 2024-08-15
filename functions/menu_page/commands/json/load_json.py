import json
import os


def load_sentences():
    sentences = {}
    json_dir = os.path.join('config_json')
    target_file = 'text.json'
    
    if target_file in os.listdir(json_dir):
        with open(os.path.join(json_dir, target_file), 'r', encoding='utf-8') as f:
            if f.read().strip():
                f.seek(0)
                sentences.update(json.load(f))
    return sentences

def load_app_paths():
    app_paths = {}
    json_dir = os.path.join('config_json')
    target_file = 'app.json'
    
    if target_file in os.listdir(json_dir):
        with open(os.path.join(json_dir, target_file), 'r', encoding='utf-8') as f:
            if f.read().strip():
                f.seek(0)
                app_paths.update(json.load(f))
    return app_paths
