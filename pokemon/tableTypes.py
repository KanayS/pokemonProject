from flask import Flask, render_template, Blueprint
from pokeTypes import Damage
import json

app = Flask(__name__)


@app.route("/")
def tableTypes():
    damage = Damage()
    typesData, colourDict = damage.makeDamageTable()

    return render_template('table.html', typesData=typesData, typeColour=colourDict)
@app.route("/getPokeType/<pokeType>")
def getPokeType(pokeType):
    damage = Damage()
    typesData, colourDict = damage.makeDamageTable()
    typesData = typesData[pokeType]
    typeColour = colourDict[pokeType]
    typeName = pokeType
    return render_template('tableEdit.html', typesData=typesData, typeColour=typeColour, typeName=typeName)
@app.route("/fullTable")
def showFullTable():
    damage = Damage()
    typesData, colourDict = damage.makeDamageTable()

    return render_template('fullTable.html', typesData=typesData, typeColour=colourDict)

if __name__ == '__main__':
    app.run()
