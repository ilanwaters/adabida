document.addEventListener('DOMContentLoaded', function () {
  const selector = document.getElementById('selector-taula');
  const capcalera = document.getElementById('capcalera-taula');
  let taula = null;

 function carregaTaula(nomTaula) {
  console.log("🔄 Carregant taula:", nomTaula);

  fetch(`/api/admin/dades/${nomTaula}`)
    .then(response => response.json())
    .then(dades => {
      if (!Array.isArray(dades) || dades.length === 0) {
        console.warn("⚠️ Dades buides o incorrectes");
        if (taula) taula.clear().draw();
        document.getElementById('capcalera-taula').innerHTML = '';
        return;
      }

      const claus = Array.from(
  dades.reduce((acc, obj) => {
    Object.keys(obj).forEach(clau => acc.add(clau));
    return acc;
  }, new Set())
);


      // 🔁 Reset complet del <table>
      if (taula) {
        taula.destroy();
      }
      const taulaHTML = document.getElementById('taula-dades');
      taulaHTML.innerHTML = `
        <thead><tr id="capcalera-taula"></tr></thead>
        <tbody></tbody>
      `;

      // Actualitza la nova capçalera
      const capcalera = document.getElementById('capcalera-taula');
      claus.forEach(clau => {
        const th = document.createElement('th');
        th.textContent = clau;
        capcalera.appendChild(th);
      });

      // Crea nova DataTable
      taula = $('#taula-dades').DataTable({
        data: dades,
        columns: claus.map(clau => ({ data: clau })),
        pageLength: 25,
        responsive: true
      });

      console.log("✅ Taula carregada:", nomTaula);
    })
    .catch(error => {
      console.error("❌ Error carregant taula:", error);
    });
}


  // Carrega inicial
  carregaTaula(selector.value);

  // Canvi de selecció
  selector.addEventListener('change', () => {
    carregaTaula(selector.value);
  });
});
