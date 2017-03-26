import cards
import decks
import players
import safe_input
from utils import Colors
from utils import pretty_print_as_supermarket_list

""" THE MODULE.
This modules defines an init the Game class, the king of all this project.
The game object is a singleton which coordinates all the actions between decks,
cards and players, which hold references to it.
"""

# thank you tuples for being inmutable we should all learn from you
COLORS = (Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW)

class Game:
    def __init__(self):
        self.main_deck = decks.MainDeck()
        self.discarded_deck = decks.DiscardedDeck()
        self.cards_to_forcibly_take = 0
        self.game_going_right = True
        self.forcibly_skip_next_turn = False
        self.special_active_color = None

        self.players = []
        self._create_players()
        self._fill_main_deck()
        self._inital_deal_cards()
        self._activate_last_card_on_discarded_deck()
        self._play_game()

    def _fill_main_deck(self):
        """Fills the main deck with the corresponding cards."""

        # fill the deck up with normal cards. weird range index to avoid
        # unnecesary ifs to comply with non-zero cards appearing twice per color
        # but zero-cards only once per color :)
        for n in range(1, 20):
            n = n % 10
            for color in COLORS:
                self.main_deck.add(cards.NormalCard(self, n, color))

        # the special colored cards, two per color
        for _ in range(2):
            for color in COLORS:
                self.main_deck.add(cards.SkipPlayerCard(self, color))
                self.main_deck.add(cards.ChangeDirectionCard(self, color))
                self.main_deck.add(cards.Take2Card(self, color))

        # and the special not-colored ones
        for _ in range(4):
            self.main_deck.add(cards.Take4Card(self))
            self.main_deck.add(cards.Take8Card(self))
            self.main_deck.add(cards.ChangeColor(self))

    def _create_players(self):
        """Add players to the game. At least one human and one AI. Human
        can choose up to two extra AI players."""
        self.players.append(players.HumanPlayer(self, "You"))
        self.players.append(players.AIPlayer(self, "AI 1"))
        print("An AI has been already created and added to the game.")
        for n in range(2,4):
            want_to_add_ai_player = safe_input.want_to_add_ai_player()
            if want_to_add_ai_player:
                self.players.append(players.AIPlayer(self, "AI {0}".format(n)))
            else:
                break

    def _inital_deal_cards(self):
        """Shuffle and deal seven cards to each player found on the game.
        Takes one card from the main deck and adds it to the discarded deck.
        """
        self.main_deck.shuffle()
        for player in self.players:
            cards = self.main_deck.take_multiple(7)
            player.hand.add_multiple_cards(cards)
        self.discarded_deck.add(self.main_deck.take())

    def _activate_last_card_on_discarded_deck(self):
        """Causes the last card on the discarded deck to do its effect."""
        last_card = self.discarded_deck.check()
        last_card.do_effect()

    def _add_or_remove(self, n, how_much=1):
        """Adds or remove 1 from n depending on wether the game is going
        left or right.
        """
        return n+how_much if self.game_going_right else n-how_much

    def _grab_players_response_cards(self, player):
        take_2 = list(filter(lambda card: isinstance(card, cards.Take2Card), player.hand.cards))
        take_4 = list(filter(lambda card: isinstance(card, cards.Take4Card), player.hand.cards))
        take_8 = list(filter(lambda card: isinstance(card, cards.Take8Card), player.hand.cards))
        if take_8:
            return take_8
        elif take_4:
            return take_4
        elif take_2:
            return list(filter(lambda card: card.is_compatible_with(self.discarded_deck.check()), take_2))
        else:
            return []

    def react_empty_deck(self):
        """When the main deck is empty, fill it up with cards from the discarded
        deck. When this method is finished, the main deck will have all
        the cards from the discarded deck except the topmost, which will still
        be in the discarded deck, and the main deck will be shuffled.
        """
        last_card = self.discarded_deck.take()
        self.main_deck = self.discarded_deck
        self.main_deck.shuffle()
        self.discarded_deck = decks.DiscardedDeck()
        self.discarded_deck.add(last_card)

    def make_player_grab_cards(self, player):
        """Responds to the special Take2 or Take4 cards. If player can respond
        to this card, the sensible option to automatically respond to it will
        be chosen automatically. Else, he will have to grab as many cards
        as necessary."""
        player_special_cards = self._grab_players_response_cards(player)
        if player_special_cards:
            player.play_specific_card(player_special_cards[0])
            return True
        else:
            player.grab_n_from_deck(self.cards_to_forcibly_take)
            self.cards_to_forcibly_take = 0
            return False

    def victory(self, winning_player):
        """Prints the victory messages."""
        print("** VICTORY ** \t" * 3)
        print("The winning player was: {0}".format(winning_player))
        print("This are the hands of the rest of the players: ")
        for player in self.players:
            pretty_print_as_supermarket_list("Hand of {0}".format(player), *player.hand.cards)
        print("Thank you for playing!")

    def _print_player_HUD(self, active_player):
        """Prints information for the user on each turn."""
        print()
        print("TURN OF: {0}".format(active_player))
        print("TOP CARD: {0}".format(str(self.discarded_deck.check()).upper()))
        print("============================================")

    def _play_game(self):
        """Starts the game itself. A continous loop that will only break
        when a player wins.
        """
        n = 0
        while True:
            if self.main_deck.is_empty:
                self.react_empty_deck()

            if self.forcibly_skip_next_turn:
                n = self._add_or_remove(n)
                self.forcibly_skip_next_turn = False
                continue

            active_player = self.players[n % len(self.players)]
            self._print_player_HUD(active_player)

            if self.cards_to_forcibly_take:
                self.make_player_grab_cards(active_player)
                n = self._add_or_remove(n)
                continue

            active_player.play_card()

            if active_player.hand.is_empty():
                self.victory(active_player)
                break
            n = self._add_or_remove(n)
            a = input("Press return to advance to next turn. \n")


if __name__ == '__main__':
    Game()
