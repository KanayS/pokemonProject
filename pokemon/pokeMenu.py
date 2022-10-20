from flask import render_template, Blueprint


pokeMenuBlueprint = Blueprint('pokeMenuURLs', __name__, )

@pokeMenuBlueprint.route("/")
def main():
    return render_template('pokeMenu.html')
