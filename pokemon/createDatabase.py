import sqlite3
from sqlite3 import Error
from pokemon.pokeClass import Pokemon
from pokemon.downloadPokemon import FetchData
import logging
import random


def splitString(string):
    if ", " in string:
        type1 = string.split(', ')[0]
        type2 = string.split(', ')[1]
        string = [type1, type2]
    else:
        string = [string]
    return string


class PokeDatabase:

    def __init__(self, databasePath: str = 'pokemonDatabase.db'):

        try:
            self.conn = sqlite3.connect(databasePath)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()

    def downloadData(self):
        truncTable = 'DELETE FROM Pokemon;'
        self.cursor.execute(truncTable)
        self.conn.commit()
        return self.__insertPokeData()

    def __insertPokeData(self):
        grabData = FetchData()
        self.pokeDict = grabData.fetchdata()
        noData = 'False'

        if self.pokeDict is not None:
            for pokemon in self.pokeDict:
                if len(self.pokeDict[pokemon]["types"]) == 2:
                    self.pokeDict[pokemon][
                        "types"] = f'{self.pokeDict[pokemon]["types"][0]}, {self.pokeDict[pokemon]["types"][1]}'
                else:
                    self.pokeDict[pokemon]["types"] = self.pokeDict[pokemon]["types"][0]

                insertPokemon = f'''
                    INSERT INTO Pokemon
                    (Name, Image_URL, Attack, Defense, Hp, Types)
                    VALUES (?, ?, ?, ?, ?, ?)'''

                self.cursor.execute(insertPokemon,
                                    (pokemon, self.pokeDict[pokemon]["artwork"], self.pokeDict[pokemon]["attack"],
                                     self.pokeDict[pokemon]["defense"], self.pokeDict[pokemon]["types"],
                                     self.pokeDict[pokemon]["hp"]))
                self.conn.commit()
        else:
            logging.info("No data received from URL. Data could not be downloaded")
            noData = 'True'

        return noData

    def createTable(self):

        SQLCommandPoke = '''
            CREATE TABLE IF NOT EXISTS Pokemon (
                Name TEXT,
                Image_URL TEXT,
                Attack INTEGER,
                Defense INTEGER,
                Hp INTEGER,
                Types TEXT             
            )'''

        self.cursor.execute(SQLCommandPoke)
        self.conn.commit()

    def getPokeData(self, pokeName: str):

        findPoke = f'''
            SELECT *
            FROM Pokemon
            WHERE Name = ?;
            '''

        self.cursor.execute(findPoke, (pokeName,))
        pokemonDataList = self.cursor.fetchone()
        if pokemonDataList is not None:
            pokemon = Pokemon()
            pokemon.name = pokeName
            pokemon.url = pokemonDataList[1]
            pokemon.attackValue = pokemonDataList[2]
            pokemon.defenseValue = pokemonDataList[3]
            pokemon.hp = pokemonDataList[5]
            pokemon.types = pokemonDataList[4]
            pokemon.types = splitString(pokemon.types)

            return pokemon
        return None

    def listOfPokeNames(self):  ###REMOVE DUPLICATES FROM LIST

        listNames = f'''
            SELECT Name
            FROM Pokemon
            ORDER BY Name ASC;            
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
                    "hp": poke[5],
                    "types": poke[4]
                }
                pokemon["types"] = [pokemon["types"]]
                pokemon["types"] = splitString(pokemon["types"][0])
                deck.append(pokemon)

            random.shuffle(deck)
            return deck[:10]
        return None
