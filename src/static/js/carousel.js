(function () {
  const stage = document.getElementById("stage");
  const dots = document.getElementById("dots");
  const indx = document.getElementById("bar")
  // const title = document.getElementById("title");
  // const sub = document.getElementById("sub");

  let cur = 0, moved = false;
  
  const cards = () => [...stage.children];

  function layout() {
    const list = cards();
    if (!list.length) return;
    const cw = list[0].offsetWidth;
    list.forEach((c, i) => {
      const o = i - cur, a = Math.abs(o), s = o < 0 ? -1 : 1;
      const x = o === 0 ? 0 : s * (cw * 0.78 + (a - 1) * cw * 0.3);
      const z = o === 0 ? 90 : -a * 40;
      const r = o === 0 ? 0 : -s * 58;
      Object.assign(c.style, {
        transform: `translateX(${x}px) translateZ(${z}px) rotateY(${r}deg)`,
        zIndex: 100 - a,
        opacity: a > 5 ? 0 : 1,
        pointerEvents: a > 5 ? "none" : "auto",
        filter: o === 0 ? "none" : `brightness(${Math.max(0.45, 1 - a * 0.12)})`,
      });
      c.classList.toggle("sel", o === 0);
      dots.children[i]?.classList.toggle("on", o === 0);
    });
    // title.textContent = list[cur].dataset.title;
    // sub.textContent = `${cur + 1} de ${list.length} · ${list[cur].dataset.sub}`;
  }

  function go(i) {
    cur = Math.max(0, Math.min(cards().length - 1, i));
    layout();
  }

  function buildDots() {
    dots.innerHTML = "";
    cards().forEach((_, i) => {
      const d = document.createElement("i");
      d.onclick = () => go(i);
      dots.appendChild(d);
    });
  }

  // Click en tarjeta (delegación)
  stage.addEventListener("click", e => {
    const card = e.target.closest(".card");
    const i = cards().indexOf(card);
    if (i >= 0 && !moved) go(i);
  });

  // Teclado y rueda
  document.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") go(cur + 1);
    if (e.key === "ArrowLeft") go(cur - 1);
    if (e.key === "Enter") {
      const libroSeleccionado = cards()[cur];
      const id = libroSeleccionado.dataset.id;
      document.getElementById("bookId").value = id;
      document.getElementById("bookCurr").value = cur;
      document.getElementById("bookQuery").value = document.getElementById("q").value;
      document.getElementById("bookForm").submit();
    }
  });
  let lastWheel = 0;
  stage.addEventListener("wheel", e => {
    e.preventDefault();
    const now = Date.now();
    if (now - lastWheel < 140) return;
    lastWheel = now;
    go(cur + ((e.deltaY || e.deltaX) > 0 ? 1 : -1));
  }, { passive: false });

  // Arrastre
  let sx = null, base = 0;
  stage.addEventListener("pointerdown", e => { sx = e.clientX; base = cur; moved = false; });
  window.addEventListener("pointermove", e => {
    if (sx === null) return;
    const dx = e.clientX - sx;
    if (Math.abs(dx) > 6) moved = true;
    go(base - Math.round(dx / 70));
  });
  window.addEventListener("pointerup", () => {
    sx = null;
    setTimeout(() => (moved = false));
  });
  window.addEventListener("resize", layout);

  // Inicializar primero, antes de cualquier listener opcional
  buildDots();
  layout();
  go(Number(indx.dataset.indx))
})();