// === FUNCIONS LLISTAT ORGANITZACIONS ===

// Funció genèrica per obrir modal de missatge
function obrirModalMissatge(opcions = {}) {
    // Obrir la modal
    document.getElementById('modal-nou-missatge').style.display = 'block';
    
    // Opcions per defecte
    const config = {
        receptor: opcions.receptor || '',
        assumpte: opcions.assumpte || '',
        contingut: opcions.contingut || '',
        mostrarReceptorValid: opcions.mostrarReceptorValid || false,
        textReceptorValid: opcions.textReceptorValid || ''
    };
    
    // Omplir camps
    document.getElementById('nou-receptor').value = config.receptor;
    document.getElementById('nou-assumpte').value = config.assumpte;
    document.getElementById('nou-contingut').value = config.contingut;
    
    // Receptor vàlid
    const receptorNom = document.getElementById('receptor-nom');
    if (config.mostrarReceptorValid) {
        receptorNom.style.display = 'inline';
        receptorNom.textContent = config.textReceptorValid;
    } else {
        receptorNom.style.display = 'none';
    }
    
    // Netejar resultats cerca
    document.getElementById('resultats-cerca').innerHTML = '';
}

// Contactar organització que ha rebutjat sol·licitud
function contactarOrganitzacio(orgId, nomOrg) {
    obrirModalMissatge({
        receptor: nomOrg,
        assumpte: `Consulta sobre sol·licitud rebutjada`,
        contingut: `Benvolguts,\n\nHe rebut notificació que la meva sol·licitud d'adhesió ha estat rebutjada. M'agradaria conèixer els motius.\n\nGràcies.`,
        mostrarReceptorValid: true,
        textReceptorValid: `→ ${nomOrg}`
    });
}

// Tancar modal de nou missatge
function tancarModalNouMissatge() {
    document.getElementById('modal-nou-missatge').style.display = 'none';
    // Netejar camps
    document.getElementById('nou-receptor').value = '';
    document.getElementById('nou-assumpte').value = '';
    document.getElementById('nou-contingut').value = '';
    document.getElementById('receptor-nom').style.display = 'none';
    document.getElementById('resultats-cerca').innerHTML = '';
}

// Enviar nou missatge
function enviarNouMissatge() {
    const receptor = document.getElementById('nou-receptor').value.trim();
    const assumpte = document.getElementById('nou-assumpte').value.trim();
    const contingut = document.getElementById('nou-contingut').value.trim();
    
    if (!receptor || !assumpte || !contingut) {
        alert('Tots els camps són obligatoris');
        return;
    }
    
    fetch('/organitzacions/contactar_org', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            receptor_login: receptor,
            assumpte: assumpte,
            contingut: contingut
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Missatge enviat correctament');
            tancarModalNouMissatge();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de connexió');
    });
}

// Cerca d'usuaris per enviar missatge (opcional, per autocompletar)
function cercarUsuaris() {
    const terme = document.getElementById('nou-receptor').value.trim();
    const resultatsDiv = document.getElementById('resultats-cerca');
    
    if (terme.length < 2) {
        resultatsDiv.innerHTML = '';
        return;
    }
    
    fetch(`/api/cercar_usuaris?q=${encodeURIComponent(terme)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let html = '';
                data.usuaris.forEach(usuari => {
                    html += `
                        <div class="resultat-usuari" onclick="seleccionarUsuari('${usuari.nom_login}', '${usuari.nom_complet}')">
                            <strong>${usuari.nom_complet}</strong> (@${usuari.nom_login})
                        </div>
                    `;
                });
                resultatsDiv.innerHTML = html;
            }
        })
        .catch(error => console.error('Error cercant usuaris:', error));
}

// Seleccionar usuari destinatari
function seleccionarUsuari(login, nomComplet) {
    document.getElementById('nou-receptor').value = login;
    document.getElementById('receptor-nom').textContent = `→ ${nomComplet}`;
    document.getElementById('receptor-nom').style.display = 'inline';
    document.getElementById('resultats-cerca').innerHTML = '';
}