import random
from urllib.request import Request, urlopen
import json
from PIL import Image
from io import BytesIO


class Pokemon:
    def __init__(self, name, level):
        self.url_paths = []
        self.name = name.title()
        self.id = -1
        self.level = level
        self.type = []
        self.power = self.calculate_power()

    def calculate_power(self):
        base_stats = self.calculate_base_stats()
        print(self.type)
        return base_stats

    def calculate_base_stats(self):
        # getting pokemon base stats
        url_path = 'https://pokeapi.co/api/v2/pokemon/' + self.name.lower()
        pokemon_content = load_page_json(url_path)
        #saving pokemon stats - id and types (url_paths are used to determine pokemon weaknesses
        self.id = pokemon_content['id']
        for poke_type in pokemon_content['types']:
            self.type.append(poke_type['type']['name'])
            self.url_paths.append(poke_type['type']['url'])
        return pokemon_content['stats'][0]['base_stat']

    def calculate_weaknesses(self, enemy):
        factor = 1
        print(self.url_paths)
        for url_path in self.url_paths:
            pokemon_content = load_page_json(url_path)
            print(pokemon_content)
            for double_dmg in pokemon_content['damage_relations']['double_damage_to']:
                if double_dmg['name'] in enemy.type:
                    if factor == 1 or factor == 0.5:
                        factor = factor * 2
            for half_dmg in pokemon_content['damage_relations']['half_damage_to']:
                if half_dmg['name'] in enemy.type:
                    if factor == 2 or factor == 1:
                        factor = factor / 2
            for no_dmg in pokemon_content['damage_relations']['no_damage_to']:
                if no_dmg['name'] in enemy.type:
                    factor = 0
        print(factor)
        return factor

    def fight(self, enemy):
        print(self.name)
        user_total_power = self.power * self.calculate_weaknesses(enemy)
        print(enemy.name)
        enemy_total_power = enemy.power * enemy.calculate_weaknesses(self)
        return self if user_total_power > enemy_total_power else enemy

    def list_types(self):
        result = self.type[0]
        if len(self.type) > 1:
            result += ', {}'.format(self.type[1])
        return result


def define_nature():
    url_path = 'https://pokeapi.co/api/v2/nature/' + str(random.randint(0, 24))
    pokemon_content = load_page_json(url_path)
    flavor = pokemon_content['likes_flavor']
    return flavor['name'], define_berry(flavor['url'])

def define_berry(url_path):
    if url_path is None:
        url_path = 'https://pokeapi.co/api/v2/berry-flavor/' + str(random.randint(0, 4))
    pokemon_content = load_page_json(url_path)
    berries = pokemon_content['berries']
    return berries[random.randint(0, len(berries))]['berry']['name']


def load_page_json(url_path):
    req = Request(url_path, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    return json.loads(webpage)


if __name__ == '__main__':
    pokemon = Pokemon('raichu', 10)