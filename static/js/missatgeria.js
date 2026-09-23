// ===== MISSATGERIA.JS - FUNCIONALITAT COMPLETA =====

// CANVIAR PESTANYES REBUTS/ENVIATS
function canviaBustia(quina) {
  const rebuts = document.getElementById("bustia-rebuts");
  const enviats = document.getElementById("bustia-enviats");
  const pestanyes = document.querySelectorAll(".pestanya-bustia");
  
  pestanyes.forEach(p => p.classList.remove("activa"));

  if (quina === "rebuts") {
    rebuts.style.display = "block";
    enviats.style.display = "none";
    pestanyes[0].classList.add("activa");
  } else {
    rebuts.style.display = "none";
    enviats.style.display = "block";
    pestanyes[1].classList.add("activa");
  }
}

// OBRIR MODAL PER VEURE MISSATGE COMPLET
function obreMissatge(missatgeId) {
  console.log('Obrint missatge ID:', missatgeId);
  
  fetch(`/missatges/api/missatge/${missatgeId}`, {
    credentials: 'same-origin'
  })
    .then(response => {
      console.log('Response status:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('Dades rebudes:', data);
      
      if (data.error) {
        alert('Error: ' + data.error);
        return;
      }
      
      // Usar els IDs EXACTES del HTML del template
      document.getElementById('modal-assumpte-missatge').textContent = data.assumpte;
      document.getElementById('modal-remitent').textContent = data.remitent;
      document.getElementById('modal-data').textContent = data.data;
      document.getElementById('modal-contingut-missatge').textContent = data.contingut;
      pintarArxiusMissatge(data.arxius || []);
          window.emissorActual = data.emissor_login;
          window.assumpteActual = data.assumpte; 
      
      // Mostrar modal
      document.getElementById('modal-missatge').style.display = 'flex';
      document.body.style.overflow = 'hidden';
    })
    .catch(error => {
      console.error('Error carregant missatge:', error);
      alert('Error de connexió carregant el missatge');
    });
}
function respondreMissatge() {
  tancarModalMissatge();
  document.getElementById('nou-receptor').value = window.emissorActual;
  document.getElementById('nou-assumpte').value = 'Re: ' + window.assumpteActual;
  document.getElementById('modal-nou-missatge').style.display = 'flex';
}
// TANCAR MODAL DE VEURE MISSATGE (nom exacte del HTML)
function tancarModalMissatge() {
  document.getElementById('modal-missatge').style.display = 'none';
  document.body.style.overflow = 'auto';
}

function obreModalNouMissatge(receptorLogin = '', receptorNom = '') {
  console.log('Obrint modal nou missatge');
  
  // Si ve amb paràmetres (des de contactes), precarrega el receptor
  if (receptorLogin) {
    document.getElementById('nou-receptor').value = receptorLogin;
    document.getElementById('receptor-nom').textContent = receptorNom;
    document.getElementById('receptor-nom').style.display = 'inline';
  } else {
    // Si s'obre directe, netejar formulari
    document.getElementById('nou-receptor').value = '';
    document.getElementById('receptor-nom').style.display = 'none';
  }
  
  // Sempre netejar assumpte i contingut
  document.getElementById('nou-assumpte').value = '';
  document.getElementById('nou-contingut').value = '';
  document.getElementById('nou-arxius').value = '';
  arxiusSeleccionatsNouMissatge = [];
  pintarLlistaArxiusSeleccionats();
  // Mostrar modal
  document.getElementById('modal-nou-missatge').style.display = 'flex';
  document.body.style.overflow = 'hidden';
  
  // Focus al primer camp (receptor o assumpte si ja està omplert)
  setTimeout(() => {
    if (!receptorLogin) {
      document.getElementById('nou-receptor').focus();
    } else {
      document.getElementById('nou-assumpte').focus();
    }
  }, 100);
}

// TANCAR MODAL NOU MISSATGE
function tancarModalNouMissatge() {
  document.getElementById('modal-nou-missatge').style.display = 'none';
  document.body.style.overflow = 'auto';
}

// ENVIAR NOU MISSATGE
function enviarNouMissatge() {
  const receptor = document.getElementById('nou-receptor').value.trim();
  const assumpte = document.getElementById('nou-assumpte').value.trim();
  const contingut = document.getElementById('nou-contingut').value.trim();
  const arxius = arxiusSeleccionatsNouMissatge;

  if (!receptor || !assumpte || !contingut) {
    alert('Tots els camps són obligatoris');
    return;
  }

  fetch(`/contactes/es_contacte/${encodeURIComponent(receptor)}`, { credentials: 'same-origin' })
    .then(r => r.json())
    .then(info => {
      if (info.existeix && !info.es_contacte) {
        const vol = confirm('Aquest usuari no forma part dels teus contactes. Vols afegir-lo?');
        if (vol) {
          fetch('/contactes/afegir_contacte', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contacte_id: info.usuari_id })
          }).then(() => enviarMissatgeReal(receptor, assumpte, contingut, arxius));
        } else {
          enviarMissatgeReal(receptor, assumpte, contingut, arxius);
        }
      } else {
        enviarMissatgeReal(receptor, assumpte, contingut, arxius);
      }
    });
}

function enviarMissatgeReal(receptor, assumpte, contingut, arxius) {
  const formData = new FormData();
  formData.append('receptor_id', receptor);
  formData.append('assumpte', assumpte);
  formData.append('contingut', contingut);

  if (arxius) {
    for (let i = 0; i < arxius.length; i++) {
      formData.append('arxius', arxius[i]);
    }
  }

  fetch('/missatges/enviar_missatge', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('Missatge enviat correctament!');
      tancarModalNouMissatge();
      location.reload();
    } else {
      alert('Error: ' + (data.error || 'No s\'ha pogut enviar el missatge'));
    }
  });
}

// CERCAR USUARIS PER AL CAMP RECEPTOR
function cercarUsuaris() {
  const query = document.getElementById('nou-receptor').value.trim();
  
  if (query.length < 2) {
    document.getElementById('resultats-cerca').innerHTML = '';
    return;
  }
  
  fetch(`/missatges/api/usuaris?q=${encodeURIComponent(query)}`, {
    credentials: 'same-origin'
  })
    .then(response => response.json())
    .then(usuaris => {
      let html = '';
      usuaris.forEach(usuari => {
        html += `
          <div class="usuari-resultat" onclick="seleccionarUsuari(${usuari.id}, '${usuari.nom}')">
            <strong>${usuari.nom}</strong>
            <small>${usuari.nom_login}</small>
          </div>
        `;
      });
      document.getElementById('resultats-cerca').innerHTML = html;
    })
    .catch(error => {
      console.error('Error cercant usuaris:', error);
    });
}

// SELECCIONAR USUARI DEL CERCADOR
function seleccionarUsuari(usuariId, nomUsuari) {
  document.getElementById('nou-receptor').value = usuariId;
  document.getElementById('receptor-nom').textContent = nomUsuari;
  document.getElementById('receptor-nom').style.display = 'inline';
  document.getElementById('resultats-cerca').innerHTML = '';
}

// TANCAR MODALS AMB ESC
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    tancarModalMissatge();
    tancarModalNouMissatge();
  }
});

// TANCAR MODALS CLICANT FORA
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal')) {
    tancarModalMissatge();
    tancarModalNouMissatge();
  }
});

// INICIALITZACIÓ
document.addEventListener("DOMContentLoaded", function () {
  console.log('Missatgeria.js carregat correctament');
});

function afegirContacte(usuariId, login, nom) {
  fetch('/contactes/afegir_contacte', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contacte_id: usuariId })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(`${nom} afegit als teus contactes!`);
      document.getElementById('modal-afegir-contacte-container').innerHTML = '';
    } else {
      alert('Error: ' + (data.error || 'No s\'ha pogut afegir el contacte'));
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error de connexió');
  });
}

function pintarArxiusMissatge(arxius) {
  const contenidor = document.getElementById('modal-arxius-missatge');

  if (!arxius.length) {
    contenidor.innerHTML = '';
    return;
  }

  const IMATGES = ['jpg', 'jpeg', 'png', 'webp', 'gif'];

  let html = '<div class="graella-arxius-missatge">';
  arxius.forEach(arxiu => {
    const ext = (arxiu.tipus || '').toLowerCase();
    if (IMATGES.includes(ext)) {
      html += `
        <a href="${arxiu.url}" target="_blank" class="arxiu-missatge-item">
          <img src="${arxiu.url}" alt="${arxiu.nom_fitxer}">
        </a>`;
    } else {
      const icona = ext === 'pdf' ? '/static/icons/pdf.png' : `/static/icons/${ext}.png`;
      html += `
        <a href="${arxiu.url}" target="_blank" class="arxiu-missatge-item arxiu-missatge-document">
          <img src="${icona}" alt="${ext}" onerror="this.src='/static/icons/sense_imatge.png'">
          <span>${arxiu.nom_fitxer}</span>
        </a>`;
    }
  });
  html += '</div>';

  contenidor.innerHTML = html;
}

let arxiusSeleccionatsNouMissatge = [];

function afegirArxiusSeleccionats(files) {
  for (let i = 0; i < files.length; i++) {
    arxiusSeleccionatsNouMissatge.push(files[i]);
  }
  document.getElementById('nou-arxius').value = ''; // permet reseleccionar el mateix fitxer després
  pintarLlistaArxiusSeleccionats();
}

function eliminarArxiuSeleccionat(index) {
  arxiusSeleccionatsNouMissatge.splice(index, 1);
  pintarLlistaArxiusSeleccionats();
}

function pintarLlistaArxiusSeleccionats() {
  const contenidor = document.getElementById('llista-arxius-seleccionats');
  const IMATGES = ['jpg', 'jpeg', 'png', 'webp', 'gif'];

  contenidor.innerHTML = arxiusSeleccionatsNouMissatge.map((f, i) => {
    const ext = f.name.split('.').pop().toLowerCase();
    const esImatge = IMATGES.includes(ext);
    const miniatura = esImatge
      ? `<img src="${URL.createObjectURL(f)}" alt="${f.name}">`
      : `<img src="/static/icons/${ext === 'pdf' ? 'pdf' : ext}.png" alt="${ext}" onerror="this.src='/static/icons/sense_imatge.png'">`;

    return `
      <div class="arxiu-seleccionat">
        ${miniatura}
        <span>${f.name}</span>
        <span class="boto-treure-arxiu" onclick="eliminarArxiuSeleccionat(${i})">&times;</span>
      </div>
    `;
  }).join('');
}