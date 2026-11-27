const codigo = document.getElementById("codigo");
const matricula = document.getElementById("alumno");
const prestamo = [];

// regresa undefined si algo fallo (el error ya se mostro)
async function enviar(url, cuerpo){
    try{
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(cuerpo)
        });
        const data = await res.json();
        if(res.ok) return data;
        alert(data.error);
    }catch(e){
        alert("No se pudo conectar con el servidor");
    }
}

matricula.addEventListener("keydown", e => {
    if(e.key !== "Enter") return;
    e.preventDefault();
    codigo.focus();
});

matricula.addEventListener("change", async () => {
    const info = document.getElementById("alumno-info");
    info.textContent = "";
    const valor = matricula.value.trim();
    if(!valor) return;

    const a = await enviar("/api/alumno/matricula", { matricula: valor });
    if(a){
        info.textContent = `${a.nombre} | Préstamos activos: ${a.activos} | Vencidos: ${a.vencidos}`;
    }
});

codigo.addEventListener("keydown", async e => {
    if(e.key !== "Enter") return;

    e.preventDefault();

    const valor = codigo.value.trim();
    codigo.value = "";
    if(!valor) return;

    const libro = await enviar("/api/libro/codigo", { codigo: valor });

    if(libro !== undefined) agregarLibro(libro);
});

function agregarLibro(libro){

    if(!libro){
        alert("Libro no encontrado");
        return;
    }
    if(libro.estado !== "disponible"){
        alert("El ejemplar ya está prestado");
        return;
    }
    if(prestamo.some(x => x.codigo_barras === libro.codigo_barras)){
        alert("Ese ejemplar ya está en la lista");
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
        const titulo = document.createElement("h3");
        const autor = document.createElement("span");
        titulo.textContent = libro.titulo;
        autor.textContent = libro.autor;

        row.append(titulo, autor);
        cont.appendChild(row);
    });
}

async function registrarPrestamo(){

    const data = await enviar("/prestamo/registrar", {
        alumno: matricula.value.trim(),
        libros: prestamo.map(x => x.codigo_barras)
    });

    if(data){
        window.location.href = "/admin/panel/prestamos";
    }
}
