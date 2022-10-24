from flask import Flask
from pokedex import pokedexBlueprint
from pokeGame import pokeGameBlueprint
from pokeMenu import pokeMenuBlueprint

app = Flask(__name__)
app.register_blueprint(pokedexBlueprint)
app.register_blueprint(pokeGameBlueprint)
app.register_blueprint(pokeMenuBlueprint)

if __name__ == "__main__":
    app.run()
