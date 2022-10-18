import sqlite3
from sqlite3 import Error
from pokeClass import Pokemon
from downloadPokemon import FetchData


class PokeDatabase:

    def __init__(self):

        try:
            self.conn = sqlite3.connect('pokemon_database.db')
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()

    def downloadData(self):
        truncTable = 'TRUNCATE TABLE Pokemon;'
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

        sql_command_poke = '''
            CREATE TABLE IF NOT EXISTS Pokemon (
                Name TEXT,
                Image_URL TEXT,
                Attack Value INTEGER,
                Defense Value INTEGER,
                Types TEXT             
            )'''

        self.cursor.execute(sql_command_poke)
        self.conn.commit()

    def getPokeData(self, pokeName):

        no_poke = ''

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
                listOfPokeNames.append(name[0].title())
            return listOfPokeNames
        return None
