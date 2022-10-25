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
    game.startRound()
    firstPlayerTopCard = game.showTopCard(firstPlayerDeck)
    attackTypes = game.getAttackerTypes()
    firstPlayerAttacking = game.firstPlayerAttacking
    #gameOver = false
    secondPlayerTopCard = game.showTopCard(secondPlayerDeck)
    firstPlayerCounter, secondPlayerCounter = game.showNumberOfCardsPlayerDeck()
    return render_template('pokeGame.html', firstPlayerTopCard=firstPlayerTopCard,
                           secondPlayerTopCard=secondPlayerTopCard, firstPlayerCounter=firstPlayerCounter,
                           secondPlayerCounter=secondPlayerCounter, firstPlayerAttacking=firstPlayerAttacking,
                           attackTypes=attackTypes)

@pokeGameBlueprint.route("/cycleCard/<playerDeck>")
def showCard(playerDeck):
    game = Game.instance()
    deck = getattr(game, f"{playerDeck}")
    game.cyclePlayerDeck(deck)
    topCard = game.showTopCard(deck)
    return json.dumps(topCard)

@pokeGameBlueprint.route("/updateCardCounter/")
def cardCounter():
    game = Game.instance()
    cardCounts = game.showNumberOfCardsPlayerDeck()
    return json.dumps(cardCounts)


@pokeGameBlueprint.route("/attack/<attackType>")
def attack(attackType):
    game = Game.instance()
    attackType = attackType.lower()
    print(game.attacker)
    damage, hp = game.attack(attackType)
    print(game.attacker)
    print(game.firstPlayerAttacking)
    return json.dumps([damage, hp])


@pokeGameBlueprint.route("/renderCards")
def cardUI():
    game = Game.instance()
    gameCardUI = render_template('gameCardUI.html')
    return render_template(gameCardUI, firstPlayerAttacking=game.firstPlayerAttacking)
