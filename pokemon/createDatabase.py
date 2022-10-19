import sqlite3
from sqlite3 import Error
from pokeClass import Pokemon
from downloadPokemon import FetchData
import logging


class PokeDatabase:

    def __init__(self):

        try:
            self.conn = sqlite3.connect('pokemonDatabase.db')
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()

    def downloadData(self):
        truncTable = 'DELETE FROM Pokemon;'
        self.cursor.execute(truncTable)
        self.conn.commit()
        self.insertPokeData()

    def insertPokeData(self):
        grabData = FetchData()
        pokeDict = grabData.fetchdata()

        for pokemon in pokeDict:
            if len(pokeDict[pokemon]["types"]) == 2:
                pokeDict[pokemon]["types"] = f'{pokeDict[pokemon]["types"][0]}, {pokeDict[pokemon]["types"][1]}'
            else:
                pokeDict[pokemon]["types"] = pokeDict[pokemon]["types"][0]

            insertPokemon = f'''
                INSERT INTO Pokemon
                (Name, Image_URL, Attack, Defense, Types)
                VALUES (
                    '{pokemon}',
                    '{pokeDict[pokemon]["artwork"]}',
                    '{pokeDict[pokemon]["attack"]}',
                    '{pokeDict[pokemon]["defense"]}',
                    '{pokeDict[pokemon]["types"]}'
                    )

                    '''
            self.cursor.execute(insertPokemon)
            self.conn.commit()

    def createTable(self):

        SQLCommandPoke = '''
            CREATE TABLE IF NOT EXISTS Pokemon (
                Name TEXT,
                Image_URL TEXT,
                Attack Value INTEGER,
                Defense Value INTEGER,
                Types TEXT             
            )'''

        self.cursor.execute(SQLCommandPoke)
        self.conn.commit()

    def getPokeData(self, pokeName: str):

        findPoke = f'''
            SELECT *
            FROM Pokemon
            WHERE Name = '{pokeName}';
            '''

        self.cursor.execute(findPoke)
        pokemonDataList = self.cursor.fetchone()
        if pokemonDataList is not None:
            pokemon = Pokemon()
            pokemon.name = pokeName
            pokemon.url = pokemonDataList[1]
            pokemon.attackValue = pokemonDataList[2]
            pokemon.defenseValue = pokemonDataList[3]
            pokemon.types = pokemonDataList[4]
            if ", " in pokemon.types:
                type1 = pokemon.types.split(', ')[0]
                type2 = pokemon.types.split(', ')[1]
                pokemon.types = [type1, type2]
            else:
                pokemon.types = [pokemon.types]

            return pokemon
        return None

    def listOfPokeNames(self):

        listNames = f'''
            SELECT Name
            FROM Pokemon
            '''
        self.cursor.execute(listNames)

        list = self.cursor.fetchall()
        listOfPokeNames = []
        if len(list) != 0:
            for name in list:
                listOfPokeNames.append(name[0])
            return listOfPokeNames
        return None


    def createMainCardDeck(self):
        Pokemon = f'''
                    SELECT *
                    FROM Pokemon
                    WHERE Name IS NOT NULL;
                    '''
        self.cursor.execute(Pokemon)
        listPoke = self.cursor.fetchall()
        totalPokeFound = len(listPoke)

        if totalPokeFound != 0:

            if totalPokeFound == len(set(listPoke)):
                logging.info("No duplicates of pokemon found in deck")
            else:
                listDuplicatePokeNames = []
                for poke in listPoke:
                    name = poke[0]
                    listDuplicatePokeNames.append(name)
                for name in set(listDuplicatePokeNames):
                    listDuplicatePokeNames.remove(name)
                for name in listDuplicatePokeNames:
                    logging.info(f"Duplicate found for {name}")

                listPoke = list(set(listPoke))
                logging.info("Duplicates removed")

            deck = []
            for poke in listPoke:
                pokemon = {
                    "name": poke[0],
                    "url": poke[1],
                    "attack": poke[2],
                    "defense": poke[3],
                    "types": poke[4]
                }
                if ", " in pokemon["types"]:
                    type1 = pokemon["types"].split(', ')[0]
                    type2 = pokemon["types"].split(', ')[1]
                    pokemon["types"] = [type1, type2]
                deck.append(pokemon)
            return deck
        return None

