from flask import render_template, Blueprint
from createDatabase import PokeDatabase
import json


pokedexBlueprint = Blueprint('pokedexURLs', __name__, )


@pokedexBlueprint.route("/pokedex")
def main():
    pokeDatabase = PokeDatabase()
    pokeList = pokeDatabase.listOfPokeNames()
    return render_template('pokedex.html', pokeList=pokeList)


@pokedexBlueprint.route("/getPokeCard/<pokeName>")
def getPokeCard(pokeName):
    pokeDatabase = PokeDatabase()
    pokemon = pokeDatabase.getPokeData(pokeName)
    print(pokemon.name.title())

    pokeDict = {
        "name": pokemon.name.title(),
        "url": pokemon.url,
        "attack": pokemon.attackValue,
        "defense": pokemon.defenseValue,
        "types": pokemon.types
    }
    return json.dumps(pokeDict)


@pokedexBlueprint.route("/downloadData")
def downloadData():
    pokeDatabase = PokeDatabase()
    print("before")
    noData = pokeDatabase.downloadData()
    print("after")
    return noData


@pokedexBlueprint.route("/pokeList")
def pokeList():
    pokeDatabase = PokeDatabase()
    pokeList = pokeDatabase.listOfPokeNames()
    pokeListHTML = ""
    for pokemon in pokeList:
        pokeListHTML += f'<option value="{pokemon}">{pokemon}</option>'
    return pokeListHTML

