const modal = document.getElementById("login-modal");

document.getElementById("admin-btn")
    .addEventListener("click", () => {
        modal.classList.add("open");
    });

document.getElementById("close-login")
    .addEventListener("click", () => {
        modal.classList.remove("open");
    });