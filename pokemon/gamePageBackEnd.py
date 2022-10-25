from pokemon.createDatabase import PokeDatabase
import random
import logging
from pokeTypes import Damage


class Game:
    _instance = None

    def __init__(self):
        self.totalCards = None
        self.mainDeck = None
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            logging.basicConfig(filename='pokemon.log', level=logging.INFO, filemode='w', force=True)
            logging.info('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls._instance.initialise()
        return cls._instance

    def initialise(self, database='pokemonDatabase.db'):
        self.database = PokeDatabase(database)

        self.mainDeck = self.database.createMainCardDeck()
        if self.mainDeck is not None:
            self.totalCards = len(self.mainDeck)
        else:
            self.totalCards = 0
        self.firstPlayerDeck = None
        self.secondPlayerDeck = None
        self.topCard = None
        self.attacker = None
        self.defender = None
        self.typesToAttack = []
        self.firstPlayerHP = 100  # need to get these from API
        self.secondPlayerHP = 100  # need to get from API for each Poke
        self.firstPlayerCard = {}
        self.secondPlayerCard = {}
        self.round = 0
        self.winner = {}
        self.loser = {}
        self.gameOver = False
        self.firstPlayerAttacking = False

    def shuffleMainDeck(self):
        if self.mainDeck is not None:
            random.shuffle(self.mainDeck)
        else:
            logging.info("Main deck of cards is empty")

    def divideMainDeckEvenly(self):

        if self.totalCards != 0:
            index_split = round(self.totalCards / 2)
            self.firstPlayerDeck = self.mainDeck[:index_split]
            self.secondPlayerDeck = self.mainDeck[index_split:]
            logging.info(f"First player received {len(self.firstPlayerDeck)} cards. "
                         f"Second player received {len(self.secondPlayerDeck)}")
        else:
            logging.info("Main deck empty. Players have received no cards")
        return self.firstPlayerDeck, self.secondPlayerDeck

    def divideMainDeckUnevenly(self, split: int):

        if split < self.totalCards and self.totalCards != 0:

            self.firstPlayerDeck = self.mainDeck[:split]
            self.secondPlayerDeck = self.mainDeck[split:]
            logging.info(f"First player received {len(self.firstPlayerDeck)} cards. "
                         f"Second player received {len(self.secondPlayerDeck)}")
            return self.firstPlayerDeck, self.secondPlayerDeck
        else:
            logging.info("Requested number of cards to player 1 exceeds cards in deck")

    def showNumberOfCardsPlayerDeck(self):
        ###use in another method so that the number of cards is updated each time card added or removed

        if self.firstPlayerDeck is not None:
            totalFirstPlayerDeck = len(self.firstPlayerDeck)
        else:
            totalFirstPlayerDeck = 0
            logging.info("Player 1 has no cards")

        if self.secondPlayerDeck is not None:
            totalSecondPlayerDeck = len(self.secondPlayerDeck)
        else:
            totalSecondPlayerDeck = 0
            logging.info("Player 2 has no cards")

        return totalFirstPlayerDeck, totalSecondPlayerDeck

    def cyclePlayerDeck(self, list):
        if list is not None:
            self.topCard = list[0]
            list.remove(self.topCard)
            list.append(self.topCard)
        else:
            logging.info("Player deck is empty and cannot cycle")

    def showTopCard(self, list):
        if list is not None:
            self.topCard = list[0]
            return self.topCard
        else:
            logging.info("Player has no cards to show")

    def getDamageValue(self, attackerType: str) -> int:

        defenderTypes = self.defender['types']

        damageData = Damage()
        damageValues = damageData.damageValues

        attackerDamage = damageData.findDamage(attackerType)[1:]
        damageTotal = 1
        damageDone = []

        for defenderType in defenderTypes:
            listIndices = []
            for damageType in attackerDamage:
                if len(damageType) > 0:
                    for pokeType in damageType:
                        if defenderType == pokeType:
                            listIndices.append(attackerDamage.index(damageType))
            if len(listIndices) != 0:

                damageDone.append(True)

                for index in listIndices:

                    if index == 1:
                        damageTotal *= damageValues["doubleDamageTo"]

                    elif index == 3:
                        damageTotal *= damageValues["halfDamageTo"]

                    elif index == 5:
                        damageTotal = damageValues["noDamageTo"]

            else:
                damageDone.append(False)

        if damageDone == [True, True] or damageDone == [True]:
            damageTotal = 0

        return damageTotal

    def startRound(self):

        if self.firstPlayerDeck is not None and self.secondPlayerDeck is not None:

            self.firstPlayerCard = self.firstPlayerDeck[0]
            self.secondPlayerCard = self.secondPlayerDeck[0]

            if self.round == 0:

                choosePlayer = random.randint(1, 2)
                self.round += 1

                self.firstPlayerAttacking = True

                if choosePlayer == 1:
                    self.attacker = self.firstPlayerCard
                    self.defender = self.secondPlayerCard
                    logging.info(f"Player 1 chosen to attack first with {self.attacker['name']}")
                elif choosePlayer == 2:
                    self.attacker = self.secondPlayerCard
                    self.defender = self.firstPlayerCard
                    self.firstPlayerAttacking = False
                    logging.info(f"Player 2 chosen to attack first with {self.attacker['name']}")

            else:
                self.attacker = self.winner[0]
                self.defender = self.loser[0]

        else:
            logging.info("Decks are empty and game cannot start")

    def checkAttacker(self):
        if self.firstPlayerAttacking == True:
            attackingPlayer = 1
        elif self.firstPlayerAttacking == False:
            attackingPlayer = 2

        return attackingPlayer

    def switchAttacker(self):

        if self.attacker == self.firstPlayerCard:
            self.attacker = self.secondPlayerCard
            self.defender = self.firstPlayerCard
            self.firstPlayerAttacking = False

        else:
            self.attacker = self.firstPlayerCard
            self.defender = self.secondPlayerCard
            self.firstPlayerAttacking = True

    def getAttackerTypes(self):
        self.typesToAttack = self.attacker["types"]
        return self.typesToAttack

    def AIAttack(self):
        AITypes = self.getAttackerTypes()
        if len(AITypes) > 1:
            random.shuffle(AITypes)
        AIAttackType = AITypes[0]
        return AIAttackType

    def attack(self, attackType):  ##if statement for if the user needs to choose type from 2 or only 1 type
        attackValue = self.attacker["attack"]
        defenseValue = self.defender["defense"]
        multiplier = self.getDamageValue(attackType)
        damageDone = (attackValue - defenseValue) * multiplier
        if self.attacker == self.firstPlayerCard:
            self.secondPlayerHP -= damageDone
            self.switchAttacker()
            return damageDone, self.secondPlayerHP
        elif self.attacker == self.secondPlayerCard:
            self.firstPlayerHP -= damageDone
            self.switchAttacker()
            return damageDone, self.firstPlayerHP

    def __giveAwayCard(self, listFrom, listTo, card):
        listFrom.remove(card)
        listTo.append(card)

    def winCheck(self): ###after each attack -> damage/ HP caluclation

        if self.firstPlayerHP == 0:
            self.__giveAwayCard(self.firstPlayerDeck, self.secondPlayerDeck, self.firstPlayerCard)
            self.loser = self.firstPlayerDeck
            self.winner = self.secondPlayerDeck
            logging.info(f"Player 2 has won the round and taken {self.firstPlayerCard['name']} from Player 1")
            if len(self.loser) == 0:
                logging.info("Game is over. Player 2 has won the game")
                self.gameOver = True
            else:
                self.firstPlayerAttacking = False
                self.startRound()

        elif self.secondPlayerHP == 0:
            self.__giveAwayCard(self.secondPlayerDeck, self.firstPlayerDeck, self.secondPlayerCard)
            self.loser = self.secondPlayerDeck
            self.winner = self.firstPlayerDeck
            logging.info(f"Player 1 has won the round and taken {self.secondPlayerCard['name']} from Player 2")
            if len(self.loser) == 0:
                logging.info("Game is over. Player 1 has won the game")
                self.gameOver = True
            else:
                self.firstPlayerAttacking = True
                self.startRound()

        return self.gameOver


if __name__ == '__main__':
    pass







