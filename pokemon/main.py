from flask import Flask
from pokedex import pokedexBlueprint
from pokeGame import pokeGameBlueprint
from pokeMenu import pokeMenuBlueprint
from pokeSetup import pokeSetupBlueprint

app = Flask(__name__)
app.register_blueprint(pokedexBlueprint)
app.register_blueprint(pokeGameBlueprint)
app.register_blueprint(pokeMenuBlueprint)
app.register_blueprint(pokeSetupBlueprint)

if __name__ == "__main__":
    app.run()
