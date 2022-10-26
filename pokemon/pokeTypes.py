import requests
import json
import logging
import sqlite3
from sqlite3 import Error

class Damage:

    def __init__(self, databasePath: str = 'pokemonDamageTypes.db'):
        logging.basicConfig(filename='pokemon.log', filemode='w', level=logging.DEBUG, force=True)
        self.damageTypesDict = {}
        try:
            self.conn = sqlite3.connect(databasePath)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()
        self.downloadData()
        self.damageValues = {'doubleDamageFrom': 2,
                             'doubleDamageTo': 2,
                             'halfDamageFrom': 0.5,
                             'halfDamageTo': 0.5,
                             'noDamageFrom': 0,
                             'noDamageTo': 0}
        self.damage = 1
        self.damageDone = []

    def __fetchTypes(self):

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
        damageData = self.__fetchTypes()
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

    def findDamage(self, attackerType):

        data = f'''
        SELECT *
        FROM TypeDamage
        WHERE Type == '{attackerType}';
        '''
        self.cursor.execute(data)
        data = self.cursor.fetchone()
        attackData = []
        for damage in data:
            damageType = damage.split()
            attackData.append(damageType)
        return attackData

    def makeDamageTable(self):
        data = 'SELECT Type FROM TypeDamage'
        self.cursor.execute(data)
        typeData = self.cursor.fetchall()
        typeList = []
        typeColor = ["#26de81",
                        "#ffeaa7",
                        "#fed330",
                        "#FF0069",
                        "#30336b",
                        "#f0932b",
                        "#81ecec",
                        "#00b894",
                        "#EFB549",
                        "#a55eea",
                        "#74b9ff",
                        "#95afc0",
                        "#6c5ce7",
                        "#a29bfe",
                        "#2d3436",
                        "#0190FF",
                        "#95afc0",
                        "#6c5ce7",
                        ]
        for types in typeData[:-2]:
            typeList.append(types[0])

        colourDict = {}
        for types in typeList:
            index = typeList.index(types)
            colourDict[types] = typeColor[index]

        tableData = {}
        for type in typeList:
            listForTable = [None] * len(typeList)
            damageData = self.findDamage(type)[2::2]

            for damageList in damageData:
                if len(damageList) != 0:
                    for damage in damageList:

                        damageIndex = damageData.index(damageList)
                        indexType = typeList.index(damage)

                        if damageIndex == 0:
                            damageValue = 2
                        elif damageIndex == 1:
                            damageValue = 0.5
                        else:
                            damageValue = 0

                        listForTable[indexType] = damageValue
            tableData[type] = listForTable

        return tableData, colourDict

# damage = Damage()
# damage.makeDamageTable()
#
#





