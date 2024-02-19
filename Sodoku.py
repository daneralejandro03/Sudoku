from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from azure.communication.email import EmailClient

load_dotenv()
app = Flask(__name__)

def imprimir_sudoku(sudoku):
    """
    Imprime el Sudoku en la consola.
    """
    for i, fila in enumerate(sudoku):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(3):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            print(" ".join(str(num) for num in fila['columnas'][j]), end=" ")
            if j == 2:
                print("|", end="")
        print()


def validar_sudoku(sudoku, fila, columna, numero):
    """
    Valida si un movimiento es válido en el Sudoku.
    """
    # Verificar si los índices de fila y columna están dentro del rango válido
    if fila < 0 or fila > 8 or columna < 0 or columna > 8:
        print("Error: Índices de fila o columna fuera de rango.")
        return False

    # Verificar si el número a colocar está dentro del rango válido (1 a 9)
    if numero < 1 or numero > 9:
        print("Error: Número fuera del rango válido (1 a 9).")
        return False

    if not verificar_fila(sudoku, fila, numero):
        return False

    if not verificar_columna(sudoku, columna, numero):
        return False

    return True

def verificar_fila(sudoku, fila, numero):
    fila_sector = fila // 3

    for i in range(fila_sector * 3, (fila_sector + 1) * 3):
        for j in range(3):
            if sudoku[i]["columnas"][fila % 3][j] == numero:
                return False
    return True

def verificar_columna(sudoku, columna, numero):
    columna_sector = columna // 3

    for i in range(columna_sector * 3, (columna_sector + 1) * 3):
        for j in range(3):
            if sudoku[i]["columnas"][j][columna % 3] == numero:
                return False
    return True

#ESTA FUNCIÓN TODAVIA NO SE ESTA USANDO
"""
def verificar_cuadrante(sudoku, fila, columna, numero):
    fila_sector = fila // 3
    columna_sector = columna // 3

    for i in range(fila_sector * 3, (fila_sector + 1) * 3):
        for j in range(columna_sector * 3, (columna_sector + 1) * 3):
            if sudoku[i]["columnas"][j // 3][j % 3] == numero:
                return False
"""


def generar_html_sudoku(sudoku, fila_verificar, columna_verificar):
    sudoku_array = [[0] * 9 for _ in range(9)]
    control = 0
    control2 = 0
    for x in range(9):
        for i in range(3):
            for j in range(3):
                if isinstance(sudoku[x]["columnas"][i][0], list):
                    sudoku_array[x][3 * i + j] = sudoku[x]["columnas"][i][0][j]
                else:
                    sudoku_array[x][3 * i + j] = sudoku[x]["columnas"][i][j]
        control = control + 1
        if control == 3:
            control = 0
            control2 = control2 + 1

    # Generar la tabla HTML
    tabla_html = f"""
    <table style="border-collapse: collapse; border: 2px solid #333;">
    """
    for fila_index, fila in enumerate(sudoku_array):
        tabla_html += "<tr>"
        for columna_index, celda in enumerate(fila):
            estilo = 'width: 40px; height: 40px; text-align: center; border: 1px solid #999;'
            if fila_index == fila_verificar or columna_index == columna_verificar:
                estilo += 'background-color: #42D6F0;'  # Cambiar el fondo a amarillo para resaltar la fila o columna
            tabla_html += f'<td style="{estilo}">'
            tabla_html += f'<input type="text" style="width: 100%; height: 100%; border: none; background-color: transparent; font-size: 16px; text-align: center;" value="{celda}">'
            tabla_html += "</td>"
            if (columna_index + 1) % 3 == 0 and columna_index != 8:
                tabla_html += '<td style="border: none; width: 5px;"></td>'  # Añadir celda vacía para separar cuadrantes horizontalmente
        tabla_html += "</tr>"
        if (fila_index + 1) % 3 == 0 and fila_index != 8:
            tabla_html += '<tr style="border: none;"><td colspan="9" style="border: none; height: 5px;"></td></tr>'  # Añadir fila vacía para separar cuadrantes verticalmente
    tabla_html += "</table>"

    return tabla_html


def enviar_sudoku(sudoku_info):
    try:
        sudoku = sudoku_info["sudoku"]
        fila = sudoku_info["fila"]
        columna = sudoku_info["columna"]
        numero = sudoku_info["numero"]

        connection_string = os.environ.get("CONNECTION_STRING")
        client = EmailClient.from_connection_string(connection_string)
        sudoku_html = generar_html_sudoku(sudoku_info["sudoku"], fila, columna)

        # Determinar si se puede colocar el número en la fila y columna especificadas

        if validar_sudoku(sudoku, fila, columna, numero):
            mensaje_validacion = f'Se puede colocar el número {numero} en la fila {fila} y columna {columna}'
            status_code = 200
        else:
            mensaje_validacion = f'No se puede colocar el número {numero} en la fila {fila} y columna {columna}'
            status_code = 400

        # Generar el contenido del correo electrónico con el Sudoku y el mensaje de validación
        body_email = f"""
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; border: 2px solid #333; }}
                td {{ width: 40px; height: 40px; text-align: center; border: 1px solid #999; }}
                input {{ width: 100%; height: 100%; border: none; background-color: transparent; font-size: 16px; text-align: center; }}
            </style>
        </head>
        <body>
            <p>{mensaje_validacion}</p>
            {sudoku_html}
        </body>
        </html>
        """

        # Configurar el mensaje de correo electrónico
        message = {
            "senderAddress": os.environ.get("SENDER_ADDRESS"),
            "recipients": {
                "to": [{"address": sudoku_info["address"]}],
            },
            "content": {
                "subject": sudoku_info["subject"],
                "html": body_email,
            }
        }

        # Enviar el correo electrónico
        poller = client.begin_send(message)
        result = poller.result()

        print("Correo electrónico enviado correctamente.")

        return jsonify({'mensaje': mensaje_validacion}), status_code

    except Exception as ex:
        print("Error al enviar correo electrónico:", ex)
        return jsonify({"error": str(ex)}), 500


@app.route('/sudoku/ver', methods=['GET'])
def mostrar_sudoku():
    """
    Muestra el Sudoku en la consola.
    """
    info_sudoku = request.get_json()["sudoku"]
    imprimir_sudoku(info_sudoku)
    return jsonify(info_sudoku), 200


@app.route('/validar/movimiento', methods=['POST'])
def validar_movimiento():
    """
    Valida un movimiento en el Sudoku y envía el Sudoku por correo electrónico.
    """
    data = request.get_json()

    sudoku = data.get('sudoku')
    fila = data.get('fila')
    columna = data.get('columna')
    numero = data.get('numero')

    if sudoku is None or fila is None or columna is None or numero is None:
        return jsonify({'error': 'Datos de entrada incompletos'}), 400

    #Función para enviar el sudoku por correo
    enviar_sudoku(data)

    if validar_sudoku(sudoku, fila, columna, numero):
        return jsonify({'mensaje': f'Se puede colocar el número {numero} en la fila {fila} y columna {columna}'}), 200
    else:
        return jsonify({'mensaje': f'No se puede colocar el número {numero} en la fila {fila} y columna {columna}'}), 400


if __name__ == '__main__':
    app.run(debug=True)