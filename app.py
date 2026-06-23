from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

app = Flask(__name__)

# ==========================
# CONEXIÓN A MYSQL
# ==========================
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "base"
}

GEMINI_API_KEY = "AIzaSyCVXu5RhR66JS-HXbkXqhfeJJDxJYmQrWU"

genai.configure(api_key=GEMINI_API_KEY)

print("\nMODELOS DISPONIBLES:\n")

for m in genai.list_models():
    print(m.name)

modelo = genai.GenerativeModel('gemini-2.5-flash')# RUTAS HTML
# ==========================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')

# ==========================
# REGISTRO DE USUARIO
# ==========================

@app.route('/api/registro', methods=['POST'])
def registrar_usuario():
    print("PETICIÓN RECIBIDA")
    try:
        datos = request.get_json()

        nombre = datos['nombre']
        correo = datos['correo']
        password = datos['password']

        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        # Verificar si ya existe el correo
        sql_verificar = "SELECT id_usuario FROM usuarios WHERE correo = %s"
        cursor.execute(sql_verificar, (correo,))
        existe = cursor.fetchone()

        if existe:
            return jsonify({
                "success": False,
                "message": "Este correo ya está registrado"
            }), 400

        # Encriptar contraseña
        password_hash = generate_password_hash(password)

        sql_insert = """
        INSERT INTO usuarios
        (nombre, correo, contraseña, rol)
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            nombre,
            correo,
            password_hash,
            "usuario"
        )

        cursor.execute(sql_insert, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({
            "success": True,
            "message": "Usuario registrado correctamente"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route('/api/login', methods=['POST'])
def iniciar_sesion():

    try:
        datos = request.get_json()

        correo = datos['correo']
        password = datos['password']

        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM usuarios
        WHERE correo = %s
        """

        cursor.execute(sql, (correo,))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if not usuario:
            return jsonify({
                "success": False,
                "message": "Correo o contraseña incorrectos"
            }), 401

        if not check_password_hash(
            usuario['contraseña'],
            password
        ):
            return jsonify({
                "success": False,
                "message": "Correo o contraseña incorrectos"
            }), 401

        return jsonify({
            "success": True,
            "nombre": usuario['nombre'],
            "rol": usuario['rol']
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

@app.route('/becas/educacion')
def becas_educacion():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='educacion'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'educacion.html',
        becas=becas
    )

@app.route('/becas/bienestar')
def becas_bienestar():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='bienestar'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'bienestar.html',
        becas=becas
    )

@app.route('/becas/vivienda')
def becas_vivienda():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='vivienda'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'vivienda.html',
        becas=becas
    )

@app.route('/becas/alimentacion')
def becas_alimentacion():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='alimentacion'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'alimentacion.html',
        becas=becas
    )


@app.route('/becas/adultos_mayores')
def adultos_mayores():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='adultos_mayores'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'adultos.html',
        becas=becas
    )

@app.route('/becas/empleo')
def becas_empleo():

    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM becas
    WHERE categoria='empleo'
    """

    cursor.execute(sql)

    becas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'empleo.html',
        becas=becas
    )
@app.route('/api/chat', methods=['POST'])
def chat():

    try:

        datos = request.get_json()
        pregunta = datos['pregunta']

        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        palabras = pregunta.split()

        condiciones = []
        valores = []

        for palabra in palabras:

            condiciones.append("""
                nombre LIKE %s OR
                tipo LIKE %s OR
                descripcion LIKE %s OR
                requisitos LIKE %s
            """)

            busqueda = f"%{palabra}%"

            valores.extend([
                busqueda,
                busqueda,
                busqueda,
                busqueda
            ])

        sql = f"""
        SELECT *
        FROM apoyos
        WHERE {' OR '.join(condiciones)}
        LIMIT 10
        """

        cursor.execute(sql, valores)

        apoyos = cursor.fetchall()

        cursor.close()
        conexion.close()

        if apoyos:

            contexto = ""

            for apoyo in apoyos:

                contexto += f"""
Nombre: {apoyo['nombre']}
Tipo: {apoyo['tipo']}
Descripción: {apoyo['descripcion']}
Requisitos: {apoyo['requisitos']}
Ubicación: {apoyo['ubicacion']}
Enlace: {apoyo['enlace']}

"""

            prompt = f"""
Eres AIAS, un asistente especializado en apoyos sociales.

Responde de forma amigable y clara.

Utiliza principalmente la información encontrada en la base de datos.

Pregunta del usuario:

{pregunta}

Apoyos encontrados:

{contexto}
"""

        else:

            prompt = f"""
Eres AIAS, un asistente especializado en apoyos sociales y becas.

No se encontraron registros relacionados en la base de datos.

Responde usando conocimiento general sobre programas sociales,
becas, apoyos gubernamentales y recomendaciones útiles.

Pregunta:

{pregunta}
"""

        respuesta = modelo.generate_content(prompt)

        return jsonify({
            "respuesta": respuesta.text
        })

    except Exception as e:

        return jsonify({
            "respuesta": f"Error: {str(e)}"
        }), 500


# ==========================
# INICIAR SERVIDOR
# ==========================

if __name__ == '__main__':
    app.run(debug=True)