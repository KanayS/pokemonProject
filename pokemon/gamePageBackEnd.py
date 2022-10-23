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

    def initialise(self, database = 'pokemonDatabase.db'):
        self.database = PokeDatabase(database)

        self.mainDeck = self.database.createMainCardDeck()
        if self.mainDeck is not None:
            self.totalCards = len(self.mainDeck)
        else:
            self.totalCards = 0
        self.firstPlayerDeck = None
        self.secondPlayerDeck = None
        self.topCard = None

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

    def getDamageValue(self, attackerType, defender):  ##assuming the type is known??
        ###card asks for parameters to be attacker and defender TYPES!

        defenderTypes = self.database.getPokeData(defender).types

        damageData = Damage()
        damageValues = damageData.DamageValues

        attackerDamage = damageData.findDamage(attackerType)[1:]
        damageTotal = 1

        for defenderType in defenderTypes:
            listIndices = []
            for damageType in attackerDamage:
                if len(damageType) > 0:
                    for pokeType in damageType:
                        if defenderType == pokeType:
                            listIndices.append(attackerDamage.index(damageType))
            if len(listIndices) != 0:
                for index in listIndices:

                    if index == 1:
                        damageTotal *= damageValues["doubleDamageTo"]

                    elif index == 3:
                        damageTotal *= damageValues["halfDamageTo"]

                    elif index == 5:
                        damageTotal = damageValues["noDamageTo"]
            else:
                damageTotal = 0

        return damageTotal

if __name__ == "__main__":
    game=Game.instance()
    game.initialise()
    damage = game.getDamageValue('dragon', 'Bulbasaur')
    print(damage)

