from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


"""
Ruta del API general 
"""
@app.route('/api/pokemon', methods=['GET'])
def general():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1302')
    data = response.json()
    results = [{"name": pokemon["name"], "url": pokemon["url"]} for pokemon in data['results']]
    return jsonify(results)


"""
Ruta del API especifico SIN posibilidad de modificacion
"""
@app.route('/api/pokemon/<id_or_name>', methods=['GET','PUT'])
def specific(id_or_name):
    if request.method == 'GET':
         # Fetch from external API
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id_or_name}')
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "name": data['name'],
                "abilities": [ability['ability']['name'] for ability in data['abilities']],
                "pokedex_number": data['id'],
                "sprites": data['sprites']['front_default'],
                "types": [t['type']['name'] for t in data['types']]
            })


if __name__ == '__main__':
    app.run()
