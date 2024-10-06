# Middleware Pokémon API
#### Prueba desarollador backend python
#### Santiago Arenas Rojas

Este proyecto es una API desarrollada en **Python** utilizando el framework **Flask**. Se conecta con la API de Pokémon del profesor Oak para obtener información de Pokémon y permite realizar consultas y modificaciones (dependiendo de la versión). Existen dos ramas en este repositorio: una versión con persistencia y otra que sirve los datos solo desde la API original.

## Descripción del Proyecto

La API tiene dos ramas principales:
1. **persistent**: Esta rama utiliza persistencia local, es decir, los datos de los Pokémon se almacenan en una base de datos SQLite local. Permite realizar consultas **GET** para obtener información de un Pokémon, así como modificar la información de un Pokémon existente mediante **PUT**.
Durante el primer request a {{baseURL}}/api/pokemon si la base de datos esta vacia, la bas de datos se llenara lo cual puede tomar un poco de tiempo.
2. **no-modifiable**: En esta rama, los datos de los Pokémon se obtienen directamente desde la API del profesor Oak. No permite realizar modificaciones locales a la información de los Pokémon.

### Rutas principales
- **GET** `/api/pokemon`: Devuelve una lista de los Pokémon.
- **GET** `/api/pokemon/<id_or_name>`: Devuelve los detalles de un Pokémon específico por nombre o número en la Pokédex.
- **PUT** `/api/pokemon/<id_or_name>`: Permite modificar la información de un Pokémon (disponible solo en la rama `persistent`).

## Requisitos de Instalación

Sigue los siguientes pasos para instalar y ejecutar la aplicación en tu entorno local:

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/pokemon-middleware.git
cd pokemon-middleware
```

### 2. Crea un env (opcional)
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar aplicación
```bash
flask run
```

## Pruebas Unitarias
La aplicación incluye pruebas unitarias para verificar el correcto funcionamiento de las rutas de la API. Las pruebas están escritas utilizando el framework pytest.
(Solo para la rama persistent)
### 1. Ejecutar pruebas
```bash
pytest
```

### 2. Descripción de las pruebas
* Prueba de GET Pokémon: Verifica que la ruta /api/pokemon devuelva correctamente los datos de un Pokémon.
* Prueba de modificación de Pokémon (PUT): En la rama persistent, se verifica que un Pokémon pueda ser modificado correctamente a través de la ruta /api/pokemon/<id_or_name>.



## Ramas del proyecto

### **1. persistent**
Esta rama permite la persistencia de los datos de Pokémon en una base de datos local, lo que significa que los datos pueden modificarse y guardarse a través de la API.

### **2. no-modifiable**
En esta rama, los datos de los Pokémon son servidos exclusivamente desde la API externa del profesor Oak, sin capacidad de modificación o almacenamiento local.

