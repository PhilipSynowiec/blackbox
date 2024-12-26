from word_processor import WordProcessor
from flashcard_generator import FlashcardGenerator

processor = WordProcessor()
flashcards = FlashcardGenerator()

if __name__ == "__main__":
    while True:
        inp = input(">> ")
        if not inp:
            break
        if inp.startswith("process file "):
            path = inp.removeprefix("process file ").strip()
            processor.process_file(path)
        elif inp == "process words":
            processor.process_lines()
        elif inp == "generate flashcards":
            flashcards.create_flashcards()