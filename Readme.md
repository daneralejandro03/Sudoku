# Sudoku Programación 3

Este proyecto de Python proporciona una API para resolver y validar Sudokus, así como también enviarlos por correo electrónico.

## Descripción

Este proyecto consta de un servidor Flask que ofrece dos endpoints principales:

1. `/sudoku/ver` (Método: GET): Este endpoint muestra el Sudoku en la consola.
2. `/validar/movimiento` (Método: POST): Este endpoint valida un movimiento en el Sudoku y envía el Sudoku por correo electrónico.

## Dependencias

- Flask
- python-dotenv
- azure-communication-email

## Configuración

1. Clona el repositorio desde GitHub:

    ```shell
    git clone https://github.com/daneralejandro03/Sudoku.git
    ```

2. Accede al directorio del proyecto:

    ```shell
    cd tu_proyecto
    ```

3. Crea un entorno virtual (opcional pero recomendado):

    ```shell
    virtualenv venv
    ```

4. Activa el entorno virtual:

    - En Windows:

        ```shell
        venv\Scripts\activate
        ```

    - En macOS y Linux:

        ```shell
        source venv/bin/activate
        ```

5. Instala las dependencias del proyecto:

    ```shell
    pip install -r requirements.txt
    ```

6. Configura las variables de entorno (si es necesario):

    - Crea un archivo `.env` en el directorio raíz del proyecto y define las variables necesarias siguiendo el formato `NOMBRE_VARIABLE=valor`.

7. Ejecuta el proyecto:

    ```shell
    python Sudoku.py
    ```
   
Asegúrate de tener Python instalado en tu sistema. Luego, puedes instalar las dependencias necesarias ejecutando:


Antes de ejecutar la aplicación, asegúrate de configurar las siguientes variables de entorno en un archivo .env:

- CONNECTION_STRING: Cadena de conexión para el cliente de correo electrónico.
- SENDER_ADDRESS: Dirección de correo electrónico del remitente.

8.Ejecuta la aplicación Flask ejecutando el archivo Sodoku.py:

```shell
python Sodoku.py
```


