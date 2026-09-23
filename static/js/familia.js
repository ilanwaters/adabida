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

function toggleVisibilitatMembre(membreId) {
  fetch(`/familia/membre/${membreId}/toggle-visibilitat`, {
    method: 'POST'
  })
    .then(res => res.json())
    .then(resposta => {
      if (resposta.success) {
        window.location.reload();
      } else {
        alert(resposta.error || 'Error canviant la visibilitat');
      }
    })
    .catch(() => alert('Error canviant la visibilitat'));
}

function toggleVisibilitatPublica() {
  const familiaId = document.getElementById('btn-visibilitat-publica').dataset.familiaId;
  fetch(`/familia/${familiaId}/administrar/toggle-visibilitat-publica`, {
    method: 'POST'
  })
    .then(res => res.json())
    .then(resposta => {
      if (resposta.success) {
        window.location.reload();
      } else {
        alert(resposta.error || 'Error canviant la visibilitat');
      }
    })
    .catch(() => alert('Error canviant la visibilitat'));
}

function ampliarFotoMembre(src) {
  const overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:zoom-out;';
  overlay.innerHTML = `<img src="${src}" style="max-width:90%;max-height:90%;border-radius:8px;">`;
  overlay.addEventListener('click', () => overlay.remove());
  document.body.appendChild(overlay);
}
function canviarFotoMembre(membreId) {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';

  input.addEventListener('change', () => {
    const fitxer = input.files[0];
    if (!fitxer) return;

    const dades = new FormData();
    dades.append('membre_id', membreId);
    dades.append('foto', fitxer);

    fetch('/familia/membre/pujar-foto', {
      method: 'POST',
      body: dades
    })
      .then(res => res.json())
      .then(resposta => {
        if (resposta.success) {
          window.location.reload();
        } else {
          alert(resposta.error || 'Error pujant la foto');
        }
      })
      .catch(() => alert('Error pujant la foto'));
  });

  input.click();
}