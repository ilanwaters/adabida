let grupPendentId = null;

function toggleBloc(element) {
    element.parentElement.classList.toggle('tancat');
}

function obreModalDocument(grupId) {
    const grup = GRUPS_DOCUMENTS[grupId];
    if (!grup) return;

    document.getElementById('modal-document-grup-titol').textContent = grup.titol || window.textosDocuments.senseTitol;
    document.getElementById('modal-document-grup-descripcio').textContent = grup.descripcio || '';
    document.getElementById('modal-document-autor').innerHTML = grup.autor_nom
        ? `${window.textosDocuments.pujatPer} <a href="/perfil/${grup.autor_login}" class="enllac-perfil" target="_blank">${grup.autor_nom}</a> (${grup.data_pujada})`
        : '';
    document.getElementById('modal-document-visibilitat').textContent = grup.visible_public ? window.textosDocuments.public : window.textosDocuments.privat;

    const botoEditarDoc = document.getElementById('boto-editar-document');
    if (botoEditarDoc) botoEditarDoc.dataset.id = grupId;
    const botoEliminarDoc = document.getElementById('boto-eliminar-document');
    if (botoEliminarDoc) botoEliminarDoc.dataset.id = grupId;

    const icones = document.getElementById('modal-document-icones');
    icones.innerHTML = '';

    grup.documents.forEach(doc => {
        const peu = doc.titol && doc.any_document ? `${doc.titol} (${doc.any_document})` : (doc.titol || doc.any_document || '');

        const contenidor = document.createElement('div');
        contenidor.style.cssText = 'display:flex; flex-direction:column; align-items:center; width:110px;';

        if (doc.tipus === 'pdf') {
            const icona = document.createElement('div');
            icona.style.cssText = 'width:100px; height:100px; cursor:pointer; display:flex; align-items:center; justify-content:center;';
            icona.innerHTML = '<i class="fas fa-file-pdf" style="font-size:3.5rem; color:#dc3545;"></i>';
            icona.addEventListener('click', () => obreDocumentActiu(doc));
            contenidor.appendChild(icona);
        } else {
            const link = document.createElement('a');
            link.href = doc.nom_fitxer;
            link.setAttribute('data-lightbox', 'grup-' + grupId);
            const parts = [];
            if (doc.titol) parts.push(doc.titol);
            if (doc.any_document) parts.push(doc.any_document);
            if (doc.descripcio) parts.push(doc.descripcio);
            link.setAttribute('data-title', parts.join(' — '));
            link.innerHTML = `<img src="${doc.nom_fitxer}" style="width:100px; height:100px; object-fit:cover; border-radius:6px; cursor:pointer;">`;
            contenidor.appendChild(link);
        }

        if (peu) {
            const etiqueta = document.createElement('small');
            etiqueta.textContent = peu;
            etiqueta.style.cssText = 'margin-top:6px; text-align:center; color:#555; word-break:break-word;';
            contenidor.appendChild(etiqueta);
        }

        icones.appendChild(contenidor);
    });

    mostraEstatResum();
    document.getElementById('modal-document').style.display = 'flex';
}

function mostraEstatResum() {
    document.getElementById('modal-document-resum').style.display = 'block';
    document.getElementById('modal-document-actiu').style.display = 'none';
}

function obreDocumentActiu(doc) {
    document.getElementById('modal-document-resum').style.display = 'none';

    const actiu = document.getElementById('modal-document-actiu');
    actiu.style.display = 'flex';

    const visor = document.getElementById('modal-document-actiu-visor');
    if (doc.tipus === 'pdf') {
        visor.innerHTML = `<iframe src="${doc.nom_fitxer}" allowfullscreen style="width:100%; height:100%; border:none;"></iframe>`;
    } else {
        visor.innerHTML = `<img src="${doc.nom_fitxer}" alt="Document" style="max-width:100%; max-height:100%;">`;
    }

    document.getElementById('modal-document-actiu-titol').textContent = doc.titol || window.textosDocuments.senseTitol;
    document.getElementById('modal-document-actiu-any').textContent = doc.any_document || '';
    document.getElementById('modal-document-actiu-descripcio').textContent = doc.descripcio || '';
}
function tornaResumDocument() {
    mostraEstatResum();
}

function tancaModalDocument() {
    document.getElementById('modal-document').style.display = 'none';
}

function confirmaEliminacioGrup() {
    const grupId = document.getElementById('boto-eliminar-document').dataset.id;
    if (!confirm(window.textosDocuments.confirmEliminarGrup)) return;

    fetch(`/familia/${window.familiaId}/administrar/documents/grup/${grupId}/eliminar`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.error || window.textosDocuments.errorEliminarGrup);
        }
    });
}

const inputDocuments = document.getElementById("puja-documents");
if (inputDocuments) {
    inputDocuments.addEventListener("change", function (e) {
        const fitxers = e.target.files;
        const galeria = document.getElementById("previsualitzacio-documents");

        for (let i = 0; i < fitxers.length; i++) {
            const fitxer = fitxers[i];
            const formData = new FormData();
            formData.append("fitxer", fitxer);
            formData.append("titol", "");
            formData.append("any_document", "");
            formData.append("descripcio", "");
            if (grupPendentId) formData.append("grup_id", grupPendentId);

            fetch(`/familia/${window.familiaId}/administrar/documents/pujar`, {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    alert(data.error || window.textosDocuments.errorPujar);
                    return;
                }

                grupPendentId = data.grup_id;
                const doc = data.document;

                const bloc = document.createElement("div");
                bloc.classList.add("arxiu-amb-metadades");
                bloc.dataset.documentId = doc.id;

                const miniatura = document.createElement("div");
                miniatura.classList.add("capsa-arxiu-metadades");
                if (doc.tipus === 'pdf') {
                    miniatura.innerHTML = '<i class="fas fa-file-pdf" style="font-size:48px;color:#dc3545;"></i>';
                } else {
                    miniatura.innerHTML = `<img src="${doc.nom_fitxer}">`;
                }
                bloc.appendChild(miniatura);

                const metadades = document.createElement("div");
                metadades.classList.add("metadades-arxiu");
                metadades.innerHTML = `
                    <input type="text" class="input-titol-doc" placeholder="${window.textosDocuments.nomDocument}">
                    <input type="text" class="input-any-doc" placeholder="${window.textosDocuments.any}">
                    <textarea class="input-descripcio-doc" rows="2" placeholder="${window.textosDocuments.descripcio}"></textarea>
                `;
                bloc.appendChild(metadades);

                const botoEliminar = document.createElement("button");
                botoEliminar.type = "button";
                botoEliminar.textContent = window.textosDocuments.eliminar;
                botoEliminar.classList.add("boto-eliminar-arxiu");
                botoEliminar.addEventListener("click", () => {
                    bloc.remove();
                    fetch(`/familia/${window.familiaId}/administrar/documents/${doc.id}/eliminar`, { method: 'POST' });
                });
                bloc.appendChild(botoEliminar);

                galeria.prepend(bloc);
                document.getElementById('btn-guardar-documents').style.display = 'inline-block';
            })
            .catch(err => console.error("Error en pujar document:", err));
        }

        e.target.value = '';
    });
}

function guardarGrupDocuments() {
    if (!grupPendentId) return;

    const boto = document.getElementById('btn-guardar-documents');
    boto.disabled = true;
    boto.textContent = window.textosDocuments.guardant;

    const titol = document.getElementById('input-titol-grup').value;
    const descripcio = document.getElementById('input-descripcio-grup').value;
    const visible_public = document.getElementById('input-visible-grup').checked;

    const peticionsDocuments = [...document.querySelectorAll('.arxiu-amb-metadades')].map(bloc => {
        const docId = bloc.dataset.documentId;
        const docTitol = bloc.querySelector('.input-titol-doc').value;
        const docAny = bloc.querySelector('.input-any-doc').value;
        const docDescripcio = bloc.querySelector('.input-descripcio-doc').value;

        return fetch(`/familia/${window.familiaId}/administrar/documents/${docId}/actualitzar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titol: docTitol, any_document: docAny, descripcio: docDescripcio })
        });
    });

    Promise.all(peticionsDocuments).then(() => {
        return fetch(`/familia/${window.familiaId}/administrar/documents/grup/${grupPendentId}/actualitzar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titol, descripcio, visible_public })
        });
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}
function pantallaCompletaDocument() {
    const iframe = document.querySelector('#modal-document-actiu-visor iframe');
    const img = document.querySelector('#modal-document-actiu-visor img');
    const element = iframe || img;

    if (!element) return;

    if (element.requestFullscreen) {
        element.requestFullscreen().catch(err => console.error('Error fullscreen:', err));
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}

function obreEdicioDocument() {
    const grupId = document.getElementById('boto-editar-document').dataset.id;
    const grup = GRUPS_DOCUMENTS[grupId];
    if (!grup) return;

    tancaModalDocument();

    grupPendentId = grupId;

    document.getElementById('input-titol-grup').value = grup.titol || '';
    document.getElementById('input-descripcio-grup').value = grup.descripcio || '';
    document.getElementById('input-visible-grup').checked = grup.visible_public;

    const galeria = document.getElementById('previsualitzacio-documents');
    galeria.innerHTML = '';

    grup.documents.forEach(doc => {
        const bloc = document.createElement('div');
        bloc.classList.add('arxiu-amb-metadades');
        bloc.dataset.documentId = doc.id;

        const miniatura = document.createElement('div');
        miniatura.classList.add('capsa-arxiu-metadades');
        if (doc.tipus === 'pdf') {
            miniatura.innerHTML = '<i class="fas fa-file-pdf" style="font-size:48px;color:#dc3545;"></i>';
        } else {
            miniatura.innerHTML = `<img src="${doc.nom_fitxer}">`;
        }
        bloc.appendChild(miniatura);

        const metadades = document.createElement('div');
        metadades.classList.add('metadades-arxiu');
        metadades.innerHTML = `
            <input type="text" class="input-titol-doc" value="${doc.titol || ''}" placeholder="${window.textosDocuments.nomDocument}">
            <input type="text" class="input-any-doc" value="${doc.any_document || ''}" placeholder="${window.textosDocuments.any}">
            <textarea class="input-descripcio-doc" rows="2" placeholder="${window.textosDocuments.descripcio}">${doc.descripcio || ''}</textarea>
        `;
        bloc.appendChild(metadades);

        const botoEliminar = document.createElement('button');
        botoEliminar.type = 'button';
        botoEliminar.textContent = window.textosDocuments.eliminar;
        botoEliminar.classList.add('boto-eliminar-arxiu');
        botoEliminar.addEventListener('click', () => {
            bloc.remove();
            fetch(`/familia/${window.familiaId}/administrar/documents/${doc.id}/eliminar`, { method: 'POST' });
        });
        bloc.appendChild(botoEliminar);

        galeria.appendChild(bloc);
    });

    document.getElementById('btn-guardar-documents').style.display = 'inline-block';

    const blocPlegable = document.getElementById('puja-documents').closest('.bloc-plegable');
    if (blocPlegable) {
        blocPlegable.classList.remove('tancat');
        blocPlegable.scrollIntoView({ behavior: 'smooth' });
    }
}