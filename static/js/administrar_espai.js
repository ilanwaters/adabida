// ============================================
// Administració de l'espai familiar
// Dades:       window.ADMIN_ESPAI      (definit a administrar_espai.html)
// Traduccions: window.TRAD_ADMIN_ESPAI (definit a administrar_espai.html)
// ============================================

const T = () => window.TRAD_ADMIN_ESPAI;
const FAMILIA_ID = () => window.ADMIN_ESPAI.familiaId;

function postJSON(url, cos) {
    const opcions = { method: 'POST' };
    if (cos !== undefined) {
        opcions.headers = { 'Content-Type': 'application/json' };
        opcions.body = JSON.stringify(cos);
    }
    return fetch(url, opcions).then(res => res.json());
}

// ---------- Modal invitar ----------
function obrirModalInvitar() {
    document.getElementById('modalInvitar').style.display = 'flex';
}

function tancarModalInvitar() {
    document.getElementById('modalInvitar').style.display = 'none';
}

window.addEventListener('click', (event) => {
    const modal = document.getElementById('modalInvitar');
    if (event.target === modal) tancarModalInvitar();
});

// ---------- Membres ----------
function canviarRol(membreId, nouRol) {
    if (!confirm(T().confirmar_rol)) return;
    postJSON(`/familia/${FAMILIA_ID()}/administrar/membre/${membreId}/canviar-rol`, { rol: nouRol })
        .then(data => data.success ? location.reload() : alert(`${T().error}: ${data.message}`));
}

function eliminarMembre(membreId, nomMembre) {
    if (!confirm(T().confirmar_eliminar_membre.replace('{nom}', nomMembre))) return;
    postJSON(`/familia/membre/${membreId}/eliminar`)
        .then(data => data.success ? location.reload() : alert(`${T().error}: ${data.message}`));
}

function toggleVisibilitatMembre(boto) {
    boto.disabled = true;
    postJSON(boto.dataset.url)
        .then(data => {
            if (!data.success) {
                alert(data.error || T().error_visibilitat);
                return;
            }
            const visible = data.visible_public;
            boto.classList.toggle('estat-public', visible);
            boto.classList.toggle('estat-privat', !visible);
            boto.textContent = visible ? T().visible : T().ocult;
        })
        .catch(() => alert(T().error_visibilitat))
        .finally(() => { boto.disabled = false; });
}

// ---------- Foto de membre ----------
function canviarFotoMembre(membreId) {
    document.getElementById('membre-id-foto').value = membreId;
    document.getElementById('modal-foto-membre').style.display = 'flex';
}

function tancarModalFotoMembre() {
    const boto = document.getElementById('btn-guardar-foto-membre');
    document.getElementById('modal-foto-membre').style.display = 'none';
    document.getElementById('foto-preview-container').style.display = 'none';
    document.getElementById('membre-foto-input').value = '';
    boto.disabled = true;
    boto.style.opacity = '0.5';
}

function previewFotoMembre(input) {
    if (!input.files || !input.files[0]) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        const boto = document.getElementById('btn-guardar-foto-membre');
        document.getElementById('foto-preview-image').src = e.target.result;
        document.getElementById('foto-preview-container').style.display = 'block';
        boto.disabled = false;
        boto.style.opacity = '1';
    };
    reader.readAsDataURL(input.files[0]);
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-foto-membre');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        fetch('/familia/membre/pujar-foto', { method: 'POST', body: new FormData(this) })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert(T().foto_guardada);
                    location.reload();
                } else {
                    alert(`${T().error}: ${data.error}`);
                }
            })
            .catch(() => alert(T().error_connexio));
    });
});

// ---------- Heràldica ----------
function pujarHeraldica(familiaId, input) {
    const fitxer = input.files[0];
    if (!fitxer) return;

    const formData = new FormData();
    formData.append('heraldica', fitxer);

    fetch(`/familia/${familiaId}/administrar/heraldica`, { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => data.success ? location.reload() : alert(data.error || T().error_heraldica));
}

// ---------- Visibilitat de l'espai ----------
function toggleVisibilitatPublica() {
    postJSON(`/familia/${FAMILIA_ID()}/administrar/toggle-visibilitat-publica`)
        .then(data => data.success ? location.reload() : alert(data.error || T().error_visibilitat))
        .catch(() => alert(T().error_visibilitat));
}

// ---------- Ubicacions ----------
function eliminarUbicacio(ubicacioId) {
    if (!confirm(T().confirmar_eliminar_ubicacio)) return;
    postJSON(`/familia/ubicacio/${ubicacioId}/eliminar`)
        .then(data => data.success ? location.reload() : alert(`${T().error}: ${data.message}`));
}

function afegirUbicacio() {
    alert(T().en_desenvolupament);
}

function recalcularUbicacions() {
    if (!confirm(T().confirmar_recalcular)) return;
    postJSON(`/familia/${FAMILIA_ID()}/recalcular-ubicacions`)
        .then(data => { alert(data.message); location.reload(); });
}

function validarRelacions() {
    alert(T().en_desenvolupament);
}

// ---------- Configuració ----------
function desarConfiguracio() {
    postJSON(`/familia/${FAMILIA_ID()}/configuracio`, {
        visible_globalment: document.getElementById('visibilitat_global').checked,
        notificacions_actives: document.getElementById('notificacions_actives').checked,
        permisos_edicio_membres: document.getElementById('permisos_edicio_membres').checked,
    }).then(data => alert(data.message));
}

// ---------- Accions de l'espai ----------
function exportarEspai() {
    window.location.href = `/familia/${FAMILIA_ID()}/exportar-pdf`;
}

function ferBackup() {
    window.location.href = `/familia/${FAMILIA_ID()}/backup`;
}

function arxivarEspai() {
    if (!confirm(T().confirmar_arxivar)) return;
    postJSON(`/familia/${FAMILIA_ID()}/arxivar`)
        .then(data => {
            alert(data.message);
            if (data.success) window.location.href = '/familia/les-meves';
        });
}

function confirmarEliminarEspai() {
    const text = prompt(T().confirmar_eliminar_espai);
    if (text === 'ELIMINAR') {
        postJSON(`/familia/${FAMILIA_ID()}/eliminar`)
            .then(data => {
                alert(data.message);
                if (data.success) window.location.href = '/familia/les-meves';
            });
    } else if (text !== null) {
        alert(T().text_incorrecte);
    }
}
// ---------- Pàgina pública: ordre dels blocs ----------
function moureBloc(boto, direccio) {
    const item = boto.closest('li');
    const llista = item.parentNode;
    if (direccio < 0 && item.previousElementSibling) {
        llista.insertBefore(item, item.previousElementSibling);
    } else if (direccio > 0 && item.nextElementSibling) {
        llista.insertBefore(item.nextElementSibling, item);
    }
}