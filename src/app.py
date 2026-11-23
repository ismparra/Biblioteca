import textwrap
from flask import Flask, Response, render_template, redirect, request, session
from random import randint
from BD.libros import *
from BD.users import *
from Extra.colors import PALETTE

app = Flask(__name__)
app.secret_key = "Los que poseen la cumbia"

@app.route("/")
def index(msg = None):
    q = request.args.get("q", "")
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", 
                           books=BOOKS, indices=indices, q=q, Message = msg)

@app.route("/", methods=['POST'])
def turn_back():
    curr = request.form.get('indx', 0)
    q = request.form.get('q', '')
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", 
                           books=BOOKS, indices=indices, curr=curr, q=q)

# ------------------- LIBROS -------------------

@app.route("/addBook")
def addBook():
    return render_template("Forms/addBook.html")

@app.route("/libros/guardar", methods=['POST'])
def guardar_libro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    insertar_libro(titulo, autor, categoria)
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
    eliminar_1_libro(id)
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
    actualizar_1_libro(id, titulo, autor, cat)
    return redirect('/')

@app.route("/cover/<int:i>.svg")
def cover(i):
    libro = buscar_libro(i)
    titulo = libro["titulo"]
    c1, c2 = PALETTE[i % len(PALETTE)]
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
    usuario = loged[0]
    if not usuario: 
        return index("Usuario o contraseña incorrecto(s)")

    session['id'] = usuario['id_bibliotecario']
    session['nombre'] = usuario['nombre_completo']
    session['user'] = usuario['usuario']
    session['rol'] = usuario['rol']
    session['estado'] = usuario['estado']

    if session['rol'] == "operador":
        return redirect("/admin/operador")

    if session['rol'] == "administrador":
        return redirect("/admin/panel")

    return redirect("/")

@app.route("/admin/operador")
def operator_panel():
    return render_template("Admin/operator.html")

@app.route("/admin/panel")
def admin_panel():
    return render_template("Admin/admin.html")

if __name__ == '__main__':
    app.run(debug = True)