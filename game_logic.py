import random

class Card:
    def __init__(self, value):
        self.value = value
        self.is_open = False
        self.is_matched = False

    def open_card(self):
        if not self.is_matched:
            self.is_open = True

    def mark_as_matched(self):
        self.is_matched = True
        self.is_open = True

class MemoryGame:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.total_cards = rows * cols
        self.total_pairs = self.total_cards // 2
        self.cards = []
        self.opened_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.is_game_finished = False
        self.create_cards()

    def create_cards(self):
        symbols = [f"{i}.jpg" for i in range(1, 19)]
        needed_symbols = symbols[:self.total_pairs]
        values = needed_symbols * 2
        random.shuffle(values)
        self.cards = [Card(value) for value in values]