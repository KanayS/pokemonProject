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
    print(playerDeck)
    topCard = game.showTopCard(playerDeck)
    return json.dumps(topCard)

