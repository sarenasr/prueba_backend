from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'  # Persistencia de datos
db = SQLAlchemy(app)

# Crear la entidad de Pokémon con sus respectivos parámetros
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada Pokémon
    name = db.Column(db.String(80), unique=True, nullable=False)  # Nombre del Pokémon
    pokedex_number = db.Column(db.Integer, nullable=False)  # Número en la Pokédex
    abilities = db.Column(db.String(200))  # Habilidades del Pokémon
    sprites = db.Column(db.String(200))  # URL del sprite del Pokémon
    types = db.Column(db.String(100))  # Tipos del Pokémon

def populate_database():
    """Función para poblar la base de datos con los datos de Pokémon desde la API externa."""
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1302'  # Número total de Pokémon
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

            # Revisar si ya existe para evitar duplicados
            if not Pokemon.query.filter_by(name=name).first():
                new_pokemon = Pokemon(
                    name=name,
                    pokedex_number=pokedex_number,
                    abilities=abilities,
                    sprites=sprites,
                    types=types
                )
                db.session.add(new_pokemon)

            # Commit cada 100 Pokémon para reducir el número de transacciones
            if index % 100 == 0:
                db.session.commit()

        db.session.commit()  # Hacer commit de cualquier Pokémon restante al final

# Crear la base de datos para la persistencia
@app.before_request
def create_tables():
    """Crear las tablas en la base de datos y poblarla si está vacía."""
    db.create_all()  # Crear las tablas

    # Revisar el número de Pokémon en la base de datos
    pokemon_count = Pokemon.query.count()

    if pokemon_count == 0:
        print("La base de datos está vacía, llenando con datos de Pokémon...")
        populate_database()  # Poblar la base de datos con datos
    else:
        print("La base de datos ya tiene información, saltando la población de datos.")

"""
Ruta del API general para obtener todos los Pokémon.
"""
@app.route('/api/pokemon', methods=['GET'])
def general():
    # Obtener todos los Pokémon de la base de datos local
    pokemon_list = Pokemon.query.all()

    # Construir la respuesta en el formato requerido
    results = [{"name": pokemon.name, "url": f'/api/pokemon/{pokemon.pokedex_number}'} for pokemon in pokemon_list]

    return jsonify(results)  # Retornar la lista de Pokémon en formato JSON

"""
Ruta del API específica con posibilidad de modificación.
"""
@app.route('/api/pokemon/<id_or_name>', methods=['GET', 'PUT'])
def specific(id_or_name):
    # Encontrar el Pokémon en la base de datos local por nombre o número en la Pokédex
    pokemon = Pokemon.query.filter_by(name=id_or_name).first() or Pokemon.query.filter_by(
        pokedex_number=id_or_name).first()

    if request.method == 'GET':
        if pokemon:
            # Retornar datos del Pokémon desde la base de datos local
            return jsonify({
                "nombre": pokemon.name,
                "habilidades": pokemon.abilities.split(','),  # Separar habilidades para coincidir con el formato esperado
                "pokedex": pokemon.pokedex_number,
                "sprites": pokemon.sprites,
                "tipo": pokemon.types.split(',')  # Separar tipos para coincidir con el formato esperado
            })
        else:
            return jsonify({"error": "Pokémon no encontrado"}), 404  # Retornar error si no se encuentra el Pokémon

    elif request.method == 'PUT':
        if not pokemon:
            return jsonify({"error": "Pokémon no encontrado"}), 404  # Retornar error si no se encuentra el Pokémon

        # Modificar los datos del Pokémon
        data = request.json
        pokemon.name = data.get('nombre', pokemon.name)
        pokemon.abilities = ','.join(data.get('habilidades', pokemon.abilities.split(',')))
        pokemon.sprites = data.get('sprites', pokemon.sprites)
        pokemon.types = ','.join(data.get('tipo', pokemon.types.split(',')))

        # Hacer commit de los cambios en la base de datos local
        db.session.commit()

        return jsonify({"message": "Pokémon modificado correctamente"}), 200  # Retornar mensaje de modificación exitosa

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run()
