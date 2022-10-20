from createDatabase import PokeDatabase
import random
import logging

logging.basicConfig(level=logging.INFO)


class Game:

    _instance = None

    def __init__(self):      
        self.totalCards = None
        self.mainDeck = None
        raise RuntimeError('Call instance() instead')       

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls._instance.initialise()
        return cls._instance

    def initialise(self):
        database = PokeDatabase()  # what is this???????
        self.mainDeck = database.createMainCardDeck()
        if self.mainDeck is not None:
            self.totalCards = len(self.mainDeck)
        else:
            self.totalCards = 0
        self.firstPlayerDeck = None
        self.secondPlayerDeck = None

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
            self.firstPlayerDeck = None
            self.secondPlayerDeck = None
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

        totalFirstPlayerDeck = 0
        totalSecondPlayerDeck = 0

        if self.firstPlayerDeck is not None:
            totalFirstPlayerDeck = len(self.firstPlayerDeck)
        else:
            logging.info("Player 1 has no cards")

        if self.secondPlayerDeck is not None:
            totalSecondPlayerDeck = len(self.secondPlayerDeck)
        else:
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
