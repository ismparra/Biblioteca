import textwrap
from flask import Flask, Response, render_template, redirect, request
from random import randint
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="biblioteca"
    )

PALETTE = [
    ("#2e7d32", "#a5d63a"), ("#0d47a1", "#42a5f5"),
    ("#b71c1c", "#ff8a65"), ("#4a148c", "#ba68c8"),
    ("#e65100", "#ffd54f"), ("#006064", "#4dd0e1"),
    ("#263238", "#90a4ae"), ("#880e4f", "#f48fb1"),
]

@app.route("/")
def index():
    q = request.args.get("q", "")
    if q:
        BOOKS = buscar_libros(q)
    else:
        BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", books=BOOKS, indices=indices, q=q)

@app.route("/", methods=['POST'])
def turn_back():
    curr = request.form.get('indx', 0)
    q = request.form.get('q', '')
    if q:
        BOOKS = buscar_libros(q)
    else:
        BOOKS = obtener_libros()
    indices = [randint(0, len(PALETTE)-1) for _ in BOOKS]
    return render_template("index.html", books=BOOKS, indices=indices, curr=curr, q=q)

@app.route("/addBook")
def addBook():
    return render_template("Forms/addBook.html")

@app.route("/libros/guardar", methods=['POST'])
def guardar_libro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    ejecutar(
        "INSERT INTO libros (titulo, autor, categoria) VALUES (%s, %s, %s)",
        (titulo, autor, categoria)
    )
    return redirect("/")

@app.route("/libro/info", methods=['POST'])
def libro_info():
    id = request.form['ID']
    curr = request.form.get('curr', 0)
    q = request.form.get('query', '')
    libro = consultar("SELECT * FROM LIBROS WHERE id_libro = %s",(id,))
    return render_template("libro_info.html", libro=libro[0], ant=curr, query=q)

@app.route("/cover/<int:i>.svg")
def cover(i):
    libro = consultar(
        "SELECT titulo FROM libros WHERE id_libro = %s",
        (i,)
    )[0]

    titulo = libro["titulo"]

    c1, c2 = PALETTE[i % len(PALETTE)]

    svg = render_template(
        "cover.svg",
        lines=textwrap.wrap(titulo, 11),
        c1=c1,
        c2=c2,
    )

    return Response(svg, mimetype="image/svg+xml")

def consultar(sql, params=None):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def ejecutar(sql, params=None):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute(sql, params)
    conexion.commit()
    cursor.close()

def obtener_libros():
    return [(fila["titulo"], fila["id_libro"])
            for fila in consultar(
                "SELECT titulo, id_libro FROM libros"
            )]

def buscar_libros(q):
    return [(fila["titulo"], fila["id_libro"])
                for fila in consultar(
                    """
                    SELECT *
                    FROM libros
                    WHERE titulo LIKE %s
                    OR autor LIKE %s
                    """, 
                (f"%{q}%", f"%{q}%")
                )
            ]

if __name__ == '__main__':
    app.run(debug = True)