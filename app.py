from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db' #Persistencia de datos
db = SQLAlchemy(app)


#Crear la entidad de pokemones con sus respectivos parametros
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    pokedex_number = db.Column(db.Integer, nullable=False)
    abilities = db.Column(db.String(200))
    sprites = db.Column(db.String(200))
    types = db.Column(db.String(100))

def populate_database():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1302'  # Total number of Pokémon
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for index, result in enumerate(data['results']):
            pokemon_url = result['url']
            pokemon_data = requests.get(pokemon_url).json()

            name = pokemon_data['name']
            pokedex_number = pokemon_data['id']
            abilities = ','.join([ability['ability']['name'] for ability in pokemon_data['abilities']])
            sprites = pokemon_data['sprites']['front_default']
            types = ','.join([t['type']['name'] for t in pokemon_data['types']])

            # Check if the Pokémon is already in the database to avoid duplicates
            if not Pokemon.query.filter_by(name=name).first():
                new_pokemon = Pokemon(
                    name=name,
                    pokedex_number=pokedex_number,
                    abilities=abilities,
                    sprites=sprites,
                    types=types
                )
                db.session.add(new_pokemon)

            # Commit every 100 Pokémon to reduce the number of transactions
            if index % 100 == 0:
                db.session.commit()

        db.session.commit()


#Crear la base de datos para la persistencia
def create_tables():
    db.create_all()

    # Revisa el numero de pokemones
    pokemon_count = Pokemon.query.count()

    if pokemon_count == 0:
        print("Database esta vacia, llenando con Pokémon data...")
        populate_database()  # Popular la database con data
    else:
        print("Database ya tiene info, saltando data population.")



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

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
Ruta del API especifico con posibilidad de modificacion
"""
@app.route('/api/pokemon/<id_or_name>', methods=['GET','PUT'])
def specific(id_or_name):
    #Pokemon a encontrar
    pokemon = Pokemon.query.filter_by(name=id_or_name).first() or Pokemon.query.filter_by(pokedex_number=id_or_name).first()

    if request.method == 'GET':
        #Revisar si el pokemon esta en la DB local
        if not pokemon:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id_or_name}')
            if response.status_code == 200:
                data = response.json()
                return jsonify({
                    "nombre": data['name'],
                    "habilidades": [ability['ability']['name'] for ability in data['abilities']],
                    "pokedex": data['id'],
                    "sprites": data['sprites']['front_default'],
                    "tipo": [t['type']['name'] for t in data['types']]
                })
        #Si esta en la DB local
        else:
            # Return desde local DB
            return jsonify({
                "nombre": pokemon.name,
                "habilidades": pokemon.abilities,
                "pokedex": pokemon.pokedex_number,
                "sprites": pokemon.sprites,
                "tipo": pokemon.types
            })
    elif request.method == 'PUT':
        if not pokemon:
            return jsonify({"error":"Pokemon no encontrado"})

        data = request.json
        pokemon.name = data.get('nombre',pokemon.name)
        pokemon.abilities = data.get('habilidades', pokemon.abilities)
        pokemon.sprites = data.get('sprites', pokemon.sprites)
        pokemon.types = data.get('tipo',pokemon.types)
        db.session.commit()
        return jsonify({"message": "Pokémon modificado correctamente"}), 200





if __name__ == '__main__':
    app.run()
