import requests
import json
import logging
import sqlite3
from sqlite3 import Error

logging.basicConfig(filename='pokemon.log', filemode='w', level=logging.DEBUG, force=True)


class Damage:

    def __init__(self, databasePath: str = 'pokemonDamageTypes.db'):
        self.damageTypesDict = {}
        try:
            self.conn = sqlite3.connect(databasePath)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()
        self.downloadData()

    def fetchTypes(self):

        try:
            TYPE_DATA_URL = "https://pokeapi.co/api/v2/type/"
            UNRESPONSIVE_URL = "https://abcd"
            content = requests.get(TYPE_DATA_URL)
            typeJson = json.loads(content.text)

        except requests.exceptions.ConnectionError:
            logging.error("Error in URL, cannot get type data.")
            typeJson = None

        if typeJson is not None:
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
                self.damageTypesDict[typeDamageName] = dictDamage
            return self.damageTypesDict
        return None

    def createTable(self):

        SQLCommandTypes = '''
            CREATE TABLE IF NOT EXISTS TypeDamage (
                Type TEXT,
                DoubleDamFrom TEXT,
                DoubleDamTo TEXT,
                HalfDamFrom TEXT,
                HalfDamTo TEXT,
                NoDamFrom TEXT,
                NoDamTo TEXT             
            )'''

        self.cursor.execute(SQLCommandTypes)
        self.conn.commit()

    def __insertTypeData(self):
        damageData = self.fetchTypes()
        noData = 'False'

        if damageData is not None:

            for pokeType, typeDamage in damageData.items():
                insertPokemon = f'''
                        INSERT INTO TypeDamage
                        (Type, DoubleDamFrom, DoubleDamTo, HalfDamFrom, HalfDamTo, NoDamFrom, NoDamTo)
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''

                self.cursor.execute(insertPokemon, (pokeType, typeDamage["double_damage_from"],
                                                    typeDamage["double_damage_to"],
                                                    typeDamage["half_damage_from"], typeDamage["half_damage_to"],
                                                    typeDamage["no_damage_from"], typeDamage["no_damage_to"]))
                self.conn.commit()
        else:
            logging.info("No data received from URL. Data could not be downloaded")
            noData = 'True'

        return noData

    def downloadData(self):
        tableEmpty = 'SELECT COUNT(*) FROM TypeDamage'
        self.cursor.execute(tableEmpty)
        ifEmpty = self.cursor.fetchone()[0]
        if ifEmpty != 20:
            truncTable = 'DELETE FROM TypeDamage;'
            self.cursor.execute(truncTable)
            self.conn.commit()
            return self.__insertTypeData()

    def findDamage(self, attacker, defender):
        data = f'''
        SELECT *
        FROM TypeDamage
        WHERE Type == '{attacker}';
        '''
        self.cursor.execute(data)
        attackData = self.cursor.fetchall()


if __name__ == '__main__':
    damage = Damage()
