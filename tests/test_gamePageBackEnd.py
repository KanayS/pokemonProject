import unittest
from unittest import TestCase
from pokemon.gamePageBackEnd import Game
from math import ceil


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

    def test_getDamageTwoDefenseTypesNotZero(self):
        gameGetDamage = Game.instance()
        gameGetDamage.initialise('../pokemon/pokemonDatabase.db')
        gameGetDamage.attacker = {'name': 'PokeAttacker', 'types': ['normal']}
        gameGetDamage.defender = {'name': 'PokeDefender', 'types': ['rock', 'steel']}
        damageMultiplier = gameGetDamage.getDamageMultiplier('normal')

        assert damageMultiplier == 0.25

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
        gameAttackerTypes = Game.instance()
        gameAttackerTypes.initialise('../pokemon/pokemonDatabase.db')
        gameAttackerTypes.attacker = {'name': 'PokeAttacker', 'types': ['normal']}
        gameAttackerTypes.defender = {'name': 'PokeDefender', 'types': ['rock']}
        types = gameAttackerTypes.getAttackerTypes()

        assert types == ['normal']

    def test_attackerFirstPlayerDamage(self):
        gameDamage = Game.instance()
        gameDamage.initialise('../pokemon/pokemonDatabase.db')
        gameDamage.firstPlayerCard = {'name': 'Squirtle', 'url': '', 'attack': 48, 'defense': 65, 'hp': 32, 'types': ['grass', 'poison']}

        gameDamage.secondPlayerCard = {'name': 'Charmander', 'url': '', 'attack': 52, 'defense': 43, 'hp': 49, 'types': ['grass', 'poison']}
        gameDamage.secondPlayerHP = gameDamage.secondPlayerCard["hp"]

        gameDamage.attacker = gameDamage.firstPlayerCard
        gameDamage.defender = gameDamage.secondPlayerCard


        damage, secondPlayerHP = gameDamage.attack('grass')

        assert damage == 7.55
        assert secondPlayerHP == 41.45
        assert gameDamage.attacker == gameDamage.secondPlayerCard

    def test_loseRoundDeckNotEmpty(self):
        gameWinCheck = Game.instance()
        gameWinCheck.initialise('../pokemon/pokemonDatabase.db')

        gameWinCheck.firstPlayerDeck = [{'name': 'Primeape', 'url': '', 'attack': 105, 'defense': 60, 'types': ['fighting']},
                                        {'name': 'Bulbasaur', 'url': '', 'attack': 49, 'defense': 49, 'types': ['grass', 'poison']}]

        gameWinCheck.secondPlayerDeck = [{'name': 'Golbat', 'url': '', 'attack': 80, 'defense': 70, 'types': ['poison', 'flying']},
                                        {'name': 'Magnemite', 'url': '', 'attack': 35, 'defense': 70, 'types': ['electric', 'steel']}]
        firstPlayerCard = gameWinCheck.firstPlayerDeck[0]
        gameWinCheck.startRound()

        gameWinCheck.firstPlayerHP = 0
        gameOver = gameWinCheck.winCheck()

        assert gameOver is False
        assert gameWinCheck.loser == gameWinCheck.firstPlayerDeck
        assert gameWinCheck.winner == gameWinCheck.secondPlayerDeck
        assert gameWinCheck.secondPlayerDeck[-1] == firstPlayerCard
        assert gameWinCheck.attacker == gameWinCheck.secondPlayerDeck[0]
        assert gameWinCheck.defender == gameWinCheck.firstPlayerDeck[0]

    def test_pokeKilled(self):

        gameDamaged = Game.instance()
        gameDamaged.initialise('../pokemon/pokemonDatabase.db')
        gameDamaged.firstPlayerDeck = [{'name': 'Poke1', 'url': '', 'attack': 99, 'defense': 65, 'hp': 15, 'types': ['grass', 'poison']},
                                        {'name': 'Bulbasaur', 'url': '', 'attack': 49, 'defense': 49, 'types': ['grass', 'poison']}]

        gameDamaged.secondPlayerDeck = [{'name': 'Poke2', 'url': '', 'attack': 48, 'defense': 43, 'hp': 15, 'types': ['grass', 'poison']},
                                        {'name': 'Magnemite', 'url': '', 'attack': 35, 'defense': 70, 'types': ['electric', 'steel']}]
        gameDamaged.firstPlayerCard = gameDamaged.firstPlayerDeck[0]
        gameDamaged.secondPlayerCard = gameDamaged.secondPlayerDeck[0]
        secondPlayerCard = gameDamaged.secondPlayerCard
        gameDamaged.secondPlayerCard = gameDamaged.secondPlayerDeck[0]
        gameDamaged.secondPlayerHP = gameDamaged.secondPlayerCard["hp"]

        gameDamaged.attacker = gameDamaged.firstPlayerCard
        gameDamaged.defender = gameDamaged.secondPlayerCard

        damage, secondPlayerHP = gameDamaged.attack('grass')

        gameOver = gameDamaged.winCheck()

        assert secondPlayerHP <= 0 ## (based on randnum being 230)
        assert damage > 15
        assert gameOver is False
        assert gameDamaged.loser == gameDamaged.secondPlayerDeck
        assert gameDamaged.winner == gameDamaged.firstPlayerDeck
        assert gameDamaged.firstPlayerAttacking is True
        assert gameDamaged.firstPlayerDeck[-1] == secondPlayerCard
        assert gameDamaged.attacker == gameDamaged.firstPlayerDeck[0]
        assert gameDamaged.defender == gameDamaged.secondPlayerDeck[0]

    def testGameover(self):
        gameOver = Game.instance()
        gameOver.initialise('../pokemon/pokemonDatabase.db')
        gameOver.firstPlayerDeck = [
            {'name': 'Poke1', 'url': '', 'attack': 99, 'defense': 65, 'hp': 50, 'types': ['grass', 'poison']},
            {'name': 'Bulbasaur', 'url': '', 'attack': 100, 'defense': 49, 'hp': 5, 'types': ['ground']}]

        gameOver.secondPlayerDeck = [
            {'name': 'Poke2', 'url': '', 'attack': 48, 'defense': 20, 'hp': 10, 'types': ['grass', 'poison']},
            {'name': 'Magnemite', 'url': '', 'attack': 35, 'defense': 20, 'hp': 10, 'types': ['electric', 'steel']}]

        gameOver.startRound()
        gameOver.attacker = gameOver.firstPlayerCard
        gameOver.defender = gameOver.secondPlayerCard
        damage, secondPLayerHP = gameOver.attack('grass')
        print(damage)
        print(secondPLayerHP)
        gameOver.winCheck()
        damage2, secondPlayerHP2 = gameOver.attack('ground')
        print(damage2)
        print(secondPlayerHP2)
        endGame = gameOver.winCheck()

        assert endGame is True
        assert len(gameOver.secondPlayerDeck) == 0
        assert len(gameOver.firstPlayerDeck) == 4
        assert gameOver.firstPlayerDeck[2] == {'name': 'Poke2', 'url': '', 'attack': 48, 'defense': 20, 'hp': 10, 'types': ['grass', 'poison']}
        assert gameOver.firstPlayerDeck[3] == {'name': 'Magnemite', 'url': '', 'attack': 35, 'defense': 20, 'hp': 10, 'types': ['electric', 'steel']}

    def test_AIAdvanced(self):
        gameAI = Game.instance()
        gameAI.initialise('../pokemon/pokemonDatabase.db')
        gameAI.firstPlayerDeck = [{'name': 'Poke1', 'url': '', 'attack': 99, 'defense': 65, 'hp': 50, 'types': ['grass', 'poison']}]
        gameAI.secondPlayerDeck = [{'name': 'Poke2', 'url': '', 'attack': 48, 'defense': 20, 'hp': 10, 'types': ['rock']}]

        gameAI.attacker = gameAI.firstPlayerDeck[0]
        gameAI.defender = gameAI.secondPlayerDeck[0]
        chosenAttackType = gameAI.AIAttackAdvanced()

        assert chosenAttackType == 'grass'

    def test_AIAdvancedEqual(self):
        gameAI0 = Game.instance()
        gameAI0.initialise('../pokemon/pokemonDatabase.db')
        gameAI0.firstPlayerDeck = [
            {'name': 'Poke1', 'url': '', 'attack': 99, 'defense': 65, 'hp': 50, 'types': ['normal', 'fighting']}]
        gameAI0.secondPlayerDeck = [
            {'name': 'Poke2', 'url': '', 'attack': 48, 'defense': 20, 'hp': 10, 'types': ['ghost']}]

        gameAI0.attacker = gameAI0.firstPlayerDeck[0]
        gameAI0.defender = gameAI0.secondPlayerDeck[0]
        chosenAttackType = gameAI0.AIAttackAdvanced()

        assert chosenAttackType == 'normal'

if __name__ == '__main__':
    unittest.main()
