import logging

import requests
import json
import logging

class FetchData:

    def __init__(self):

        logging.basicConfig(filename='pokemon.log', filemode='w', level=logging.DEBUG, force=True)
    def fetchdata(self):

        try:
            DATA_URL = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151"
            UNRESPONSIVE_URL = "https://abcd"
            content = requests.get(DATA_URL)
            parsedJson = json.loads(content.text)
        except requests.exceptions.ConnectionError:
            logging.error("Error in URL, cannot get pokemon data.")
            parsedJson = None

        if parsedJson is not None:

            dict = {}

            pokemons = parsedJson["results"]

            for pokemon in pokemons:
                pokemonName = pokemon["name"].title()
                pokemonURL = pokemon["url"]
                pokeContent = requests.get(pokemonURL)
                pokeJson = json.loads(pokeContent.text)
                attack = pokeJson["stats"][1]["base_stat"]
                defense = pokeJson["stats"][2]["base_stat"]
                artwork = pokeJson["sprites"]["other"]["official-artwork"]["front_default"]
                types = pokeJson["types"]
                listTypes = []
                for type in types:
                    listTypes.append(type["type"]["name"])
                dict[pokemonName] = {"artwork": artwork, "attack": attack, "defense": defense, "types": listTypes}
        else:
            dict = None

        return dict
