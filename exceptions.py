"""Some exceptions used on the game.  """

class WrongUserInput(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return ("Program failed because the input was wrong. The suspected reason is "
                "{0}".format(self.reason))

class DeckError(Exception):
    def __init__(self):
        pass

class CantTakeFromEmptyDeck(DeckError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "You can't take a card from an empty deck!"

class CantCheckEmptyDeck(DeckError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "You can't check the last card of an empty deck!"

class CantTakeFromDiscardedDeck(DeckError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "You can't take from the discarded deck!"

class GameError(Exception):
    def __init__(self):
        pass

class CantUseThisCard(GameError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return ("You can't use this card right now!")
