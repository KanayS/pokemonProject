from flask import Flask, render_template, Blueprint
from createDatabase import PokeDatabase
from gamePageBackEnd import Game
import json

pokeSetupBlueprint = Blueprint('pokeSetupURLs', __name__, )


@pokeSetupBlueprint.route("/pokeSetup")
def main():
    return render_template('pokeSetup.html')
