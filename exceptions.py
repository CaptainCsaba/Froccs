class GameException(Exception):
    """ Base exception for non-critical excetptions which could happen as part of the game. """

class NotEnoughMoneyException(GameException):
    pass

class PourDrinkInGlassException(GameException):
    pass

class MaximumGlassCountReached(GameException):
    pass

class CardDeckIsEmptyException(GameException):
    pass

class GlassPurchaseException(GameException):
    pass

class CardUsageException(GameException):
    pass

class GlassIndexException(GameException):
    pass

class PlayerIndexError(GameException):
    pass

class NoSuchActionException(GameException):
    pass

class NoSuchCardException(GameException):
    pass

class UserInputException(GameException):
    pass

class ActionException(GameException):
    pass