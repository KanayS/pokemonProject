from flask import Flask
from pokedex import pokedexBlueprint

app = Flask(__name__)
app.register_blueprint(pokedexBlueprint)
if __name__ == "__main__":
    app.run()
