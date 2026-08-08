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
                console.log('🔍 Buscant:', query);
                fetch(`/api/buscar-usuaris?q=${encodeURIComponent(query)}`)
                    .then(r => {
                        console.log('📡 Resposta rebuda:', r.status);
                        return r.json();
                    })
                    .then(usuaris => {
                        console.log('👥 Usuaris trobats:', usuaris);
                        const div = document.getElementById('resultats_usuari');
                        console.log('📦 Div resultats:', div);
                        if (usuaris.length === 0) {
                            div.innerHTML = '<div style="padding: 8px; color: #666;">No s\'han trobat usuaris</div>';
                        } else {
                            div.innerHTML = usuaris.map(u => 
                                `<div class="usuari-item" onclick="seleccionarUsuari(${u.id}, '${u.text}')" style="padding: 8px; cursor: pointer; border-bottom: 1px solid #eee;">
                                    ${u.text}
                                </div>`
                            ).join('');
                        }
                        console.log('✅ Mostrant resultats');
                        div.style.display = 'block';
                    })
                    .catch(err => console.error('❌ Error:', err));
            }, 300);
        });
        
        // Prevenir Enter al camp de buscar
        buscarInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
            }
        });
    }
    
    // Tancar resultats si es clica fora
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#buscar_usuari') && !e.target.closest('#resultats_usuari')) {
            const resultatsDiv = document.getElementById('resultats_usuari');
            if (resultatsDiv) {
                resultatsDiv.style.display = 'none';
            }
        }
    });
});

// Funcions globals
function seleccionarUsuari(id, text) {
    console.log('✨ Usuari seleccionat:', id, text);
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

// Funcions per carregar ubicacions al formulari d'editar
async function carregarRegions(suffix) {
    const paisId = document.getElementById('pais_' + suffix).value;
    const selectRegio = document.getElementById('regio_' + suffix);
    
    if (!paisId) return;
    
    selectRegio.disabled = true;
    selectRegio.innerHTML = '<option value="">Carregant...</option>';
    
    const response = await fetch(`/api/regions/${paisId}`);
    const regions = await response.json();
    
    selectRegio.innerHTML = '<option value="">-- Selecciona regió --</option>';
    regions.forEach(regio => {
        const option = document.createElement('option');
        option.value = regio.id;
        option.textContent = regio.nom;
        selectRegio.appendChild(option);
    });
    selectRegio.disabled = false;
}

async function carregarMunicipis(suffix) {
    const regioId = document.getElementById('regio_' + suffix).value;
    const inputMunicipi = document.getElementById('municipi_' + suffix);
    
    if (!regioId) return;
    
    inputMunicipi.disabled = true;
    inputMunicipi.placeholder = 'Carregant...';
    
    const response = await fetch(`/api/municipis/${regioId}`);
    const municipis = await response.json();
    
    const datalist = document.getElementById('municipis_' + suffix + '_list');
    datalist.innerHTML = '';
    
    municipis.forEach(municipi => {
        const option = document.createElement('option');
        option.value = municipi.nom;
        datalist.appendChild(option);
    });
    
    inputMunicipi.disabled = false;
    inputMunicipi.placeholder = 'Escriu o selecciona';
}

function confirmarEliminar() {
    if (confirm('Estàs segur que vols eliminar aquest membre?')) {
        window.location.href = window.URL_ELIMINAR_MEMBRE;
    }
}