// Obrir modal de contactes
function obreModalContactes() {
    carregarContactes();
    document.getElementById('modal-contactes').style.display = 'flex';
}

// Tancar modal de contactes
function tancarModalContactes() {
    document.getElementById('modal-contactes').style.display = 'none';
}

// Carregar llista de contactes
function carregarContactes() {
    fetch('/contactes/llistar_contactes')
    .then(response => response.json())
    .then(contactes => {
        const llista = document.getElementById('llista-contactes');
        if (contactes.length === 0) {
            llista.innerHTML = `
                <div style="text-align: center; color: #666; margin: 2rem 0;">
                    <p>No tens contactes encara</p>
                    <small>Afegeix contactes des dels perfils d'altres usuaris</small>
                </div>
            `;
        } else {
            llista.innerHTML = contactes.map(contacte => `
                <div class="contacte-item" onclick="seleccionarContacte('${contacte.nom_login}', '${contacte.nom}')">
                    <div class="contacte-info">
                        <strong>${contacte.nom}</strong>
                        <small>@${contacte.nom_login}</small>
                        ${contacte.nom_personalitzat ? `<em>(${contacte.nom_personalitzat})</em>` : ''}
                    </div>
                </div>
            `).join('');
        }
    })
    .catch(error => {
        console.error('Error carregant contactes:', error);
        document.getElementById('llista-contactes').innerHTML = 
            '<p style="color: #dc3545; text-align: center;">Error carregant contactes</p>';
    });
}

// Seleccionar un contacte
function seleccionarContacte(login, nom) {
    tancarModalContactes();
    obreModalNouMissatge(login, nom);
}

// Obrir modal nou missatge directe (sense contacte)
function obreModalNouMissatgeDirecte() {
    tancarModalContactes();
    obreModalNouMissatge();
}