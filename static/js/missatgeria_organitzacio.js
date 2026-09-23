// === FUNCIONS MISSATGERIA D'ORGANITZACIÓ ===

// Variables globals per missatgeria
let missatgeActualOrg = null;


// Canviar entre pestanyes rebuts/enviats
function canviaBustiaOrg(tipus) {
    const rebuts = document.getElementById('bustia-rebuts-org');
    const enviats = document.getElementById('bustia-enviats-org');
    const pestanyes = document.querySelectorAll('.pestanya-bustia');
    
    pestanyes.forEach(p => p.classList.remove('activa'));
    
    if (tipus === 'rebuts') {
        rebuts.style.display = 'block';
        enviats.style.display = 'none';
        pestanyes[0].classList.add('activa');
    } else {
        rebuts.style.display = 'none';
        enviats.style.display = 'block';
        pestanyes[1].classList.add('activa');
    }
}

// Obrir missatge per llegir
function obreMissatgeOrg(missatgeId) {
    fetch(`/organitzacions/api/missatge/${missatgeId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                missatgeActualOrg = data.missatge;
                
                document.getElementById('modal-assumpte-missatge-org').textContent = data.missatge.assumpte;
                document.getElementById('modal-remitent-org').textContent = data.missatge.emissor_nom;
                document.getElementById('modal-data-org').textContent = data.missatge.data_env;
                document.getElementById('modal-contingut-missatge-org').textContent = data.missatge.contingut;
                
                document.getElementById('modal-missatge-org').style.display = 'flex';
                
                // Marcar com llegit
                marcarComLlegitOrg(missatgeId);
            } else {
                alert('Error carregant missatge: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de connexió');
        });
}

// Marcar missatge com llegit
function marcarComLlegitOrg(missatgeId) {
    fetch(`/organitzacions/marcar_llegit/${missatgeId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualitzar visualmente (treure classe no-llegit)
            const missatgeElement = document.querySelector(`[onclick="obreMissatgeOrg(${missatgeId})"]`).closest('.missatge-item');
            if (missatgeElement) {
                missatgeElement.classList.remove('no-llegit');
            }
        }
    });
}

// Tancar modal de missatge
function tancarModalMissatgeOrg() {
    document.getElementById('modal-missatge-org').style.display = 'none';
    missatgeActualOrg = null;
}

// Obrir modal per nou missatge
function obreModalNouMissatgeOrg() {
    document.getElementById('modal-nou-missatge-org').style.display = 'flex';
    document.getElementById('nou-receptor-org').focus();
}

// Tancar modal nou missatge
function tancarModalNouMissatgeOrg() {
    document.getElementById('modal-nou-missatge-org').style.display = 'none';
    // Netejar camps
    document.getElementById('nou-receptor-org').value = '';
    document.getElementById('nou-assumpte-org').value = '';
    document.getElementById('nou-contingut-org').value = '';
    document.getElementById('receptor-nom-org').style.display = 'none';
    document.getElementById('resultats-cerca-org').innerHTML = '';
}

// Cerca d'usuaris per enviar missatge
function cercarUsuarisOrg() {
    const terme = document.getElementById('nou-receptor-org').value.trim();
    const resultatsDiv = document.getElementById('resultats-cerca-org');
    
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
                        <div class="resultat-usuari" onclick="seleccionarUsuariOrg('${usuari.nom_login}', '${usuari.nom_complet}')">
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
function seleccionarUsuariOrg(login, nomComplet) {
    document.getElementById('nou-receptor-org').value = login;
    document.getElementById('receptor-nom-org').textContent = nomComplet;
    document.getElementById('receptor-nom-org').style.display = 'inline';
    document.getElementById('resultats-cerca-org').innerHTML = '';
}

// Enviar nou missatge com a organització
function enviarNouMissatgeOrg() {
    const receptor = document.getElementById('nou-receptor-org').value.trim();
    const assumpte = document.getElementById('nou-assumpte-org').value.trim();
    const contingut = document.getElementById('nou-contingut-org').value.trim();
    
    if (!receptor || !assumpte || !contingut) {
        alert('Tots els camps són obligatoris');
        return;
    }
    
    fetch('/organitzacions/enviar_missatge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            organitzacio_id: orgIdActual,
            receptor_login: receptor,
            assumpte: assumpte,
            contingut: contingut
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Missatge enviat correctament');
            tancarModalNouMissatgeOrg();
            location.reload(); // Recarregar per mostrar missatge enviat
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de connexió');
    });
}

// Respondre a un missatge
function respondreComOrganitzacio() {
    if (!missatgeActualOrg) return;
    
    tancarModalMissatgeOrg();
    obreModalNouMissatgeOrg();
    
    // Pre-omplir camps per resposta
    document.getElementById('nou-receptor-org').value = missatgeActualOrg.emissor_login;
    document.getElementById('receptor-nom-org').textContent = missatgeActualOrg.emissor_nom;
    document.getElementById('receptor-nom-org').style.display = 'inline';
    
    const assumpteOriginal = missatgeActualOrg.assumpte;
    const nouAssumpte = assumpteOriginal.startsWith('Re: ') ? assumpteOriginal : `Re: ${assumpteOriginal}`;
    document.getElementById('nou-assumpte-org').value = nouAssumpte;
    
    document.getElementById('nou-contingut-org').focus();
}

// Eliminar missatge rebut
function eliminarMissatgeOrg(missatgeId) {
    if (confirm('Segur que vols eliminar aquest missatge?')) {
        fetch(`/organitzacions/eliminar_missatge/${missatgeId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        });
    }
}

// Eliminar missatge enviat
function eliminarMissatgeEnviatOrg(missatgeId) {
    if (confirm('Segur que vols eliminar aquest missatge enviat?')) {
        fetch(`/organitzacions/eliminar_missatge_enviat/${missatgeId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        });
    }
}

// === FUNCIÓ PER CONTACTAR ORGANITZACIÓ (des del botó rebutjat) ===
function contactarOrganitzacio(orgId, nomOrg) {
    // Aquesta funció s'executaria des del llistat d'organitzacions
    // Redirigeix a una pàgina específica per contactar l'organització
    window.location.href = `/organitzacions/contactar/${orgId}`;
}