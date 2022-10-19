from createDatabase import PokeDatabase
import random
import logging

logging.basicConfig(level=logging.INFO)


class Game:

    def __init__(self):

        database = PokeDatabase()
        self.mainDeck = database.createMainCardDeck()
        if self.mainDeck is not None:
            self.totalCards = len(self.mainDeck)
        else:
            self.totalCards = 0
        self.firstPlayerDeck = []
        self.secondPlayerDeck = []

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

        if len(self.firstPlayerDeck) > 0:
            totalFirstPlayerDeck = len(self.firstPlayerDeck)
        else:
            logging.info("Player 1 has no cards")

        if len(self.secondPlayerDeck) > 0:
            totalSecondPlayerDeck = len(self.secondPlayerDeck)
        else:
            logging.info("Player 2 has no cards")

        return totalFirstPlayerDeck, totalSecondPlayerDeck

    # def cyclePlayerDeck(self):
    #
    #

if __name__ == "__main__":
    data = PokeDatabase()
    game = Game()
    game.shuffleMainDeck()
    game.divideMainDeckEvenly()
    [firstPlayer, secondPlayer] = game.divideMainDeckEvenly()
    totalFirstPlayer = game.showNumberOfCardsPlayerDeck()[0]
    print(totalFirstPlayer)
    firstPlayer.remove(firstPlayer[0])
    totalFirstPlayer = game.showNumberOfCardsPlayerDeck()[0]
    print(totalFirstPlayer)
