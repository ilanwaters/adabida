// Funció per copiar URL
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert(TRAD_ORG.url_copiada);
    });
}

// FUNCIÓ ESBORRAR ORGANITZACIÓ
function esborrarOrganitzacio() {
    const nomOrg = orgIdActual ? document.querySelector('h1').textContent : '';
    const missatge1 = TRAD_ORG.confirmar_esborrar_1;
    const missatge2 = TRAD_ORG.confirmar_esborrar_2;
    const missatgeExit = TRAD_ORG.esborrada_correctament;
    const missatgeError = TRAD_ORG.error_connexio;

    if (confirm(missatge1)) {
        if (confirm(missatge2)) {
            fetch(TRAD_ORG.url_esborrar, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(missatgeExit);
                    window.location.href = TRAD_ORG.url_pagina_personal;
                } else {
                    alert(TRAD_ORG.error + ': ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(missatgeError);
            });
        }
    }
}

// Canviar rol d'un membre
function canviarRol(membreId, nouRol) {
    fetch(TRAD_ORG.url_canviar_rol, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            membre_id: membreId,
            nou_rol: nouRol
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(TRAD_ORG.rol_actualitzat);
        } else {
            alert(TRAD_ORG.error + ': ' + data.error);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(TRAD_ORG.error_connexio);
        location.reload();
    });
}

// Expulsar membre
function expulsarMembre(membreId) {
    if (confirm(TRAD_ORG.confirmar_expulsar)) {
        fetch(TRAD_ORG.url_expulsar_membre, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                membre_id: membreId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(TRAD_ORG.error + ': ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(TRAD_ORG.error_connexio);
        });
    }
}

// Plegar/desplegar blocs
function toggleBloc(element) {
    const bloc = element.parentElement;
    bloc.classList.toggle('tancat');
}

// Sol·licituds
function veureDetallsSolicitud(solicitudId, nomUsuari, missatge) {
    document.getElementById('modal-nom-solicitant').textContent = `${TRAD_ORG.solicitud_de} ${nomUsuari}`;
    document.getElementById('modal-missatge-complet').textContent = missatge;
    document.getElementById('modal-detalls-solicitud').style.display = 'flex';
}

function tancarModalDetalls() {
    document.getElementById('modal-detalls-solicitud').style.display = 'none';
}

function acceptarSolicitud(solicitudId) {
    if (confirm(TRAD_ORG.confirmar_acceptar)) {
        fetch(TRAD_ORG.url_processar_solicitud, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ solicitud_id: solicitudId, accio: 'acceptar' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(TRAD_ORG.solicitud_acceptada);
                location.reload();
            } else {
                alert(TRAD_ORG.error + ': ' + data.error);
            }
        });
    }
}

function rebutjarSolicitud(solicitudId) {
    if (confirm(TRAD_ORG.confirmar_rebutjar)) {
        fetch(TRAD_ORG.url_processar_solicitud, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ solicitud_id: solicitudId, accio: 'rebutjar' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(TRAD_ORG.solicitud_rebutjada);
                location.reload();
            } else {
                alert(TRAD_ORG.error + ': ' + data.error);
            }
        });
    }
}
