// static/js/galeria.js

document.addEventListener("DOMContentLoaded", function () {
  const botons = document.querySelectorAll(".subpestanyes-galeria .subpestanya");

  botons.forEach(boto => {
    boto.addEventListener("click", function () {
      // Treu "activa" de tots els botons
      botons.forEach(b => b.classList.remove("activa"));
      boto.classList.add("activa");

      // Amaga totes les subpestanyes
      document.getElementById("subpestanya-destacades").classList.remove("visible");
      document.getElementById("subpestanya-destacades").classList.add("ocult");

      document.getElementById("subpestanya-exposicions").classList.remove("visible");
      document.getElementById("subpestanya-exposicions").classList.add("ocult");

      // Mostra la subpestanya clicada
      const id = boto.getAttribute("data-subpestanya");
      const activa = document.getElementById("subpestanya-" + id);
      activa.classList.remove("ocult");
      activa.classList.add("visible");
    });
  });
});

function mostrarSubpestanyaGaleria(id) {
  document.getElementById("subpestanya-destacades").classList.add("ocult");
  document.getElementById("subpestanya-exposicions").classList.add("ocult");
  document.getElementById("subpestanya-" + id).classList.remove("ocult");

  document.querySelectorAll(".subpestanyes-galeria .subpestanya").forEach(el => {
  el.classList.remove("activa");
});
event.target.classList.add("activa");

}
     
function tancaLightboxIObreModal(entradaId, usuariLogin) {
  if (typeof lightbox !== "undefined" && lightbox.end) {
    lightbox.end();
  }
  setTimeout(() => {
    obreModal(entradaId, usuariLogin);
  }, 300);
}