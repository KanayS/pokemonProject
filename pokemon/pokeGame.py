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
    firstPlayerAttacking = game.firstPlayerAttacking
    gameStage = game.gameStage
    damage, hp = game.attack(attackType)
    if hp <= 0:
        hp = "Fainted"
    return json.dumps([damage, hp, firstPlayerAttacking, gameStage])

@pokeGameBlueprint.route("/showInitialCard/<playerDeck>")
def showInitialCard(playerDeck):
    game = Game.instance()
    deck = getattr(game, f"{playerDeck}")
    topCard = game.showTopCard(deck)
    return json.dumps(topCard)


@pokeGameBlueprint.route("/renderCardButtons/")
def cardUI():
    game = Game.instance()
    attackTypes = game.getAttackerTypes()
    return render_template("gameCardUI.html", firstPlayerAttacking=game.firstPlayerAttacking, attackTypes=attackTypes)

@pokeGameBlueprint.route("/winCheck/")
def winCheck():
    game = Game.instance()
    gameOver = game.winCheck()
    firstPlayerTopCard = game.firstPlayerCard
    secondPlayerTopCard = game.secondPlayerCard
    attackTypes = game.getAttackerTypes()
    firstPlayerAttacking = game.firstPlayerAttacking
    firstPlayerCounter, secondPlayerCounter = game.showNumberOfCardsPlayerDeck()
    roundInfoDict = {
        "gameOver": gameOver,
        "beginningPlayerTopCard": "",
        "attackTypes": attackTypes,
        "firstPlayerAttacking": firstPlayerAttacking,
        "firstPlayerCounter": firstPlayerCounter,
        "secondPlayerCounter": secondPlayerCounter
    }
    if firstPlayerAttacking:
        roundInfoDict["beginningPlayerTopCard"] = firstPlayerTopCard
    else:
        roundInfoDict["beginningPlayerTopCard"] = secondPlayerTopCard
    return json.dumps(roundInfoDict)
