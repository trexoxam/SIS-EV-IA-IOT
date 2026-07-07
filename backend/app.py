from flask import Flask, request, render_template, session, redirect, url_for
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "examai_2026"

def conectar():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 16443)),
        ssl_ca='ca.pem' 
    )

@app.route('/')
@app.route('/index')
def index():

    if session.get('rol') == 'admin':
        return render_template(
            'indexadmin.html',
            usuario=session.get('usuario'),
            rol=session.get('rol')
        )

    return render_template(
        'index.html',
        usuario=session.get('usuario'),
        rol=session.get('rol')
    )

@app.route('/ver_examen/<nombre_examen>')
def ver_examen(nombre_examen):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Traer las preguntas del examen seleccionado
    cursor.execute("""
        SELECT *
        FROM preguntas
        WHERE nombre_examen = %s
        ORDER BY id_pregunta
    """, (nombre_examen,))

    preguntas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "ver_examen.html",
        nombre_examen=nombre_examen,
        preguntas=preguntas
    )

@app.route('/mis_examenes')
def mis_examenes():

    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') == 'admin':
        return redirect(url_for('examenes'))

    return redirect(url_for('examenes_aspirante'))

@app.route('/examenes_aspirante')
def examenes_aspirante():

    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            nombre_examen,
            COUNT(*) AS total_preguntas
        FROM preguntas
        GROUP BY nombre_examen
        ORDER BY nombre_examen
    """)

    examenes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'examenes_aspirante.html',
        examenes=examenes
    )





@app.route('/iniciar_examen/<nombre_examen>')
def iniciar_examen(nombre_examen):

    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    session['examen_actual'] = nombre_examen
    session['pregunta_actual'] = 0

    return redirect(url_for('examen'))


@app.route('/examenes')
def examenes():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            nombre_examen,
            COUNT(*) AS total_preguntas
        FROM preguntas
        GROUP BY nombre_examen
        ORDER BY nombre_examen
    """)

    examenes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'examenes.html',
        examenes=examenes
    )

@app.route('/examen')
def examen():

    nombre_examen = session.get('examen_actual')
    indice = session.get('pregunta_actual', 0)

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM preguntas
        WHERE nombre_examen = %s
        ORDER BY id_pregunta
    """, (nombre_examen,))

    preguntas = cursor.fetchall()

    if not preguntas:
        cursor.close()
        conn.close()
        return "No hay preguntas"

    if indice >= len(preguntas):
        indice = len(preguntas) - 1

    pregunta = preguntas[indice]

    cursor.execute("""
        SELECT respuesta_usuario
        FROM respuestas_usuario
        WHERE id_usuario = %s
        AND id_pregunta = %s
    """, (
        session['id_usuario'],
        pregunta['id_pregunta']
    ))

    respuesta_guardada = cursor.fetchone()

    cursor.close()
    conn.close()

    respuesta_usuario = None

    if respuesta_guardada:
        respuesta_usuario = respuesta_guardada['respuesta_usuario']

    return render_template(
        'examen.html',
        pregunta=pregunta,
        numero=indice + 1,
        total=len(preguntas),
        nombre_examen=nombre_examen,
        respuesta_usuario=respuesta_usuario
    )


@app.route('/guardar_respuesta', methods=['POST'])
def guardar_respuesta():

    id_usuario = session['id_usuario']

    id_pregunta = request.form.get('id_pregunta')
    respuesta = request.form.get('respuesta')

    if not respuesta:
        return "Debes seleccionar una respuesta."

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Verificar si ya existe una respuesta para esta pregunta
    cursor.execute("""
        SELECT *
        FROM respuestas_usuario
        WHERE id_usuario = %s
        AND id_pregunta = %s
    """, (
        id_usuario,
        id_pregunta
    ))

    existe = cursor.fetchone()

    if existe:

        cursor.execute("""
            UPDATE respuestas_usuario
            SET respuesta_usuario = %s
            WHERE id_usuario = %s
            AND id_pregunta = %s
        """, (
            respuesta,
            id_usuario,
            id_pregunta
        ))

    else:

        cursor.execute("""
            INSERT INTO respuestas_usuario (
                id_usuario,
                id_pregunta,
                respuesta_usuario
            )
            VALUES (%s,%s,%s)
        """, (
            id_usuario,
            id_pregunta,
            respuesta
        ))

    conn.commit()

    nombre_examen = session.get('examen_actual')

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM preguntas
        WHERE nombre_examen = %s
    """, (nombre_examen,))

    total = cursor.fetchone()['total']

    session['pregunta_actual'] += 1

    cursor.close()
    conn.close()

    if session['pregunta_actual'] >= total:
        return redirect(url_for('resultado'))

    return redirect(url_for('examen'))


@app.route('/resultado')
def resultado():
    id_usuario = session['id_usuario']
    nombre_examen = session.get('examen_actual')
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # 1. Calculamos correctas e incorrectas
    cursor.execute("""
        SELECT COUNT(*) AS correctas
        FROM respuestas_usuario r
        INNER JOIN preguntas p ON r.id_pregunta = p.id_pregunta
        WHERE r.id_usuario = %s AND r.respuesta_usuario = p.respuesta_correcta
    """, (id_usuario,))
    correctas = cursor.fetchone()['correctas']

    cursor.execute("SELECT COUNT(*) AS total FROM respuestas_usuario WHERE id_usuario = %s", (id_usuario,))
    total = cursor.fetchone()['total']
    
    incorrectas = total - correctas
    calificacion = round((correctas / total) * 100) if total > 0 else 0

    # 2. INSERTAMOS usando las variables que ya calculamos
    # Ahora sí incluimos aciertos e incorrectas (que es tu columna 'errores')
    cursor.execute("""
        INSERT INTO resultados_examen (id_usuario, nombre_examen, calificacion, aciertos, errores, fecha_fin) 
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, (id_usuario, nombre_examen, calificacion, correctas, incorrectas))
    
    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        'resultado.html',
        correctas=correctas,
        incorrectas=incorrectas,
        total=total,
        calificacion=calificacion
    )

@app.route('/siguiente')
def siguiente():

    session['pregunta_actual'] += 1

    return redirect(url_for('examen'))

@app.route('/anterior')
def anterior():

    if session.get('pregunta_actual', 0) > 0:
        session['pregunta_actual'] -= 1

    return redirect(url_for('examen'))

@app.route('/dashboard')
def dashboard():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    # Traemos los últimos 5 resultados
    cursor.execute("SELECT * FROM resultados_examen ORDER BY fecha_fin DESC LIMIT 5")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', resultados=resultados)

@app.route('/crear_pregunta')
def crear_pregunta():
    return render_template('crear_pregunta.html')

@app.route('/guardar_pregunta', methods=['POST'])
def guardar_pregunta():

    nombre_examen = request.form['nombre_examen']

    pregunta = request.form['pregunta']
    opcion_a = request.form['opcion_a']
    opcion_b = request.form['opcion_b']
    opcion_c = request.form['opcion_c']
    opcion_d = request.form['opcion_d']

    respuesta_correcta = request.form['respuesta_correcta']

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO preguntas (
        nombre_examen,
        pregunta,
        opcion_a,
        opcion_b,
        opcion_c,
        opcion_d,
        respuesta_correcta
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    valores = (
        nombre_examen,
        pregunta,
        opcion_a,
        opcion_b,
        opcion_c,
        opcion_d,
        respuesta_correcta
    )

    cursor.execute(sql, valores)

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('crear_pregunta'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        correo = request.form['correo']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE correo = %s",
            (correo,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(
            usuario['password'],
            password
        ):

            session['id_usuario'] = usuario['id_usuario']
            session['usuario'] = usuario['nombre_completo']
            session['correo'] = usuario['correo']
            session['rol'] = usuario['rol']

            return redirect(url_for('index'))

        return render_template(
            'login.html',
            error='Correo o contraseña incorrectos'
        )

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/registro')
def formulario_registro():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro():


    nombre = request.form['nombre_completo']
    curp = request.form['curp']
    correo = request.form['correo']
    telefono = request.form['telefono']
    password = generate_password_hash(request.form['password'])

    nivel = request.form['nivel_academico']
    institucion = request.form['institucion']
    area = request.form['area_interes']
    promedio = request.form['promedio']

    internet = request.form['internet_estable']
    experiencia = request.form['experiencia_examenes']
    camara = request.form['dispone_camara']

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO usuarios (
        nombre_completo, curp, correo, telefono, password,
        nivel_academico, institucion, area_interes, promedio,
        internet_estable, experiencia_examenes, dispone_camara
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    valores = (
        nombre, curp, correo, telefono, password,
        nivel, institucion, area, promedio,
        internet, experiencia, camara
    )

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('login'))


@app.route('/agenda')
def agenda():
    if 'id_usuario' not in session: return redirect(url_for('login'))
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Obtener citas
    cursor.execute("""
        SELECT c.fecha_cita AS fecha, c.horario_inicio AS hora, c.estado, u.nombre_completo 
        FROM citas c
        INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
        ORDER BY c.fecha_cita ASC
    """)
    citas = cursor.fetchall()
    
    # 2. Obtener horas ocupadas de forma segura (sin importar si es time o timedelta)
    cursor.execute("SELECT DISTINCT horario_inicio FROM citas")
    datos = cursor.fetchall()
    
    ocupadas = []
    for c in datos:
        val = c['horario_inicio']
        if isinstance(val, (str)): # Si llega como string
            ocupadas.append(val[:5])
        elif hasattr(val, 'strftime'): # Si es tipo time
            ocupadas.append(val.strftime("%H:%M"))
        else: # Si es timedelta
            total_segundos = int(val.total_seconds())
            ocupadas.append(f"{total_segundos // 3600:02}:{(total_segundos % 3600) // 60:02}")
    
    cursor.close()
    conn.close()
    
    return render_template('agenda.html', citas=citas, ocupadas=ocupadas)

@app.route('/crear_cita', methods=['POST'])
def crear_cita():
    if 'id_usuario' not in session: return redirect(url_for('login'))
    
    id_usuario = session['id_usuario']
    fecha = request.form['fecha']
    hora_inicio = request.form['hora']
    
    from datetime import datetime, timedelta
    t = datetime.strptime(hora_inicio, "%H:%M")
    hora_fin = (t + timedelta(hours=2)).strftime("%H:%M")

    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO citas (id_usuario, fecha_cita, horario_inicio, horario_fin, estado)
            VALUES (%s, %s, %s, %s, 'Confirmada')
        """, (id_usuario, fecha, hora_inicio, hora_fin))
        conn.commit()
        return redirect(url_for('agenda', status='success'))
    except Exception as e:
        print(f"Error al agendar: {e}")
        return redirect(url_for('agenda', status='error'))
    finally:
        cursor.close()
        conn.close()





if __name__ == '__main__':
    app.run(debug=True)