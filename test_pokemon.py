import pytest
from app import app, db, Pokemon

# Marcar 'client' como un fixture de pytest
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usar una base de datos en memoria para las pruebas
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crear las tablas de la base de datos

            # Agregar un Pokémon de prueba a la base de datos solo si no existe
            if not Pokemon.query.filter_by(name='test').first():
                test = Pokemon(
                    name='test',
                    pokedex_number=1303,
                    abilities='ability1,ability2',
                    sprites='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
                    types='type1,type2'
                )
                db.session.add(test)
                db.session.commit()
        yield client

        # Después de la prueba, no limpiar la base de datos, pero eliminar los datos específicos de la prueba si es necesario
        with app.app_context():
            test_pokemon = Pokemon.query.filter_by(name='test').first()
            if test_pokemon:
                db.session.delete(test_pokemon)  # Eliminar el Pokémon de prueba
                db.session.commit()  # Confirmar los cambios

def test_get_pokemon(client):
    """Prueba para asegurarse de que el Pokémon de prueba ('test') existe y se puede consultar."""
    rv = client.get('/api/pokemon')
    assert rv.status_code == 200
    # Buscar el Pokémon 'test' que debería haber sido insertado en la base de datos en memoria
    assert b'"name":"test"' in rv.data

def test_edit_pokemon(client):
    """Prueba para modificar los datos de Bulbasaur."""
    # Modificar los datos de Bulbasaur (suponiendo que ID 1 corresponde a Bulbasaur)
    client.put('/api/pokemon/1', json={
        "nombre": "Testing",
        "habilidades": ["change1"],
        "sprites": "new_sprite_url",
        "tipo": ["change1", "change2"]
    })

    # Obtener los datos modificados de Bulbasaur para verificar si los cambios se aplicaron
    rv = client.get('/api/pokemon/1')
    assert rv.status_code == 200
    assert b'"nombre":"Testing"' in rv.data  # Comprobar el nombre actualizado
    assert b'"habilidades":["change1"]' in rv.data  # Comprobar las habilidades modificadas
    assert b'"sprites":"new_sprite_url"' in rv.data  # Comprobar el sprite actualizado
    assert b'"tipo":["change1","change2"]' in rv.data  # Comprobar los tipos actualizados

    # Restablecer los datos de Bulbasaur a los valores originales para evitar cambios permanentes
    client.put('/api/pokemon/1', json={
        "nombre": "bulbasaur",
        "habilidades": ["overgrow", "chlorophyll"],
        "sprites": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "tipo": ["grass", "poison"]
    })

    # Obtener nuevamente a Bulbasaur para asegurarse de que se haya restablecido a los valores originales
    rv = client.get('/api/pokemon/1')
    assert rv.status_code == 200
    assert b'"nombre":"bulbasaur"' in rv.data  # Asegurarse de que el nombre se haya restablecido
    assert b'"habilidades":["overgrow","chlorophyll"]' in rv.data  # Asegurarse de que las habilidades se hayan restablecido
    assert b'"sprites":"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"' in rv.data  # Asegurarse de que el sprite se haya restablecido
    assert b'"tipo":["grass","poison"]' in rv.data  # Asegurarse de que los tipos se hayan restablecido
