import unittest
from unittest import TestCase
from pokemon.gamePageBackEnd import Game
from pokemon.pokeTypes import Damage


class TestGame(TestCase):

    def test_initialise(self):
        game = Game.instance()
        game.initialise('../pokemon/pokemonDatabase.db')

        assert game.totalCards == 10

    def test_shuffleMainDeckMainDeckEmpty(self):
        gameShuffleEmpty = Game.instance()
        gameShuffleEmpty.initialise('../pokemon/pokemonDatabase.db')
        gameShuffleEmpty.mainDeck = None
        gameShuffleEmpty.shuffleMainDeck()

        assert gameShuffleEmpty.mainDeck is None

    def test_divideMainDeckEvenlyIfEmpty(self):
        gameDivideEvenEmpty = Game.instance()
        gameDivideEvenEmpty.initialise('../pokemon/pokemonDatabase.db')
        gameDivideEvenEmpty.mainDeck = None
        gameDivideEvenEmpty.totalCards = 0
        gameDivideEvenEmpty.shuffleMainDeck()

        gameDivideEvenEmpty.divideMainDeckEvenly()

        assert gameDivideEvenEmpty.firstPlayerDeck is None
        assert gameDivideEvenEmpty.secondPlayerDeck is None

    def test_divideMainDeckUnevenlyIfEmpty(self):
        gameDivideUnevenEmpty = Game.instance()
        gameDivideUnevenEmpty.initialise('../pokemon/pokemonDatabase.db')
        gameDivideUnevenEmpty.mainDeck = None
        gameDivideUnevenEmpty.totalCards = 0
        gameDivideUnevenEmpty.shuffleMainDeck()

        gameDivideUnevenEmpty.divideMainDeckUnevenly(30)

        assert gameDivideUnevenEmpty.firstPlayerDeck is None
        assert gameDivideUnevenEmpty.secondPlayerDeck is None

    def test_divideMainDeckUnevenlyNotEmpty(self):
        gameDivideEven = Game.instance()
        gameDivideEven.initialise('../pokemon/pokemonDatabase.db')
        gameDivideEven.divideMainDeckUnevenly(7)

        assert len(gameDivideEven.firstPlayerDeck) == 7
        assert len(gameDivideEven.secondPlayerDeck) == 3

    def test_divideMainDeckUnevenlyIfSplitExceedsNotEmpty(self):
        gameDivideSplit = Game.instance()
        gameDivideSplit.initialise('../pokemon/pokemonDatabase.db')

        gameDivideSplit.divideMainDeckUnevenly(160)

        assert gameDivideSplit.firstPlayerDeck is None
        assert gameDivideSplit.secondPlayerDeck is None

    def test_cyclePlayerDeckIfEmpty(self):
        gameCycleEmpty = Game.instance()
        gameCycleEmpty.initialise('../pokemon/pokemonDatabase.db')
        gameCycleEmpty.mainDeck = None
        gameCycleEmpty.totalCards = 0
        firstPlayerDeck = gameCycleEmpty.divideMainDeckEvenly()[0]

        gameCycleEmpty.cyclePlayerDeck(firstPlayerDeck)

        assert gameCycleEmpty.firstPlayerDeck is None

    def test_cyclePlayerDeckNotEmpty(self):
        gameCycleNotEmpty = Game.instance()
        gameCycleNotEmpty.initialise('../pokemon/pokemonDatabase.db')

        PlayerDeck = gameCycleNotEmpty.divideMainDeckEvenly()[0]
        TopCard = PlayerDeck[0]
        originalDeck = PlayerDeck.copy()

        gameCycleNotEmpty.cyclePlayerDeck(PlayerDeck)
        BottomCard = PlayerDeck[-1]

        assert TopCard == BottomCard
        assert originalDeck[0] == BottomCard
        assert originalDeck[1] == PlayerDeck[0]

    def test_showNumberOfCardsIfPlayerDecksEmpty(self):
        gameShowCardsEmpty = Game.instance()
        gameShowCardsEmpty.initialise('../pokemon/pokemonDatabase.db')
        gameShowCardsEmpty.mainDeck = None
        gameShowCardsEmpty.totalCards = 0

        totalFirstPlayer = gameShowCardsEmpty.showNumberOfCardsPlayerDeck()[0]
        totalSecondPlayer = gameShowCardsEmpty.showNumberOfCardsPlayerDeck()[1]

        assert totalFirstPlayer == 0
        assert totalSecondPlayer == 0

    def test_showTopCardPlayerDeckEmpty(self):
        gameShowTopCardEmpty = Game.instance()
        gameShowTopCardEmpty.initialise('../pokemon/pokemonDatabase.db')
        firstPlayerDeckEmpty = gameShowTopCardEmpty.firstPlayerDeck

        gameShowTopCardEmpty.showTopCard(firstPlayerDeckEmpty)

        assert gameShowTopCardEmpty.topCard is None

    def test_showTopCardPlayerDeckNotEmpty(self):
        gameShowTopCardNotEmpty = Game.instance()
        gameShowTopCardNotEmpty.initialise('../pokemon/pokemonDatabase.db')

        firstPlayerDeckNotEmpty = gameShowTopCardNotEmpty.divideMainDeckEvenly()[0]
        TopCard = gameShowTopCardNotEmpty.showTopCard(firstPlayerDeckNotEmpty)

        assert TopCard == firstPlayerDeckNotEmpty[0]

    def test_getDamageIf0(self):
        gameGetDamageIf0 = Game.instance()
        gameGetDamageIf0.initialise('../pokemon/pokemonDatabase.db')
        gameGetDamageIf0.attacker = {'name': 'PokeAttacker', 'types': ['poison']}
        gameGetDamageIf0.defender = {'name': 'PokeDefender', 'types': ['ice']}
        damageMultiplierOneType = gameGetDamageIf0.getDamageMultiplier('poison')
        gameGetDamageIf0.defender = {'name': 'PokeDefenderTwo', 'types': ['grass', 'steel']}
        damageMultiplierTwoType = gameGetDamageIf0.getDamageMultiplier('poison')

        assert damageMultiplierOneType == 0
        assert damageMultiplierTwoType == 0

    def test_getDamageIfHalf(self):
        gameGetDamageIf0 = Game.instance()
        gameGetDamageIf0.initialise('../pokemon/pokemonDatabase.db')
        gameGetDamageIf0.attacker = {'name': 'PokeAttacker', 'types': ['normal']}
        gameGetDamageIf0.defender = {'name': 'PokeDefender', 'types': ['rock']}
        damageMultiplierOneType = gameGetDamageIf0.getDamageMultiplier('normal')

        assert damageMultiplierOneType == 0.5

    def test_startRoundEmptyDecks(self):
        gameStartRoundEmptyDecks = Game.instance()
        gameStartRoundEmptyDecks.initialise('../pokemon/pokemonDatabase.db')
        gameStartRoundEmptyDecks.startRound()

        assert gameStartRoundEmptyDecks.attacker is None
        assert gameStartRoundEmptyDecks.defender is None

    def test_startRoundIfFirst(self):
        gameStartRoundFirst = Game.instance()
        gameStartRoundFirst.initialise('../pokemon/pokemonDatabase.db')
        ##????

    def test_switchAttacker(self):
        gameswitchAttacker = Game.instance()
        gameswitchAttacker.initialise('../pokemon/pokemonDatabase.db')
        gameswitchAttacker.firstPlayerCard = 1
        gameswitchAttacker.secondPlayerCard = 2
        gameswitchAttacker.attacker = gameswitchAttacker.firstPlayerCard
        gameswitchAttacker.defender = gameswitchAttacker.secondPlayerCard

        gameswitchAttacker.switchAttacker()

        assert gameswitchAttacker.attacker == gameswitchAttacker.secondPlayerCard
        assert gameswitchAttacker.defender == gameswitchAttacker.firstPlayerCard

    def test_getAttackerTypes(self):
        gamegetAttackerTypes = Game.instance()
        gamegetAttackerTypes.initialise('../pokemon/pokemonDatabase.db')
        gamegetAttackerTypes.attacker = {'name': 'PokeAttacker', 'types': ['normal']}
        gamegetAttackerTypes.defender = {'name': 'PokeDefender', 'types': ['rock']}
        types = gamegetAttackerTypes.getAttackerTypes()

        assert types == ['normal']








if __name__ == '__main__':
    unittest.main()
