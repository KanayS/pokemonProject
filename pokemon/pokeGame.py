from flask import Flask, render_template, Blueprint
from createDatabase import PokeDatabase
from gamePageBackEnd import Game
import json

pokeGameBlueprint = Blueprint('pokeGameURLs', __name__, )


@pokeGameBlueprint.route("/pokeGame")
def pokeGame():
    game = Game.instance()
    game.initialise()
    game.shuffleMainDeck()
    firstPlayerDeck, secondPlayerDeck = game.divideMainDeckEvenly()
    return render_template('pokeGame.html', firstPlayerDeck=firstPlayerDeck, secondPlayerDeck=secondPlayerDeck)

@pokeGameBlueprint.route("/showTopCard/<playerDeck>")
def showCard(playerDeck):
    game = Game.instance()
    deck = getattr(game, f"{playerDeck}")
    deck1 = game.firstPlayerDeck
    topCard = game.showTopCard(deck)

    print(topCard)

    return json.dumps(topCard)

