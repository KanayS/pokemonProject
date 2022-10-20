from unittest import TestCase
from pokemon.gamePageBackEnd import Game

game_empty = Game('../pokemon/pokemonDatabase.db')
game_empty.mainDeck = None
game_empty.totalCards = 0

class TestGame(TestCase):

    @staticmethod
    def test_shuffleMainDeckMainDeckEmpty():
        gameShuffleEmpty = Game('../pokemon/pokemonDatabase.db')
        gameShuffleEmpty.mainDeck = None
        gameShuffleEmpty.shuffleMainDeck()

        assert gameShuffleEmpty.mainDeck is None

    @staticmethod
    def test_divideMainDeckEvenlyIfEmpty():
        gameDivideEvenEmpty = Game('../pokemon/pokemonDatabase.db')
        gameDivideEvenEmpty.mainDeck = None
        gameDivideEvenEmpty.shuffleMainDeck()

        gameDivideEvenEmpty.divideMainDeckEvenly()

        assert gameDivideEvenEmpty.firstPlayerDeck is None
        assert gameDivideEvenEmpty.secondPlayerDeck is None

    @staticmethod
    def test_divideMainDeckUnevenlyIfEmpty():
        gameDivideUnevenEmpty = Game('../pokemon/pokemonDatabase.db')
        gameDivideUnevenEmpty.mainDeck = None
        gameDivideUnevenEmpty.shuffleMainDeck()

        gameDivideUnevenEmpty.divideMainDeckUnevenly(30)

        assert gameDivideUnevenEmpty.firstPlayerDeck is None
        assert gameDivideUnevenEmpty.secondPlayerDeck is None

    @staticmethod
    def test_cyclePlayerDeckIfEmpty():

        gameCycleEmpty = Game('../pokemon/pokemonDatabase.db')
        gameCycleEmpty.mainDeck = None
        gameCycleEmpty.cyclePlayerDeck()

        assert gameCycleEmpty.firstPlayerDeck is None
        assert gameCycleEmpty.secondPlayerDeck is None


    @staticmethod
    def showNumberOfCardsIfPlayerDecksEmptySplitEven():

        gameShowCardsEmpty = Game('../pokemon/pokemonDatabase.db')
        totalFirstPlayer = gameShowCardsEmpty.showNumberOfCardsPlayerDeck()[0]
        totalSecondPlayer = gameShowCardsEmpty.showNumberOfCardsPlayerDeck()[2]

        assert totalFirstPlayer == 0
        assert totalSecondPlayer == 0


    @staticmethod
    def test_divideMainDeckUnevenly():
        gameDivideEven = Game('../pokemon/pokemonDatabase.db')
        gameDivideEven.divideMainDeckUnevenly(30)

        assert len(gameDivideEven.firstPlayerDeck) == 30
        assert len(gameDivideEven.secondPlayerDeck) == 121

    @staticmethod
    def test_divideMainDeckUnevenlyIfSplitExceeds():
        gameDivideSplit = Game('../pokemon/pokemonDatabase.db')

        gameDivideSplit.divideMainDeckUnevenly(160)

        assert gameDivideSplit.firstPlayerDeck is None
        assert gameDivideSplit.secondPlayerDeck is None

if __name__ == '__main__':
    TestCase()


