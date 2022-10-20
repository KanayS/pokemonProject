from unittest import TestCase
from pokemon.createDatabase import PokeDatabase


class TestPokeDatabase(TestCase):
    def test_create_main_card_deck(self):


        database = PokeDatabase('../pokemon/pokemonDatabase.db')

        insertExtraPoke = f'''
            INSERT INTO Pokemon
            (Name, Image_URL, Attack, Defense, Types)
            VALUES (
                'Bulbasaur',
                'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png',
                49,
                49,
                'grass, poison'
                )'''

        database.cursor.execute(insertExtraPoke)
        database.conn.commit()
        listNames = database.listOfPokeNames()
        mainDeck = database.createMainCardDeck()

        assert mainDeck[-1] != {'name': 'Bulbasaur',
                                'url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png',
                                'attack': 49,
                                'defense': 49,
                                'types': 'grass, poison'}
