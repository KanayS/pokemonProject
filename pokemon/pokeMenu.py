from flask import render_template, Blueprint


pokeMenuBlueprint = Blueprint('pokeMenuURLs', __name__, )

@pokeMenuBlueprint.route("/pokeMenu")
def main():
    return render_template('pokeMenu.html')
