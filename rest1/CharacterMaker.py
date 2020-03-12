from urllib.request import Request, urlopen
import json
from PIL import Image
from io import BytesIO

url_paths = []


class Pokemon:
    def __init__(self, name, level):
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
        req = Request(url_path, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        pokemon_content = json.loads(webpage)
        #saving pokemon stats like id and types
        self.id = pokemon_content['id']
        for poke_type in pokemon_content['types']:
            self.type.append(poke_type['type']['name'])
            url_paths.append(poke_type['type']['url'])
        return pokemon_content['stats'][0]['base_stat']

    def calculate_weaknesses(self, enemy):
        factor = 1
        for url_path in url_paths:
            req = Request(url_path, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            pokemon_content = json.loads(webpage)
            for double_dmg in pokemon_content['damage_relations']['double_damage_to']:
                if double_dmg['name'] in enemy.type:
                    factor *= 2
            for half_dmg in pokemon_content['damage_relations']['half_damage_to']:
                if half_dmg['name'] in enemy.type:
                    factor /= 2
            for no_dmg in pokemon_content['damage_relations']['no_damage_to']:
                if no_dmg['name'] in enemy.type:
                    factor = 0
        return factor

    def get_sprite(self):#todo - displaying winning pokemon sprite (game image)
        url_path = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{}.png'.format(self.id)
        file = BytesIO(urlopen(url_path).read())
        img = Image.open(file)
        return img

    def fight(self, enemy):
        user_total_power = self.power * self.calculate_weaknesses(enemy)
        enemy_total_power =  enemy.power * enemy.calculate_weaknesses(self)
        return self if user_total_power > enemy_total_power else enemy

    def list_types(self):
        result = self.type[0]
        if len(self.type) > 1:
            result += ', {}'.format(self.type[1])
        return result


if __name__ == '__main__':
    pokemon = Pokemon('raichu', 10)