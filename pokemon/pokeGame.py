from flask import Flask, render_template, Blueprint
from createDatabase import PokeDatabase
from gamePageBackEnd import Game
import json

pokeGameBlueprint = Blueprint('pokeGameURLs', __name__, )


@pokeGameBlueprint.route("/pokeGame/<gameMode>")
def pokeGame(gameMode):
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
    script = gameMode

    return render_template('pokeGame.html', firstPlayerTopCard=firstPlayerTopCard,
                           secondPlayerTopCard=secondPlayerTopCard, firstPlayerCounter=firstPlayerCounter,
                           secondPlayerCounter=secondPlayerCounter, firstPlayerAttacking=firstPlayerAttacking,
                           attackTypes=attackTypes, script=script)

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
    lAttackType = attackType.lower()
    firstPlayerAttacking = game.firstPlayerAttacking
    gameStage = game.gameStage
    damage, hp = game.attack(lAttackType)
    if hp <= 0:
        hp = "Fainted"
    return json.dumps([damage, hp, firstPlayerAttacking, gameStage, attackType])

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

@pokeGameBlueprint.route("/aiAttack/")
def aiAttack():
    game = Game.instance()
    attack = game.AIAttackAdvanced()
    return json.dumps(attack)

@pokeGameBlueprint.route("/victory/")
def victory():
    game = Game.instance()
    victor = game.victor
    return render_template('pokeVictory.html', victor=victor)
