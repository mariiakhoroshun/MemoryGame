import random

class Card:
    def __init__(self, value):
        self.value = value
        self.is_open = False
        self.is_matched = False