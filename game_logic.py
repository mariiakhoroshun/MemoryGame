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