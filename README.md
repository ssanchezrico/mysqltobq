# Script carga de datos - Proyecto calidad y gobierno del dato

Script en Python3 para la carga de datos desde MySql hacia BigQuery.

## Índice
- [Instalación](#Instalación)
- [Configuración](#Configuracion)
- [Notas](#Notas)

## Instalación

Para instalar las dependencias necesarias, sigue estos pasos:

1. Clona el repositorio:
```sh
git clone https://github.com/ssanchezrico/dataquality.git
```
2. Entra en el directorio del proyecto
```sh
cd bigquery
```
3. Crea y activa el entorno virtual
```sh
python3 -m venv virtual_enviroment
source virtual_enviroment/bin/activate
```
4. Instala las dependencias
```sh
pip3 install -r requeriments.txt
```


## Configuración

Son necesarios 4 ficheros JSON de configuración:
1. [Fichero de credenciales de BigQuery](#Fichero-de-credenciales-BigQuery)
2. [Fichero de credenciales de la bbdd MySql](#Fichero-de-credenciales-MySql)
3. [Fichero configuración de la carga](#Fichero-de-configuración-de-la-carga)
4. [Fichero con las tablas a cargar](#Fichero-con-las-tablas-a-cargar)

### Fichero de credenciales BigQuery

Se trata del fichero de clave con formato JSON generado desde la consola de BigQuery:
- Estando dentro del proyecto en la consola de BigQuery ir a la opción "Cuentas de servicio" del menú principal
- Crear nueva cuenta de servicio
- Establecer nombre de la cuenta y asignarle rol de Propietario
- Una vez creada, en "opciones" seleccionar "Administrar claves"
- Se crea una clave nueva en formato JSON y se descarga. Nota: No se podrá descargar de nuevo.

Crea el directorio .credentials/ en la raíz del proyecto y mueve ahí el fichero.

### Fichero de credenciales MySql

Fichero JSON con 4 claves para la conexión a la bbdd de MySql
- host
- user
- password
- database

Este fichero debe copiarse en la carpeta .credentials/ creada en el punto anterior.


### Fichero de configuración de la carga

Fichero JSON denominado config.json ubicado en la raíz del proyecto con 3 claves:
- project_name: Se indicará el nombre del proyecto tal cual está en BigQuery
- layer: El nombre de la capa donde se volcarán los datasets en BigQuery. Si no existe en BigQuery el script la creará.
- datasets_file: Nombre del fichero json que contiene la estructura de las tablas a cargar. Se describe a continación [Fichero con las tablas a cargar](#Fichero-con-las-tablas-a-cargar)<br>
<br>
Crea el directorio config en la raíz del proyecto y mueve ahí el fichero config.json.<br><br>

Ejemplo:
```json
{
	"project_name": "data-quality",
	"layer": "bronze",
	"datasets_file": "bronze_tables.json"
}
```

### Fichero con las tablas a cargar

Debe contener, en formato JSON, el nombre de la tabla, las columnas y el tipo de dato de BigQuery para cada columna.<br>
Contiene un objeto JSON con clave "datasets" y esta clave consiste en un array de objetos JSON con claves "name" y "columns". Cada objeto representa una tabla a cargar.<br>
La clave "columns" contendrá los nombres de columna y su tipo en BigQuery.<br>
De forma opcional puede usarse una tercera clave "where" para filtrar los datos a cargar.<br>
<br>
Este fichero debe copiarse a la carpeta config creada en el punto anterior.<br><br>
Ejemplo:
```json
{
  "datasets": [
    {
      "name": "empresa",
      "columns": {
        "id": "INT64",
        "nombre": "STRING",
        "abreviatura": "STRING",
        "codigocontabilidad": "STRING"
      }
    },
    {
      "name": "tmp_main_reservations",
      "columns": {
        "empresa_id": "INT64",
        "reservation_number": "INT64",
        "guest_country_code": "STRING",
        "union_sources": "STRING"
      },
      "where": "empresa_id in (1,2,3) and reservation_number > 1234"
    }
  ]
}
```

## Notas
En función de la capa destino (conjunto de datos en bq) donde queramos volcar los datos, necesitaremos una copia de todo el proyecto.<br>

