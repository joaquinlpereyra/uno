import random
import safe_input
import players
from utils import Colors
from exceptions import CantUseThisCard


"""A module to hold all card-related classes.
The most interesting are base classes: Card, _ColoredCard, _SpecialColoredCard,
_SpecialCard.

Polymorphism is used extensively on SpecialCards (both colored and non-colored)
to affect the game.
"""

class Card:
    """A base class to represent all cards."""
    def __init__(self, game):
        """A Card is part of a particular game and has a Place: it is either
        on a Player's Hand or on one of the decks.
        """
        self._game = game
        self._place = None

    @property
    def owner(self):
        """Return the owner of the card, if it has one. If not, return None."""
        return self._place.owner if isinstance(self._place, players.Hand) else None

    @property
    def deck(self):
        """Return the deck of the card, if it has one. If not, return None."""
        return self._place if isinstance(self._place, Deck) else None

    @property
    def game(self):
        return self._game

    def is_compatible_with(self, another_card):
        """Should return wether the card is _compatible_ (that is, can be put
        above on the discarded stack) with another card."""
        raise NotImplementedError("Every Card should decide what is compatible with!")

    def use(self):
        """Remove the card from the hand of the owner and add it to the
        discarded_deck of the game. If it is a special card, apply its effects
        to the game as well.

        Raises CantUseThisCard error if the card is not compatible with the
        topmost card of the game's discarded deck.
        """
        if not self.is_compatible_with(self.game.discarded_deck.check()):
            raise CantUseThisCard

        self.do_effect()
        self.owner.hand.remove_card(self)
        self.game.discarded_deck.add(self)

    def move(self, somewhere):
        """Moves the card to somewhere. Somewhere should either be a
        player's hand or a deck.
        """
        self._place = somewhere

    def do_effect(self):
        pass

class _ColoredCard(Card):
    """A baseclass to represent all cards which have a color."""
    def __init__(self, game, color):
        Card.__init__(self, game)
        self._color = color

    # property decorator makes the color inmutable after creation :)
    # it is used extensively to create read-only properties
    @property
    def color(self):
        return self._color

    @property
    def number(self):
        # NOTE: this is useful so as to make compatibilities easily symmetric,
        # without the need to try/except all the methods.
        # all the cards with no numbers actually have a magic, impossible -1 value
        return -1

    def is_compatible_with(self, another_card):
        """Should return wether the card is _compatible_ (that is, can be put
        above on the discarded stack) with another card."""
        if self.game.special_active_color is not None:
            return self.color == self.game.special_active_color

        return self.color == another_card.color or \
               isinstance(another_card, _SpecialCard)

    def use(self):
        super().use()
        self.game.special_active_color = None

class _SpecialColoredCard(_ColoredCard):
    """A class to represent all cards which have special effects and have colors."""
    def __init__(self, game, color):
        _ColoredCard.__init__(self, game, color)

class _SpecialCard(Card):
    """A class to represent all cards which have special effects and dont have
    colors."""
    def __init__(self, game):
        Card.__init__(self, game)

    @property
    def color(self):
        return None

    @property
    def number(self):
        return -1

    def is_compatible_with(self, another_card):
        # a special card is compatible with everything, really
        return True

class NormalCard(_ColoredCard):
    def __init__(self, game, number, color):
        _ColoredCard.__init__(self, game, color)
        self._number = number

    @property
    def number(self):
        return self._number

    def is_compatible_with(self, another_card):
        if self.game.special_active_color is not None:
            return self.color == self.game.special_active_color

        return self.number == another_card.number or \
               self.color == another_card.color or \
               isinstance(another_card, _SpecialCard)

    def __str__(self):
        return "{0} {1}".format(self.color, self.number)

class SkipPlayerCard(_SpecialColoredCard):
    def __init__(self, game, color):
        _SpecialColoredCard.__init__(self, game, color)

    def do_effect(self):
        print("A Skip Player card has been played! Next player will be skipped.")
        self.game.forcibly_skip_next_turn = True

    def __str__(self):
        return "{0} Skip Player".format(self.color)

class ChangeDirectionCard(_SpecialColoredCard):
    def __init__(self, game, color):
        _SpecialColoredCard.__init__(self, game, color)

    def do_effect(self):
        print("A Change Direction card has been played! Game will go in reverse now.")
        self.game.game_going_right = not self.game.game_going_right

    def __str__(self):
        return "{0} Change Direction".format(self.color)

class Take2Card(_SpecialColoredCard):
    def __init__(self, game, color):
        _SpecialColoredCard.__init__(self, game, color)

    def is_compatible_with(self, another_card):
        if self.game.special_active_color is not None:
            return self.color == self.game.special_active_color

        return self.color == another_card.color or \
               isinstance(another_card, Take4Card) or \
               isinstance(another_card, Take2Card)

    def do_effect(self):
        print("A Take 2 card has been played! Next player will have to take {0} cards "
              "unless she can defend herself!".format(self.game.cards_to_forcibly_take+2))
        self.game.cards_to_forcibly_take += 2

    def __str__(self):
        return "{0} Take 2".format(self.color)

class Take4Card(_SpecialCard):
    def __init__(self, game):
        _SpecialCard.__init__(self, game)

    def do_effect(self):
        print("A Take 4 card has been played! Next player will have to take {0} cards "
              "unless she can defend herself!".format(self.game.cards_to_forcibly_take+4))
        self.game.cards_to_forcibly_take += 4

    def __str__(self):
        return "Take 4"

class Take8Card(_SpecialCard):
    def __init__(self, game):
        _SpecialCard.__init__(self, game)

    def do_effect(self):
        print("A Take 8 card has been played! Next player will have to take {0} cards "
              "unless she can defend herself!".format(self.game.cards_to_forcibly_take+8))
        self.game.cards_to_forcibly_take += 8

    def __str__(self):
        return "Take 8"

class ChangeColor(_SpecialCard):
    def __init__(self, game):
        _SpecialCard.__init__(self, game)
        self.colors = {'red': Colors.RED,
                       'yellow': Colors.YELLOW,
                       'green': Colors.GREEN,
                       'blue': Colors.BLUE
                        }

    def choose_color(self):
        color_chosen = safe_input.choose_color()
        return color_chosen

    def _do_effect(self, color_chosen):
        self.game.special_active_color = self.colors[color_chosen]
        print("A Change Color card has been played! The active color is now: {0}".format(color_chosen))

    def do_effect(self):
        if isinstance(self.owner, players.AIPlayer):
            self.do_ai_effect()
        else:
            color_chosen = self.choose_color()
            self._do_effect(color_chosen)

    def do_ai_effect(self):
        color_chosen = random.choice(list(self.colors.keys()))
        self._do_effect(color_chosen)

    def __str__(self):
        return "Change Color"
