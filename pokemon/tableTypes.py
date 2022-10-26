from flask import Flask, render_template, Blueprint
from pokeTypes import Damage
from gamePageBackEnd import Game
import json

app = Flask(__name__)


@app.route("/")
def tableTypes():
    damage = Damage()
    typesData, colourDict = damage.makeDamageTable()


    return render_template('table.html', typesData=typesData, typeColour=colourDict)


if __name__ == '__main__':
    app.run()
