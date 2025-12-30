// Cerca de membres
document.getElementById('cerca-membres')?.addEventListener('input', function(e) {
  const cerca = e.target.value.toLowerCase();
  filtrarMembres();
});

// Filtres
document.getElementById('filtre-rol')?.addEventListener('change', filtrarMembres);
document.getElementById('ordenar-per')?.addEventListener('change', ordenarMembres);

function filtrarMembres() {
  const cerca = document.getElementById('cerca-membres')?.value.toLowerCase() || '';
  const rolFiltre = document.getElementById('filtre-rol')?.value || '';
  
  const targetes = document.querySelectorAll('.targeta-membre');
  let visibles = 0;
  
  targetes.forEach(targeta => {
    const nom = targeta.dataset.nom || '';
    const rol = targeta.dataset.rol || '';
    
    const coincideixNom = !cerca || nom.includes(cerca);
    const coincideixRol = !rolFiltre || rol === rolFiltre;
    
    if (coincideixNom && coincideixRol) {
      targeta.style.display = '';
      visibles++;
    } else {
      targeta.style.display = 'none';
    }
  });
  
  // Mostrar missatge si no hi ha resultats
  const sensResultats = document.getElementById('sense-resultats-membres');
  if (sensResultats) {
    sensResultats.style.display = visibles === 0 ? 'block' : 'none';
  }
}

function ordenarMembres() {
  const ordenar = document.getElementById('ordenar-per')?.value || 'nom';
  const grid = document.getElementById('grid-membres');
  if (!grid) return;
  
  const targetes = Array.from(grid.querySelectorAll('.targeta-membre'));
  
  targetes.sort((a, b) => {
    if (ordenar === 'nom') {
      return (a.dataset.nom || '').localeCompare(b.dataset.nom || '');
    } else if (ordenar === 'data_adhesio') {
      return (b.dataset.data || 0) - (a.dataset.data || 0);
    }
    return 0;
  });
  
  targetes.forEach(targeta => grid.appendChild(targeta));
}

function veureMembre(membreId) {
  window.location.href = `/familia/membre/${membreId}`;  
}

function editarMembre(membreId) {
  window.location.href = `/familia/membre/${membreId}/editar`; 
}
function tancarModalMembre() {
  document.getElementById('modal-membre').style.display = 'none';
}
