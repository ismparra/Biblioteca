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

    const cont = document.getElementById("prestamo-lista");
    cont.innerHTML = "";
    document.getElementById("cantidad").textContent = prestamo.length;

    prestamo.forEach(libro => {

        const row = document.createElement("div");

        row.innerHTML = `
            <h3>${libro.titulo}</h3>
            <span>${libro.autor}</span>
        `;

        cont.appendChild(row);
    });
}

async function registrarPrestamo(){

    const alumno = document.getElementById("alumno").value.trim();

    const libros = prestamo.map(x => x.codigo_barras);


    const res = await fetch("/prestamo/registrar", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            alumno: alumno,
            libros: libros
        })
    });

    const data = await res.json();

    if(data.ok){
    window.location.href = "/admin/panel/prestamos";
    }else{
        alert(data.error);
    }
}