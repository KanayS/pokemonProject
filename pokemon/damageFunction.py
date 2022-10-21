import sqlite3
from sqlite3 import Error
from pokeTypes import fetchTypes
import logging


class DamageDatabase:

    def __init__(self, databasePath: str = 'pokemonDamageTypes.db'):

        try:
            self.conn = sqlite3.connect(databasePath)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()

    def createTable(self):

        SQLCommandTypes = '''
            CREATE TABLE IF NOT EXISTS TypeDamage (
                Type TEXT,
                DoubleDamFrom TEXT,
                DoubleDamTo TEXT,
                HalfDamFrom TEXT,
                HalfDamaTo TEXT,
                NoDamFrom TEXT,
                NoDamTo TEXT             
            )'''

        self.cursor.execute(SQLCommandTypes)
        self.conn.commit()

    def insertTypeData(self):
        damageData = fetchTypes()
        noData = 'False'

        if damageData is not None:

            for pokeType, typeDamage in damageData.items():
                insertPokemon = f'''
                        INSERT INTO TypeDamage
                        (Type, Double Damage From, Double Damage To, Half Damage From, Half Damage To, No Damage From, No Damage To)
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


if __name__ == '__main__':
    data = DamageDatabase()
    data.insertTypeData()
