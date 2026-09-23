document.addEventListener('DOMContentLoaded', function() {
    // Buscar usuaris per vincular
    let timeoutBuscar;
    const buscarInput = document.getElementById('buscar_usuari');
    
    if (buscarInput) {
        buscarInput.addEventListener('input', function(e) {
            clearTimeout(timeoutBuscar);
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                document.getElementById('resultats_usuari').style.display = 'none';
                return;
            }
            
            timeoutBuscar = setTimeout(() => {
                fetch(`/api/buscar-usuaris?q=${encodeURIComponent(query)}`)
                    .then(r => r.json())
                    .then(usuaris => {
                        const div = document.getElementById('resultats_usuari');
                        div.innerHTML = '';
                        
                        if (usuaris.length === 0) {
                            div.innerHTML = '<div style="padding: 8px; color: #666;">No s\'han trobat usuaris</div>';
                        } else {
                            usuaris.forEach(u => {
                                const item = document.createElement('div');
                                item.style.cssText = 'padding: 8px; cursor: pointer; border-bottom: 1px solid #eee;';
                                item.textContent = u.text;
                                item.onclick = () => seleccionarUsuari(u.id, u.text);
                                div.appendChild(item);
                            });
                        }
                        
                        div.style.display = 'block';
                    })
                    .catch(err => console.error('Error:', err));
            }, 300);
        });
        
        buscarInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') e.preventDefault();
        });
    }
    
    // Tancar resultats si es clica fora
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#buscar_usuari') && !e.target.closest('#resultats_usuari')) {
            const resultatsDiv = document.getElementById('resultats_usuari');
            if (resultatsDiv) resultatsDiv.style.display = 'none';
        }
        
        if (!e.target.closest('#buscar_membre') && !e.target.closest('#resultats_membre')) {
            const resultatsMembre = document.getElementById('resultats_membre');
            if (resultatsMembre) resultatsMembre.style.display = 'none';
        }
    });
    
    // BUSCAR MEMBRE EXISTENT
    inicialitzarBuscarMembre();
});

function seleccionarUsuari(id, text) {
    document.getElementById('usuari_id').value = id;
    document.getElementById('usuari_nom').textContent = text;
    document.getElementById('usuari_seleccionat').style.display = 'block';
    document.getElementById('buscar_usuari').value = '';
    document.getElementById('resultats_usuari').style.display = 'none';
}

function netejarUsuari() {
    document.getElementById('usuari_id').value = '';
    document.getElementById('usuari_seleccionat').style.display = 'none';
}

function inicialitzarBuscarMembre() {
    const inputBuscarMembre = document.getElementById('buscar_membre');
    if (!inputBuscarMembre || !window.totsMembres) return;
    
    inputBuscarMembre.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const resultatsMembre = document.getElementById('resultats_membre');
        
        if (query.length < 2) {
            resultatsMembre.style.display = 'none';
            return;
        }
        
        const filtrats = window.totsMembres.filter(m => 
            (m.nom + ' ' + m.primer_cognom).toLowerCase().includes(query)
        );
        
        if (filtrats.length === 0) {
            resultatsMembre.style.display = 'none';
            return;
        }
        
        resultatsMembre.innerHTML = filtrats.map(m => `
            <div onclick="seleccionarMembre(${m.id}, '${m.nom} ${m.primer_cognom}')" 
                 style="padding: 8px; cursor: pointer; border-bottom: 1px solid #eee;">
                ${m.nom} ${m.primer_cognom} 
                ${m.data_naixement ? '(' + m.data_naixement.split('-')[0] + ')' : ''}
            </div>
        `).join('');
        
        resultatsMembre.style.display = 'block';
    });
}

function seleccionarMembre(id, nom) {
    document.getElementById('membre_existent_id').value = id;
    document.getElementById('membre_nom').textContent = nom;
    document.getElementById('membre_seleccionat').style.display = 'block';
    document.getElementById('resultats_membre').style.display = 'none';
    document.getElementById('buscar_membre').value = '';
}

function netejarMembre() {
    document.getElementById('membre_existent_id').value = '';
    document.getElementById('membre_seleccionat').style.display = 'none';
}

function afegirDocument() {
    const container = document.getElementById('documents-container');
    const nouDocument = document.createElement('div');
    nouDocument.className = 'document-item';
    nouDocument.style.cssText = 'border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9; position: relative;';
    
    nouDocument.innerHTML = `
        <button type="button" onclick="this.closest('.document-item').remove()" 
                style="position: absolute; top: 10px; right: 10px; background-color: #ffecec; color: #b30000; border: 1px solid #b30000; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 0.85em;">
            Eliminar
        </button>
        <div class="fila-formulari">
            <div>
                <label>Tipus de document</label>
                <select name="tipus_document[]" style="width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 6px;">
                    <option value="">-- Selecciona --</option>
                    <option value="dni">DNI/Passaport</option>
                    <option value="partida_naixement">Partida de Naixement</option>
                    <option value="partida_defuncio">Partida de Defunció</option>
                    <option value="certificat">Certificat</option>
                    <option value="fotografia">Fotografia</option>
                    <option value="altre">Altre Document</option>
                </select>
            </div>
            <div>
                <label>Fitxer</label>
                <input type="file" name="document[]" accept=".pdf,.jpg,.jpeg,.png,.gif" 
                       style="width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 6px;">
            </div>
            <div>
                <label>Visibilitat</label>
                <select name="visibilitat_document[]" style="width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 6px;">
                    <option value="familia">Visible per tota la família</option>
                    <option value="admin">Només administradors</option>
                </select>
            </div>
        </div>
        <div style="margin-top: 10px;">
            <label>Descripció del document (opcional)</label>
            <input type="text" name="descripcio_document[]" placeholder="Ex: DNI renovat el 2020"
                   style="width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 6px;">
        </div>
    `;
    
    container.appendChild(nouDocument);
}

function seleccionarMembre(id, nom) {
    document.getElementById('membre_existent_id').value = id;
    document.getElementById('membre_nom').textContent = nom;
    document.getElementById('membre_seleccionat').style.display = 'block';
    document.getElementById('resultats_membre').style.display = 'none';
    document.getElementById('buscar_membre').value = '';
    
    // AMAGAR FORMULARI I DESACTIVAR VALIDACIÓ
    const formulari = document.getElementById('formulari-nou-membre');
    formulari.style.display = 'none';
    
    // Desactivar required dels camps amagats
    formulari.querySelectorAll('[required]').forEach(input => {
        input.removeAttribute('required');
        input.dataset.wasRequired = 'true';
    });
}

function netejarMembre() {
    document.getElementById('membre_existent_id').value = '';
    document.getElementById('membre_seleccionat').style.display = 'none';
    
    // MOSTRAR FORMULARI I REACTIVAR VALIDACIÓ
    const formulari = document.getElementById('formulari-nou-membre');
    formulari.style.display = 'block';
    
    // Reactivar required
    formulari.querySelectorAll('[data-was-required]').forEach(input => {
        input.setAttribute('required', '');
        delete input.dataset.wasRequired;
    });
}

