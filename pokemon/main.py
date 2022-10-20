from flask import Flask
from pokedex import pokedexBlueprint
from pokeGame import pokeGameBlueprint

app = Flask(__name__)
app.register_blueprint(pokedexBlueprint)
app.register_blueprint(pokeGameBlueprint)

if __name__ == "__main__":
    app.run()
