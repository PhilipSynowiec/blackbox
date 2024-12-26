import json
import os

class DB(object):
    def __init__(self, file_path='database.json'):
        self.file_path = file_path

    def add_entry(self, word: str, grammatical_type: str, cloze_sentence: str, anki_id=None):
        data = self._load_data()
        if self.check_entry_exists(word, grammatical_type):
            print(f"The entry '{word}" + ("" if grammatical_type is None else f" ({grammatical_type})") + f"' already exists.")
            return

        data.append({
            "word": word,
            "grammatical_type": grammatical_type,
            "cloze_sentence": cloze_sentence,
            "anki_id": anki_id
        })

        self._save_data(data)
        print(f"The entry '{word} ({grammatical_type}) - {cloze_sentence}' was added.")

    def check_entry_exists(self, word, grammatical_type=None):
        data = self._load_data()
        return any(entry['word'] == word and (entry['grammatical_type'] == grammatical_type or grammatical_type is None) for entry in data)

    def get_all_entries(self):
        return self._load_data()

    def set_all_entries(self, new_data):
        self._save_data(new_data)

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
