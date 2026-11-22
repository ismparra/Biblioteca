import textwrap
from flask import Flask, Response, render_template, redirect, request
from random import randint
from BD.libros import *
from Extra.colors import PALETTE

app = Flask(__name__)

@app.route("/")
def index():
    q = request.args.get("q", "")
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", books=BOOKS, indices=indices, q=q)

@app.route("/", methods=['POST'])
def turn_back():
    curr = request.form.get('indx', 0)
    q = request.form.get('q', '')
    if q: BOOKS = buscar_libros(q)
    else: BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", books=BOOKS, indices=indices, curr=curr, q=q)

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
    return render_template("Info/libro_info.html", libro=libro, ant=curr, query=q)

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

if __name__ == '__main__':
    app.run(debug = True)