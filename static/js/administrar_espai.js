
// Funcions JavaScript per l'administració

function obrirModalInvitar() {
    document.getElementById('modalInvitar').style.display = 'flex';
}

function tancarModalInvitar() {
    document.getElementById('modalInvitar').style.display = 'none';
}

function canviarRol(membreId, nouRol) {
    if (confirm('Segur que vols canviar el rol d\'aquest membre?')) {
        fetch(`/familia/membre/${membreId}/canviar-rol`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rol: nouRol })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}

function eliminarMembre(membreId, nomMembre) {
    if (confirm(`Segur que vols eliminar ${nomMembre} de l'espai familiar?\n\nAquesta acció no es pot desfer.`)) {
        fetch(`/familia/membre/${membreId}/eliminar`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}

function eliminarUbicacio(ubicacioId, tipus) {
    if (confirm('Segur que vols eliminar aquesta ubicació?')) {
        fetch(`/familia/ubicacio/${ubicacioId}/eliminar`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}

function afegirUbicacio(tipus) {
    alert('Funció en desenvolupament: Afegir ubicació ' + tipus);
}

function recalcularUbicacions() {
    if (confirm('Això recalcularà les ubicacions actuals basant-se en les adreces dels membres. Continuar?')) {
        fetch(`/familia/{{ familia.id }}/recalcular-ubicacions`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
    }
}

function validarRelacions() {
    alert('Funció en desenvolupament: Validar consistència de relacions');
}

function desarConfiguracio() {
    const config = {
        visible_globalment: document.getElementById('visibilitat_global').checked,
        notificacions_actives: document.getElementById('notificacions_actives').checked,
        permisos_edicio_membres: document.getElementById('permisos_edicio_membres').checked
    };
    
    fetch(`/familia/{{ familia.id }}/configuracio`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

function exportarEspai() {
    window.location.href = `/familia/{{ familia.id }}/exportar-pdf`;
}

function ferBackup() {
    window.location.href = `/familia/{{ familia.id }}/backup`;
}

function arxivarEspai() {
    if (confirm('Segur que vols arxivar aquest espai?\n\nRomandrà accessible però no es podrà editar.')) {
        fetch(`/familia/{{ familia.id }}/arxivar`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                window.location.href = '/familia/les-meves';
            }
        });
    }
}

function confirmarEliminarEspai() {
    const confirmText = prompt('Aquesta acció ELIMINARÀ PERMANENTMENT tot l\'espai familiar.\n\nEscriu "ELIMINAR" per confirmar:');
    
    if (confirmText === 'ELIMINAR') {
        fetch(`/familia/{{ familia.id }}/eliminar`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                window.location.href = '/familia/les-meves';
            }
        });
    } else if (confirmText !== null) {
        alert('Text incorrecte. Operació cancel·lada.');
    }
}

// Tancar modal en clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modalInvitar');
    if (event.target === modal) {
        tancarModalInvitar();
    }
}

function canviarFotoMembre(membreId) {
    alert('Funció en desenvolupament: Canviar foto membre ' + membreId);
    // TODO: Modal per pujar foto
}
