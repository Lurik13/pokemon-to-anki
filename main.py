import asyncio
import pickle
from src.generate_data.generate_files import generate_folder
from src.anki.anki_utils import *
import genanki # type: ignore
import sys
from src.anki.print import *
from src.generate_data.generate_evolutions_file import generate_evolutions_file
from data.Knowledge.evolutions import EVOLUTIONS
from src.functions.anki_deck import *
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_de_pokemon(name):
	if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
		return "d'" + name
	return "de " + name

def parsing(argv): ###################
	if len(argv) != 2:
		raise ValueError("Vous devez indiquer le numéro d'une génération.")
	if argv[1].isnumeric() == False:
		raise ValueError(f"'{argv[1]}' n'est pas un numéro.")

if __name__ == "__main__":
	# generate_evolutions_file(POKEMON)
	try:
		parsing(sys.argv)
		gen_number = sys.argv[1]
		gen_id = int(str((gen_number * (10 // len(gen_number) + 1)))[:10])
		gen_number = int(gen_number)
		if gen_number not in GENERATIONS:
			raise ValueError("Cette génération n'existe pas.")
		
		model = add_model_to_anki(gen_id, GENERATIONS[gen_number]['name'], 
			GENERATIONS[gen_number]['text_color'], GENERATIONS[gen_number]['background_image'])
		deck = genanki.Deck(gen_id, GENERATIONS[gen_number]['name'])

		asyncio.run(print_download(gen_number))
		add_pokemons(gen_number, model, deck)
		add_evolutions(gen_number, model, deck)
		print("Fini ! Tu peux dès maintenant importer le paquet dans Anki, depuis le dossier anki_decks !")
		
		generate_folder("./anki_decks", "")
		my_package = genanki.Package(deck)
		my_package.write_to_file("./anki_decks/" + GENERATIONS[gen_number]['name'] + '.apkg')
		
	except ValueError as ve:
		print("Error:", ve)
