import textwrap
from flask import Flask, Response, render_template, redirect
from flask import jsonify, request, session
from random import randint
from BD.libros import *
from BD.users import *
from BD.ejemplares import *
from BD.alumnos import *
from BD.auditorias import *
from BD.prestamos import *
from Extra.colors import PALETTE
from datetime import date, timedelta
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "Los que poseen la cumbia"

roles = ("administrador", "operador")

def es_admin():
    return session.get('rol') == "administrador" and session.get('estado') == "activo"

@app.route("/")
def index(msg = None):
    q = request.args.get("q", "")
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    return render_template("index.html", 
                           books=BOOKS, q=q, Message = msg)

@app.route("/", methods=['POST'])
def turn_back():
    curr = request.form.get('indx', 0)
    q = request.form.get('q', '')
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", 
                           books=BOOKS, indices=indices, curr=curr, q=q)

@app.route("/close_session")
def close_session():
    session.clear()
    return redirect("/")

# ------------------- LIBROS -------------------

@app.route("/addBook")
def addBook():
    return render_template("Forms/addBook.html")

@app.route("/libros/guardar", methods=['POST'])
def guardar_libro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    filas = insertar_libro(titulo, autor, categoria)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/")

@app.route("/libro/info", methods=['POST'])
def libro_info():
    id = request.form['ID']
    curr = request.form.get('curr', 0)
    q = request.form.get('query', '')
    libro = buscar_libro(id)
    return render_template("Info/libro_info.html", 
                           libro=libro, ant=curr, query=q, user = session)

@app.route("/libros/eliminar", methods=['POST'])
def eliminar_libro():
    id = request.form['id_libro']
    filas = eliminar_1_libro(id)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/")

@app.route("/libros/editar", methods=['POST'])
def editar_libro():
    id = request.form['id_libro']
    libro = buscar_libro(id)
    return render_template("Forms/updateBook.html", libro=libro)

@app.route("/libros/actualizar", methods=['POST'])
def actualizar_libro():
    id = request.form['id_libro']
    titulo = request.form['titulo']
    autor = request.form['autor']
    cat = request.form['categoria']
    filas = actualizar_1_libro(id, titulo, autor, cat)
    if filas == 0:
        return index("Operación fallida")
    return redirect('/')

@app.route("/libros/ejemplar", methods=['POST'])
def ejemplar_libro():
    if session['rol'] != "administrador":
        return redirect("/")
    id = request.form['id_libro']
    return render_template("Forms/addEjemplar.html", id=id)

@app.route("/libros/ejemplar/registrar", methods=['POST'])
def registrar_ejemplar():
    id = request.form['id']
    codigo = request.form['codigo']
    filas = registrar_1_ejemplar(codigo, id)
    if filas == 0:
        return index("Operación fallida")
    return redirect('/')

@app.route("/cover/<int:i>.svg")
def cover(i):
    libro = buscar_libro(i)
    titulo = libro["titulo"]
    index = randint(0, len(PALETTE)-1)
    c1, c2 = PALETTE[index]
    svg = render_template(
        "cover.svg",
        lines=textwrap.wrap(titulo, 11),
        c1=c1,
        c2=c2,
    )
    return Response(svg, mimetype="image/svg+xml")

#------------------- Admin --------------------
@app.route("/admin/login", methods=['POST'])
def login_route():
    user = request.form['usuario']
    passw = request.form['password']
    loged = login(user, passw)

    if not loged or loged[0]['rol'] not in roles or loged[0]['estado'] == 'inactivo': 
        return index("Usuario o contraseña incorrecto(s)")
    
    usuario = loged[0]

    session['id'] = usuario['id_bibliotecario']
    session['nombre'] = usuario['nombre_completo']
    session['user'] = usuario['usuario']
    session['rol'] = usuario['rol']
    session['estado'] = usuario['estado']

    return redirect("/admin/panel")

@app.route("/admin/panel")
def admin_panel():
    if not session or  session['rol'] not in roles and session['estado'] == 'activo':
            return redirect("/")
    return render_template("Admin/admin.html", user = session)

#------------------- Users --------------------

@app.route("/admin/panel/crearUsuario", methods = ['POST'])
def insert_user():
    name = request.form['name']
    user = request.form['user']
    _pass = request.form['pass']
    rol = request.form['rol']
    filas = insertar_1_user(name, user, _pass, rol)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel")

#------------------- Alumnos --------------------

@app.route("/admin/panel/crearAlumno", methods = ['POST'])
def insert_alumno():
    name = request.form['name']
    mat = request.form['mat']
    filas = insert_1_alumno(name, mat)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel")

#------------------ Registrar -------------

@app.route("/admin/panel/registrar")
def registrar_prestamo():
    if not session or  session['rol'] not in roles and session['estado'] == 'activo':
        return redirect("/")
    return render_template("Admin/registrarPrestamo.html")

@app.route("/prestamo/registrar", methods=['POST'])
def registrar():
    data = request.get_json()
    alumno = data["alumno"]
    libros = data["libros"]
    fecha_limite = date.today() + timedelta(days=8)

    try: 
        for codigo in libros:
            ejecutar(
                "CALL registrar_prestamo(%s, %s, %s, %s)",
                (alumno, codigo, session['id'], fecha_limite)
            )
        return jsonify({ "ok": True })
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route("/api/libro/codigo", methods=["POST"])
def buscar_libro_codigo():
    codigo = request.json["codigo"]
    libro = buscar_libro_cod(codigo)
    return jsonify(libro)

#----------------- Usuarios -------------
@app.route("/admin/panel/usuarios")
def ver_usuarios():
    if not session or  session['rol'] not in roles:
        return redirect("/")
    users = obtener_usuarios()
    return render_template("Admin/mostrarUsuarios.html", usuarios=users, user=session)

@app.route("/admin/panel/usuarios/baja", methods=['POST'])
def dar_baja_usuario():
    id = request.form['id_usuario']
    filas = dar_baja_1_usuario(id)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/alta", methods=['POST'])
def dar_alta_usuarios():
    id = request.form['id_usuario']
    filas = dar_alta_1_usuario(id)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/editar", methods=['POST'])
def editar_usuario():
    if not es_admin():
        return redirect("/")
    usuario = buscar_user(request.form['id_usuario'])
    if not usuario:
        return index("Operación fallida")
    propio = usuario['id_bibliotecario'] == session['id']
    return render_template("Forms/updateUser.html", usuario=usuario, propio=propio)

@app.route("/admin/panel/usuarios/actualizar", methods=['POST'])
def actualizar_usuario():
    if not es_admin():
        return redirect("/")
    id = int(request.form['id_usuario'])
    name = request.form['name']
    user = request.form['user']
    _pass = request.form['pass']
    propio = id == session['id']
    rol = session['rol'] if propio else request.form['rol']
    try:
        actualizar_1_user(id, name, user, _pass, rol)
    except Error as e:
        return index(e.msg)
    if propio:
        session['nombre'] = name
        session['user'] = user
    return redirect("/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/eliminar", methods=['POST'])
def eliminar_usuario():
    if not es_admin():
        return redirect("/")
    id = int(request.form['id_usuario'])
    if id == session['id']:
        return index("No puedes eliminar tu propio usuario")
    try:
        eliminar_1_user(id)
    except Error as e:
        return index(e.msg)
    return redirect("/admin/panel/usuarios")

#-------------------- Alumnos -------------

@app.route("/admin/panel/alumnos")
def ver_alumnos():
    if session['rol'] not in roles:
        return redirect("/")
    alumnos = obtener_alumnos()
    return render_template("Admin/mostrarAlumnos.html", alumnos=alumnos, user=session)

@app.route("/admin/panel/alumnos/baja", methods=['POST'])
def dar_baja_alumno():
    id = request.form['id_usuario']
    filas = dar_baja_1_alumno(id)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/alta", methods=['POST'])
def dar_alta_alumno():
    id = request.form['id_usuario']
    filas = dar_alta_1_alumno(id)
    if filas == 0:
        return index("Operación fallida")
    return redirect("/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/editar", methods=['POST'])
def editar_alumno():
    if not es_admin():
        return redirect("/")
    alumno = buscar_alumno(request.form['id_alumno'])
    if not alumno:
        return index("Operación fallida")
    return render_template("Forms/updateAlumno.html", alumno=alumno)

@app.route("/admin/panel/alumnos/actualizar", methods=['POST'])
def actualizar_alumno():
    if not es_admin():
        return redirect("/")
    id = request.form['id_alumno']
    name = request.form['name']
    mat = request.form['mat']
    try:
        actualizar_1_alumno(id, name, mat)
    except Error as e:
        return index(e.msg)
    return redirect("/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/eliminar", methods=['POST'])
def eliminar_alumno():
    if not es_admin():
        return redirect("/")
    try:
        eliminar_1_alumno(request.form['id_alumno'])
    except Error as e:
        return index(e.msg)
    return redirect("/admin/panel/alumnos")

#-------------------- Auditorias ----------------
@app.route("/admin/panel/auditorias")
def ver_auditorias():
    if not session or session['rol'] not in roles:
        return redirect("/")
    auditorias = obtener_auditorias()
    return render_template("Admin/mostrarAuditorias.html", 
                           auditorias=auditorias, user=session)

#----------------- Panel prestamos ---------------
@app.route("/admin/panel/prestamos")
def ver_prestamos():
    if not session or session['rol'] not in roles:
        return redirect("/")
    prestamos = obtenerPrestamos()
    return render_template("Admin/mostrarPrestamos.html", prestamos = prestamos, user = session)

@app.route("/admin/panel/prestamos/devolver", methods = ['POST'])
def devolver_prestamo():
    codigo = request.form['codigo_barras']
    registrar_1_devolucion(codigo)
    return redirect("/admin/panel/prestamos")

@app.route("/admin/panel/reportes")
def mostrar_reportes():
    libros = consultar("""
            select l.titulo, l.autor, count(*) as veces_prestado
            from libros l join ejemplares e on e.id_libro = l.id_libro 
                join prestamos p on p.id_ejemplar = e.id_ejemplar
            group by l.id_libro, l.titulo, l.autor
            having count(*) >= 2
            order by veces_prestado desc;
                        """)
    alumnos = consultar("""
            select a.matricula, a.nombre_completo, count(*) as prestamos_vencidos, 
                    max(dias_retraso(p.id_prestamo)) as dias_atraso,
                    group_concat(l.titulo separator ', ') as libros
            from alumnos a join prestamos p on p.id_alumno = a.id_alumno
                 join ejemplares e on e.id_ejemplar = p.id_ejemplar 
                 join libros l on l.id_libro = e.id_libro
            where p.fecha_devolucion is null and dias_retraso(p.id_prestamo) > 0
            group by a.id_alumno, a.matricula, a.nombre_completo
            order by dias_atraso desc;
            """)
    return render_template("Admin/mostrarReportes.html", libros = libros, alumnos=alumnos)

if __name__ == '__main__':
    app.run(debug = True)