from openai import OpenAI
from db import DB
from pydantic import BaseModel

class Entry(BaseModel):
    word: str
    grammatical_type: str
    cloze_sentence: str

class WordProcessor:
    def __init__(self, api_key,
                 db_path='database.json', prompt_file='prompt.txt'):
        self.client = OpenAI(api_key=api_key)
        self.db = DB(file_path=db_path)
        self.prompt = open(prompt_file, 'r').read()

    def _get_word_data(self, word, grammatical_type, cloze_sentence):
        if word:
            if (grammatical_type and cloze_sentence) or self.db.check_entry_exists(word, grammatical_type):
                self.db.add_entry(word, grammatical_type, cloze_sentence)
                return 0


        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": f"Word: {word}\nGrammatical type: {grammatical_type}\nCloze sentence: {cloze_sentence}"}
            ],
            response_format=Entry
        )

        response = completion.choices[0].message.parsed
        if not response:
            raise Exception("Wrong output format.")

        word = response.word if word is None else word
        cloze_sentence = response.cloze_sentence if cloze_sentence is None else cloze_sentence
        cloze_sentence = cloze_sentence.replace("} {", " ")
        grammatical_type = response.grammatical_type if grammatical_type is None else grammatical_type
        if grammatical_type == "v" and not word.startswith("to "):
            word = "to " + word
        self.db.add_entry(word, grammatical_type, cloze_sentence)

        return completion.usage.total_tokens

    def _format_line(self, line):
            word, grammatical_type, cloze_sentence = [c.strip() for c in line.split(';')]
            return word or None, grammatical_type or None, cloze_sentence or None

    def _fetch_words(self, path):
        with open(path, 'r') as f:
            for line in f.readlines():
                yield self._format_line(line)

    def process_file(self, path):
        estimated_cost = 0
        for word, grammatical_type, cloze_sentence in self._fetch_words(path):
            estimated_cost += ((self._get_word_data(word, grammatical_type, cloze_sentence) * 0.00015) // 1) / 100
            if estimated_cost > 1:
                print(f"File has not been fully processed. Estimated cost: {estimated_cost}$.")
                return
        print(f"File {path} has been processed. Estimated cost: {estimated_cost}$.")

    def process_lines(self):
        estimated_cost = 0
        while True:
            line = input("enter word >> ")
            if estimated_cost > 1 or not line:
                break
            word, grammatical_type, cloze_sentence = self._format_line(line)
            estimated_cost += ((self._get_word_data(word, grammatical_type, cloze_sentence) * 0.00015) // 1) / 100
        print(f"Estimated cost: {estimated_cost}$.")


# To run the class
if __name__ == "__main__":
    processor = WordProcessor()
    processor.run()
