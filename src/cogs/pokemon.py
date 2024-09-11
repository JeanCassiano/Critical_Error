import discord
from discord import app_commands
from discord.ext import commands
from typing import List
import requests

class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Função de autocomplete para pesquisa de Pokémon
    async def pokemon_autocomplete(
        self, 
        interaction: discord.Interaction, 
        current: str
    ) -> List[app_commands.Choice[str]]:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1100")  # Pega todos os Pokémon
        if response.status_code == 200:
            all_pokemons = response.json()['results']
            matched_pokemons = [pokemon['name'].capitalize() for pokemon in all_pokemons if current.lower() in pokemon['name']]
            return [
                app_commands.Choice(name=pokemon, value=pokemon)
                for pokemon in matched_pokemons[:5]  # Limite de 5 resultados
            ]
        else:
            return []

    @app_commands.command(name="pokemon", description="Pesquise um Pokémon")
    @app_commands.describe(shiny="Mostrar versão shiny", mega="Mostrar versão Mega", gmax="Mostrar versão Gigantamax")
    @app_commands.autocomplete(query=pokemon_autocomplete)
    async def pokemon(
        self, 
        interaction: discord.Interaction, 
        query: str, 
        shiny: bool = False, 
        mega: bool = False, 
        gmax: bool = False
    ):
        """Comando para buscar um Pokémon."""
        # Construir o nome do Pokémon para versões Mega e Gigantamax
        pokemon_name = query.lower()
        if mega:
            pokemon_name += "-mega"
        elif gmax:
            pokemon_name += "-gmax"

        # Solicitação à PokeAPI para buscar o Pokémon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code != 200:
            await interaction.response.send_message("Pokémon não encontrado. Verifique o nome e tente novamente.")
            return

        pokemon_data = response.json()
        # Obter informações do Pokémon
        pokemon_name_cap = pokemon_data['name'].capitalize()
        types = [t['type']['name'] for t in pokemon_data['types']]
        types_text = ', '.join(t.capitalize() for t in types)

        # Buscar imagem correta com base nas opções
        if shiny:
            pokemon_image_url = pokemon_data['sprites']['other']['official-artwork']['front_shiny']
        else:
            pokemon_image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']

        # Obter informações adicionais da espécie
        pokemon_species_url = pokemon_data['species']['url']
        pokemon_species_info = requests.get(pokemon_species_url)
        if pokemon_species_info.status_code == 200:
            species_data = pokemon_species_info.json()
            dex_entry = next(entry['flavor_text'].replace('\n', ' ').replace('\f', ' ') 
                             for entry in species_data['flavor_text_entries'] if entry['language']['name'] == 'en')
        else:
            dex_entry = "Não foi possível obter a descrição da espécie."

        # Obter relações de dano para o tipo de Pokémon
        damage_relations = {type_name: requests.get(f"https://pokeapi.co/api/v2/type/{type_name}").json()['damage_relations'] for type_name in types}
        
        # Calcular multiplicadores de dano
        multipliers = {}
        for relation in damage_relations.values():
            for type_, relations in relation.items():
                for type_relation in relations:
                    if type_ in ['double_damage_from', 'half_damage_from', 'no_damage_from']:
                        type_name = type_relation['name']
                        if type_name not in multipliers:
                            multipliers[type_name] = 1
                        if type_ == 'double_damage_from':
                            multipliers[type_name] *= 2
                        elif type_ == 'half_damage_from':
                            multipliers[type_name] *= 0.5
                        elif type_ == 'no_damage_from':
                            multipliers[type_name] = 0

        # Formatar os multiplicadores de dano
        multipliers_text = "\n".join(f"{type_name.capitalize()}: {multiplier}x" for type_name, multiplier in multipliers.items())

        # Criar a mensagem embed
        embed = discord.Embed(title=f"A wild {pokemon_name_cap} has appeared!", description=dex_entry)
        embed.set_image(url=pokemon_image_url)
        embed.add_field(name="Tipo", value=types_text, inline=False)
        embed.add_field(name="Modificadores de Dano", value=multipliers_text or "Nenhum", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PokemonCog(bot))
