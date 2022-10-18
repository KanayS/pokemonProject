import requests
import json


class FetchData:
    def fetchdata(self):

        DATA_URL = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151"
        content = requests.get(DATA_URL)
        parsedJson = json.loads(content.text)

        dict = {}

        pokemons = parsedJson["results"]

        for pokemon in pokemons:
            pokemonName = pokemon["name"]
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
        return dict
