import random
import safe_input
import exceptions
from utils import pretty_print_as_supermarket_list

"""A module to hold Player and Hand, both deeply related classes"""

class Hand:
    """Represent a set of cards having an owner. Methods are pretty
    self explanatory.
    """
    def __init__(self, cards, owner):
        self._owner = owner
        self._cards = cards

    @property
    def owner(self):
        return self._owner

    @property
    def cards(self):
        return self._cards

    def add_card(self, card):
        self.cards.append(card)
        card.move(self)

    def add_multiple_cards(self, cards):
        [self.add_card(card) for card in cards]

    def remove_card(self, card):
        assert card in self.cards
        self.cards.remove(card)
        card.move(None)

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        hand_str = "Hand of player: {0}".format(self.owner)
        for card in self.cards:
            hand_str += " {0}\t".format(card)
        return hand_str

    def get_all_compatible_with(self, some_card):
        """Return all the cards in the hand which are compatible with
        some_card.
        """
        return [card for card in self.cards if card.is_compatible_with(some_card)]


class Player:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.hand = Hand([], self)

    def get_possible_plays(self):
        """Return all the cards the player can player in this turn."""
        return self.hand.get_all_compatible_with(self.game.discarded_deck.check())

    def grab_from_deck_because_has_no_compatible(self):
        """Forces the player to grab from the deck. Used mostly when the player
        can't play anything 'cause he has no compatible cards.
        If the card grabbed is compatible with the topmost card on the discarded deck,
        force the player to use it!.
        """
        card = self.game.main_deck.take()
        self.hand.add_card(card)
        if card.is_compatible_with(self.game.discarded_deck.check()):
            print("Player {0} plays the card she just grabbed!".format(self))
            print("That card was {0}".format(card))
            card.use()

    def grab_from_deck(self):
        """Makes the player grab one card from the deck."""
        return self.grab_n_from_deck(1)

    def grab_n_from_deck(self, n):
        """Makes the player grab n cards from the deck."""
        print("Player {0} grabs {1} card(s) from the deck!. So sad :(".format(self, n))
        for n in range(n):
            try:
                card = self.game.main_deck.take()
            except exceptions.CantTakeFromEmptyDeck:
                self.game.react_empty_deck()
                card = self.game.main_deck_take()
            finally:
                self.hand.add_card(card)

    def play_specific_card(self, card):
        """Make the player use the card card."""
        card.use()

    def __str__(self):
        return "{0}".format(self.name)


class HumanPlayer(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    def play_card(self):
        pretty_print_as_supermarket_list("Your hand", *self.hand.cards)
        possible_plays = self.get_possible_plays()
        if not possible_plays:
            print("You'll have to grab from the deck, you have no compatible cards!")
            self.grab_from_deck_because_has_no_compatible()
        else:
            print("Please choose a card to play: ")
            pretty_print_as_supermarket_list("Available cards", *possible_plays)
            which_card = safe_input.choose_card(possible_plays)
            self.play_specific_card(possible_plays[which_card])
            print("The card played was: {0}".format(possible_plays[which_card]))

class AIPlayer(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    def play_card(self):
        if not self.get_possible_plays():
            print("Player {0} has to grab from the deck, she has no compatible cards!".format(self))
            self.grab_from_deck_because_has_no_compatible()
        else:
            which_card = random.choice(self.get_possible_plays())
            self.play_specific_card(which_card)
            print("The card played was: {0}".format(which_card))
