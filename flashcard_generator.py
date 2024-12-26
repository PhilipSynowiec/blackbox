import genanki
import random
from db import DB

class FlashcardGenerator:
    def __init__(self, db_path='database.json'):
        self.db = DB(file_path=db_path)
        self.deck = genanki.Deck(
            1234567891,  # Deck-ID
            'Blackbox'
        )
        self.model = genanki.Model(
            1091735106,
            'Vocabulary',
            fields=[
                {'name': 'Word'},
                {'name': 'Grammatical type'},
                {'name': 'Cloze sentence'},
                {'name': 'Complete sentence'},
            ],
            templates=[{
                'name': 'Card 1',
                'qfmt': '{{Cloze sentence}}',
                'afmt': '{{Complete sentence}}'}],
            css=
            """
            .card {
              font-family: arial;
              font-size: 20px;
              text-align: center;
              color: black;
              background-color: white;
            }
            """
        )

    def create_flashcards(self, only_new=True):
        word_entries = self.db.get_all_entries()

        for entry in word_entries:
            if entry["anki_id"] is not None:
                if only_new:
                    continue
            else:
                entry["anki_id"] = random.randrange(1 << 30, 1 << 31)

            sentence = entry["cloze_sentence"].replace("}", "{").split("{")
            cloze = '...'.join([part for part in sentence][::2])
            complete = ''.join(sentence)

            note = genanki.Note(
                model=self.model,
                fields=[
                    entry["word"],
                    entry["grammatical_type"],
                    cloze,
                    complete
                ],
                guid=str(entry["anki_id"])
            )

            self.deck.add_note(note)

        self.db.set_all_entries(word_entries)
        genanki.Package(self.deck).write_to_file('Blackbox.apkg')
