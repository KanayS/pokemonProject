import requests
import json
import logging

logging.basicConfig(filename='pokemon.log', filemode='w', level=logging.DEBUG, force=True)

def fetchTypes():

    try:
        TYPE_DATA_URL = "https://pokeapi.co/api/v2/type/"
        UNRESPONSIVE_URL = "https://abcd"
        content = requests.get(TYPE_DATA_URL)
        typeJson = json.loads(content.text)

    except requests.exceptions.ConnectionError:
        logging.error("Error in URL, cannot get type data.")
        typeJson = None

    if typeJson is not None:
        damageTypesDict = {}
        typeDict = typeJson["results"]
        for typeDamage in typeDict:
            typeDamageName = typeDamage["name"]
            typeDamageContent = requests.get(typeDamage["url"])
            damageJson = json.loads(typeDamageContent.text)
            damageRelations = damageJson["damage_relations"]
            dictDamage = {}
            for damageType, pokeType in damageRelations.items():
                listTypeNames = []
                for pokeTypeName in pokeType:
                    name = pokeTypeName["name"]
                    listTypeNames.append(name)

                strTypeNames = ' '.join([str(elem) for elem in listTypeNames])
                dictDamage[damageType] = strTypeNames
            damageTypesDict[typeDamageName] = dictDamage
        return damageTypesDict
    return None




if __name__ == '__main__':
    damage = fetchTypes()

    print()
