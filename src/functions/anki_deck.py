import asyncio
import os
import sys
sys.path.append(os.path.abspath('../..'))
from src.anki.anki_utils import add_card_to_anki
from src.anki.print import print_pokemon
from data.Knowledge.evolutions import EVOLUTIONS
from data.Knowledge.generations import GENERATIONS
from main import POKEMON, get_de_pokemon


def get_tags(pokemon_id, pokemon_name, types):
	tags = [pokemon_id + "-" + pokemon_name.replace(' ', '-')]
	for type in types:
		tags.append(type)
	return tags

def add_sprite(sprite, pokemon_name, tags, model, deck):
	add_card_to_anki('<img src="' + sprite + '" />', pokemon_name, tags, model, deck)

def add_types_or_weaknesses(question_start, types_or_weaknesses, pokemon_name, tags, model, deck):
	result_string = ""
	for type_or_weakness in types_or_weaknesses:
		result_string += type_or_weakness + ", "
	result_string = result_string[:-2]
	add_card_to_anki(f"{question_start} " + get_de_pokemon(pokemon_name), result_string, tags, model, deck)

def create_pokemon_cards(pokemon, model, deck):
	tags = get_tags(pokemon['number'], pokemon['french_name'], pokemon['types'])
	add_card_to_anki("Numéro " + get_de_pokemon(pokemon['french_name']), pokemon['number'], tags, model, deck)
	add_card_to_anki("Nom anglais " + get_de_pokemon(pokemon['french_name']), pokemon['english_name'], tags, model, deck)
	add_sprite(pokemon['sprite'], pokemon['french_name'], tags, model, deck)
	add_types_or_weaknesses("Types", pokemon['types'], pokemon['french_name'], tags, model, deck)
	add_types_or_weaknesses("Faiblesses", pokemon['weaknesses'], pokemon['french_name'], tags, model, deck)
	if pokemon['forms']:
		for form in pokemon['forms']:
			if (form['types'] is None):
				tags = get_tags(pokemon['number'], form['french_name'], pokemon['types'])
				add_sprite(form['sprite'], form['french_name'], tags, model, deck)
			else:
				tags = get_tags(pokemon['number'], form['french_name'], form['types'])
				add_sprite(form['sprite'], form['french_name'], tags, model, deck)
				add_types_or_weaknesses("Types", form['types'], form['french_name'], tags, model, deck)
				add_types_or_weaknesses("Faiblesses", form['weaknesses'], form['french_name'], tags, model, deck)
				
def add_pokemons(gen_number, model, deck):
	first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
	last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1] + 1
	for pokemon_id in range(first_pokemon_id, last_pokemon_id):
		asyncio.run(print_pokemon(POKEMON[pokemon_id], gen_number))
		create_pokemon_cards(POKEMON[pokemon_id], model, deck)

def get_evolutions_text(chain):
	result = ""
	for i in range(len(chain)):
		if isinstance(chain[i], str):
			result += chain[i]
		else:
			if len(chain[i]) == 1:
				result += chain[i][0]
			else:
				result += "[" + get_evolutions_text(chain[i]) + "]"

		if i + 1 < len(chain):
			if isinstance(chain[i], str):
				result += " → "
			else:
				result += " ou "
	return result

def add_evolutions(gen_number, model, deck):
	for i in range (GENERATIONS[gen_number]['pokemon_range'][0], GENERATIONS[gen_number]['pokemon_range'][1] + 1):
		if i in EVOLUTIONS:
			question = "Évolutions " + get_de_pokemon(POKEMON[i]['french_name'])
			if isinstance(EVOLUTIONS[i][0], list): # on veut 2 questions différentes (on a forcément que des listes)
				for j in range (len(EVOLUTIONS[i])):
					answer = get_evolutions_text(EVOLUTIONS[i][j])
				tags = get_tags(POKEMON[i]['number'], POKEMON[i]['french_name'], POKEMON[i]['types'])
			else:
				answer = get_evolutions_text(EVOLUTIONS[i])
				tags = get_tags(POKEMON[i]['number'], POKEMON[i]['french_name'], POKEMON[i]['types'])
			add_card_to_anki(question, answer, tags, model, deck)