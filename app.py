from flask import Flask, request, jsonify
import requests

# Inicialización de la aplicación Flask
app = Flask(__name__)

"""
Ruta del API general para obtener todos los Pokémon.
"""
@app.route('/api/pokemon', methods=['GET'])
def general():
    # Realizar una solicitud a la API externa para obtener la lista de Pokémon
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1302')
    data = response.json()

    # Construir la respuesta en el formato requerido
    results = [{"name": pokemon["name"], "url": pokemon["url"]} for pokemon in data['results']]
    return jsonify(results)  # Retornar la lista de Pokémon en formato JSON

"""
Ruta del API específica SIN posibilidad de modificación.
"""
@app.route('/api/pokemon/<id_or_name>', methods=['GET', 'PUT'])
def specific(id_or_name):
    if request.method == 'GET':
        # Realizar una solicitud a la API externa para obtener datos de un Pokémon específico
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id_or_name}')
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "name": data['name'],
                "abilities": [ability['ability']['name'] for ability in data['abilities']],  # Obtener habilidades
                "pokedex_number": data['id'],  # Número en la Pokédex
                "sprites": data['sprites']['front_default'],  # URL del sprite del Pokémon
                "types": [t['type']['name'] for t in data['types']]  # Obtener tipos
            })
        else:
            return jsonify({"error": "Pokémon no encontrado"}), 404  # Retornar error si no se encuentra el Pokémon

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run()
