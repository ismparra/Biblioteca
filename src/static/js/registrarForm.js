const codigo = document.getElementById("codigo");

codigo.addEventListener("keydown", async e => {
    if(e.key !== "Enter") return;

    e.preventDefault();

    const valor = codigo.value.trim();

    const res = await fetch("/api/libro/codigo", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            codigo: valor
        })
    });

    const libro = await res.json();

    agregarLibro(libro);

    codigo.value = "";
});

const prestamo = [];

function agregarLibro(libro){

    if(!libro){
        alert("Libro no encontrado");
        return;
    }

    prestamo.push(libro);

    render();
}

function render(){

    const cont = document.getElementById("lista");

    cont.innerHTML = "";

    prestamo.forEach(libro => {

        const row = document.createElement("div");

        row.innerHTML = `
            <b>${libro.titulo}</b>
            <span>${libro.autor}</span>
        `;

        cont.appendChild(row);
    });
}

async function registrarPrestamo(idAlumno){

    const libros = prestamo.map(x => x.id_libro);

    await fetch("/prestamo/registrar", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            alumno: idAlumno,
            libros: libros
        })
    });
}