import textwrap
from flask import Flask, Response, render_template, redirect
from flask import jsonify, request, session, flash, abort
from functools import wraps
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

ADMIN = ("administrador",)
PERSONAL = ("administrador", "operador")

def requiere(*roles):
    """Solo deja pasar a usuarios activos con alguno de esos roles."""
    def decorador(vista):
        @wraps(vista)
        def protegida(*args, **kwargs):
            if session.get('rol') in roles and session.get('estado') == "activo":
                return vista(*args, **kwargs)
            error = "No tienes permiso para realizar esta operación"
            if request.is_json:
                return jsonify(ok=False, error=error), 403
            flash(error, "error")
            return redirect("/")
        return protegida
    return decorador

def mensaje_error(e):
    if e.errno == 1062:
        return "Ya existe un registro con ese código de barras, usuario o matrícula"
    if e.sqlstate == "45000":   # mensajes de los procedimientos y triggers
        return e.msg
    app.logger.error(e)
    return "No se pudo completar la operación en la base de datos"

def hacer(operacion, exito, destino):
    try:
        operacion()
        flash(exito, "ok")
    except Error as e:
        flash(mensaje_error(e), "error")
    return redirect(destino)

@app.errorhandler(Error)
def error_bd(e):
    # fallos fuera de hacer(), por ejemplo si MySQL esta apagado
    if request.is_json:
        return jsonify(ok=False, error=mensaje_error(e)), 500
    return mensaje_error(e), 500

@app.route("/")
def index():
    q = request.args.get("q", "")
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    return render_template("index.html", 
                           books=BOOKS, q=q)

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
@requiere(*ADMIN)
def addBook():
    return render_template("Forms/addBook.html")

@app.route("/libros/guardar", methods=['POST'])
@requiere(*ADMIN)
def guardar_libro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    return hacer(lambda: insertar_libro(titulo, autor, categoria), "Libro registrado", "/")

@app.route("/libro/info", methods=['POST'])
def libro_info():
    id = request.form['ID']
    curr = request.form.get('curr', 0)
    q = request.form.get('query', '')
    libro = buscar_libro(id)
    if not libro:
        flash("Libro no encontrado", "error")
        return redirect("/")
    return render_template("Info/libro_info.html", 
                           libro=libro, ant=curr, query=q, user = session)

@app.route("/libros/eliminar", methods=['POST'])
@requiere(*ADMIN)
def eliminar_libro():
    id = request.form['id_libro']
    return hacer(lambda: eliminar_1_libro(id), "Libro eliminado", "/")

@app.route("/libros/editar", methods=['POST'])
@requiere(*ADMIN)
def editar_libro():
    libro = buscar_libro(request.form['id_libro'])
    if not libro:
        flash("Libro no encontrado", "error")
        return redirect("/")
    return render_template("Forms/updateBook.html", libro=libro)

@app.route("/libros/actualizar", methods=['POST'])
@requiere(*ADMIN)
def actualizar_libro():
    id = request.form['id_libro']
    titulo = request.form['titulo']
    autor = request.form['autor']
    cat = request.form['categoria']
    return hacer(lambda: actualizar_1_libro(id, titulo, autor, cat), "Libro actualizado", "/")

@app.route("/libros/ejemplar", methods=['POST'])
@requiere(*ADMIN)
def ejemplar_libro():
    id = request.form['id_libro']
    return render_template("Forms/addEjemplar.html", id=id)

@app.route("/libros/ejemplar/registrar", methods=['POST'])
@requiere(*ADMIN)
def registrar_ejemplar():
    id = request.form['id']
    codigo = request.form['codigo'].strip()
    return hacer(lambda: registrar_1_ejemplar(codigo, id), "Ejemplar registrado", "/")

@app.route("/cover/<int:i>.svg")
def cover(i):
    libro = buscar_libro(i)
    if not libro:
        abort(404)
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

    if not loged or loged[0]['estado'] != 'activo':
        flash("Usuario o contraseña incorrecto(s)", "error")
        return redirect("/")

    usuario = loged[0]

    session['id'] = usuario['id_bibliotecario']
    session['nombre'] = usuario['nombre_completo']
    session['user'] = usuario['usuario']
    session['rol'] = usuario['rol']
    session['estado'] = usuario['estado']

    flash(f"Bienvenido {usuario['nombre_completo']}", "ok")
    return redirect("/admin/panel" if usuario['rol'] in PERSONAL else "/")

@app.route("/admin/panel")
@requiere(*PERSONAL)
def admin_panel():
    return render_template("Admin/admin.html", user = session)

#------------------- Users --------------------

@app.route("/admin/panel/crearUsuario", methods = ['POST'])
@requiere(*ADMIN)
def insert_user():
    name = request.form['name']
    user = request.form['user']
    _pass = request.form['pass']
    rol = request.form['rol']
    return hacer(lambda: insertar_1_user(name, user, _pass, rol), "Usuario creado", "/admin/panel")

#------------------- Alumnos --------------------

@app.route("/admin/panel/crearAlumno", methods = ['POST'])
@requiere(*ADMIN)
def insert_alumno():
    name = request.form['name']
    mat = request.form['mat'].strip()
    return hacer(lambda: insert_1_alumno(name, mat), "Alumno creado", "/admin/panel")

#------------------ Registrar -------------

@app.route("/admin/panel/registrar")
@requiere(*PERSONAL)
def registrar_prestamo():
    return render_template("Admin/registrarPrestamo.html")

@app.route("/prestamo/registrar", methods=['POST'])
@requiere(*PERSONAL)
def registrar():
    data = request.get_json()
    alumno = data["alumno"].strip()
    libros = data["libros"]
    if not alumno or not libros:
        return jsonify(ok=False, error="Captura la matrícula y escanea al menos un libro"), 400
    # la coma separa los codigos dentro del procedimiento
    if any("," in codigo for codigo in libros):
        return jsonify(ok=False, error="Código de barras no válido"), 400
    fecha_limite = date.today() + timedelta(days=8)

    try:
        registrar_1_prestamo(alumno, libros, session['id'], fecha_limite)
    except Error as e:
        return jsonify(ok=False, error=mensaje_error(e)), 400
    flash(f"Préstamo registrado ({len(libros)} libro(s))", "ok")
    return jsonify(ok=True)

@app.route("/api/libro/codigo", methods=["POST"])
@requiere(*PERSONAL)
def buscar_libro_codigo():
    codigo = request.json["codigo"]
    libro = buscar_libro_cod(codigo)
    return jsonify(libro)

@app.route("/api/alumno/matricula", methods=["POST"])
@requiere(*PERSONAL)
def consultar_alumno_matricula():
    return jsonify(consultar_1_alumno(request.json["matricula"]))

#----------------- Usuarios -------------
@app.route("/admin/panel/usuarios")
@requiere(*PERSONAL)
def ver_usuarios():
    users = obtener_usuarios()
    return render_template("Admin/mostrarUsuarios.html", usuarios=users, user=session)

@app.route("/admin/panel/usuarios/baja", methods=['POST'])
@requiere(*ADMIN)
def dar_baja_usuario():
    id = int(request.form['id_usuario'])
    if id == session['id']:
        flash("No puedes dar de baja tu propio usuario", "error")
        return redirect("/admin/panel/usuarios")
    return hacer(lambda: dar_baja_1_usuario(id), "Usuario dado de baja", "/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/alta", methods=['POST'])
@requiere(*ADMIN)
def dar_alta_usuarios():
    id = request.form['id_usuario']
    return hacer(lambda: dar_alta_1_usuario(id), "Usuario dado de alta", "/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/editar", methods=['POST'])
@requiere(*ADMIN)
def editar_usuario():
    usuario = buscar_user(request.form['id_usuario'])
    if not usuario:
        flash("El usuario no existe", "error")
        return redirect("/admin/panel/usuarios")
    propio = usuario['id_bibliotecario'] == session['id']
    return render_template("Forms/updateUser.html", usuario=usuario, propio=propio)

@app.route("/admin/panel/usuarios/actualizar", methods=['POST'])
@requiere(*ADMIN)
def actualizar_usuario():
    id = int(request.form['id_usuario'])
    name = request.form['name']
    user = request.form['user']
    _pass = request.form['pass']
    propio = id == session['id']
    rol = session['rol'] if propio else request.form['rol']

    def actualizar():
        actualizar_1_user(id, name, user, _pass, rol)
        if propio:
            session['nombre'] = name
            session['user'] = user
    return hacer(actualizar, "Usuario actualizado", "/admin/panel/usuarios")

@app.route("/admin/panel/usuarios/eliminar", methods=['POST'])
@requiere(*ADMIN)
def eliminar_usuario():
    id = int(request.form['id_usuario'])
    if id == session['id']:
        flash("No puedes eliminar tu propio usuario", "error")
        return redirect("/admin/panel/usuarios")
    return hacer(lambda: eliminar_1_user(id), "Usuario eliminado", "/admin/panel/usuarios")

#-------------------- Alumnos -------------

@app.route("/admin/panel/alumnos")
@requiere(*PERSONAL)
def ver_alumnos():
    alumnos = obtener_alumnos()
    return render_template("Admin/mostrarAlumnos.html", alumnos=alumnos, user=session)

@app.route("/admin/panel/alumnos/baja", methods=['POST'])
@requiere(*ADMIN)
def dar_baja_alumno():
    id = request.form['id_usuario']
    return hacer(lambda: dar_baja_1_alumno(id), "Alumno suspendido", "/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/alta", methods=['POST'])
@requiere(*ADMIN)
def dar_alta_alumno():
    id = request.form['id_usuario']
    return hacer(lambda: dar_alta_1_alumno(id), "Alumno reactivado", "/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/editar", methods=['POST'])
@requiere(*ADMIN)
def editar_alumno():
    alumno = buscar_alumno(request.form['id_alumno'])
    if not alumno:
        flash("El alumno no existe", "error")
        return redirect("/admin/panel/alumnos")
    return render_template("Forms/updateAlumno.html", alumno=alumno)

@app.route("/admin/panel/alumnos/actualizar", methods=['POST'])
@requiere(*ADMIN)
def actualizar_alumno():
    id = request.form['id_alumno']
    name = request.form['name']
    mat = request.form['mat'].strip()
    return hacer(lambda: actualizar_1_alumno(id, name, mat), "Alumno actualizado", "/admin/panel/alumnos")

@app.route("/admin/panel/alumnos/eliminar", methods=['POST'])
@requiere(*ADMIN)
def eliminar_alumno():
    id = request.form['id_alumno']
    return hacer(lambda: eliminar_1_alumno(id), "Alumno eliminado", "/admin/panel/alumnos")

#-------------------- Auditorias ----------------
@app.route("/admin/panel/auditorias")
@requiere(*ADMIN)
def ver_auditorias():
    auditorias = obtener_auditorias()
    return render_template("Admin/mostrarAuditorias.html",
                           auditorias=auditorias, user=session)

#----------------- Panel prestamos ---------------
@app.route("/admin/panel/prestamos")
@requiere(*PERSONAL)
def ver_prestamos():
    prestamos = obtenerPrestamos()
    return render_template("Admin/mostrarPrestamos.html", prestamos = prestamos, user = session)

@app.route("/admin/panel/prestamos/devolver", methods = ['POST'])
@requiere(*PERSONAL)
def devolver_prestamo():
    codigo = request.form['codigo_barras']
    return hacer(lambda: registrar_1_devolucion(codigo), "Devolución registrada", "/admin/panel/prestamos")

@app.route("/admin/panel/reportes")
@requiere(*PERSONAL)
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