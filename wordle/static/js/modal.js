document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("howto-modal");
    const btn = document.getElementById("howto-btn");
    const span = document.querySelector(".close-btn");

    btn.onclick = function () {
        modal.style.display = "block";
    }

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
});