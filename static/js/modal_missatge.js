document.addEventListener("DOMContentLoaded", function () {

  function obreMissatge(missatgeId) {
    fetch(`/missatges/api/missatge/${missatgeId}`)
      .then(res => res.json())
      .then(data => {
        
        document.getElementById("modal-assumpte").innerText = data.assumpte;
        document.getElementById("modal-remitent").innerText = data.remitent;
        document.getElementById("modal-data-missatge").innerText = data.data;

     document.getElementById("modal-contingut-missatges").innerHTML =
  (data.contingut || "(missatge buit)").replace(/\n/g, "<br>");


        document.getElementById("modal-missatge").style.display = "flex";
      });
  }

  // Assignem la funció globalment si cal accedir-hi des de HTML onclick
  window.obreMissatge = obreMissatge;
});

function tancaModalMissatge() {
  document.getElementById("modal-missatge").style.display = "none";
}
