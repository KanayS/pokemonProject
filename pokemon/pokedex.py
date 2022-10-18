from flask import Flask, render_template, request
from createDatabase import PokeDatabase
import json
app = Flask(__name__)

@app.route("/")
def main():
    pokeDatabase = PokeDatabase()
    pokeList = pokeDatabase.listOfPokeNames()


    return render_template('pokedex.html', pokeList=pokeList)


@app.route("/getPokeCard/<pokeName>")
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


if __name__ == "__main__":
    pokeDatabase = PokeDatabase()
    pokeDatabase.insertPokeData()
    app.run()
