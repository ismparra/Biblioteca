import textwrap
from flask import Flask, Response, render_template, redirect
from flask import jsonify, request, session
from random import randint
from BD.libros import *
from BD.users import *
from BD.ejemplares import *
from BD.alumnos import *
from BD.auditorias import *
from Extra.colors import PALETTE

app = Flask(__name__)
app.secret_key = "Los que poseen la cumbia"

roles = ("administrador", "operador")

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

#-------------------- Auditorias ----------------
@app.route("/admin/panel/auditorias")
def ver_auditorias():
    if not session or session['rol'] not in roles:
        return redirect("/")
    auditorias = obtener_auditorias()
    return render_template("Admin/mostrarAuditorias.html", 
                           auditorias=auditorias, user=session)


if __name__ == '__main__':
    app.run(debug = True)