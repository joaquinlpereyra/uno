import random
from exceptions import CantTakeFromEmptyDeck, CantCheckEmptyDeck

"""
Holds all the deck related classes.
Decks are thought of of mostly as stacks.
The DiscardedDeck is special in the sense that we (almost) never take from it,
we only keep adding stuff.

Class and methods don't have docstrings because of their simplistic nature.
"""

class Deck:
    def __init__(self):
        self.elems = []

    @property
    def is_empty(self):
        return len(self.elems) == 0

    def add(self, elem):
        self.elems.append(elem)
        elem.move(self)

    def take(self):
        if self.is_empty:
            raise CantTakeFromEmptyDeck

        card = self.elems.pop()
        card.move(None)
        return card

    def take_multiple(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.take())
        return cards

    def shuffle(self):
        random.shuffle(self.elems)

class DiscardedDeck(Deck):
    def __init__(self):
        Deck.__init__(self)

    def check(self):
        if self.is_empty:
            raise CantCheckEmptyDeck

        return self.elems[-1]

class MainDeck(Deck):
    def __init__(self):
        Deck.__init__(self)
