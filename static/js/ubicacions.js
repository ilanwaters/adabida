/**
 * Sistema global d'ubicacions intel·ligents
 * Detecta automàticament camps de país/regió/municipi i els omple dinàmicament
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🗺️ Sistema d\'ubicacions carregat');
    
    // Detectar tots els grups de camps d'ubicació
    const grupsUbicacio = detectarGrupsUbicacio();
    
    grupsUbicacio.forEach(grup => {
        inicialitzarGrup(grup);
    });
    
    // Preparar formularis per crear municipis automàticament
    prepararEnviamentFormulari();
});

/**
 * Obté traduccions (fallback si no estan definides)
 */
function t(clau) {
    const traduccions = {
        seleccionaPais: 'Selecciona un país',
        seleccionaRegio: 'Selecciona província/regió',
        seleccionaMunicipi: 'Selecciona o escriu el teu municipi',
        carregant: 'Carregant...',
        errorCarregant: 'Error carregant',
        seleccionaPrimerRegio: 'Selecciona primer la regió',
        seleccionaPrimerPais: 'Selecciona primer el país'
    };
    
    // Si hi ha traduccions globals del template, usar-les
    if (window.traduccions && window.traduccions[clau]) {
        return window.traduccions[clau];
    }
    
    // Sinó, usar les predefinides
    return traduccions[clau] || clau;
}

/**
 * Detecta grups de camps relacionats (país, regió, municipi)
 */
function detectarGrupsUbicacio() {
    const grups = [];
    const campsPais = document.querySelectorAll('select[name*="pais"], input[name*="pais"]');
    
    campsPais.forEach(campPais => {
        let nomRegio, nomMunicipi;
        
        // Cas especial: camps sense prefix (pais, regio, municipi)
        if (campPais.name === 'pais') {
            nomRegio = 'regio';
            nomMunicipi = 'municipi';
        } else {
            // Per camps amb prefix: pais_X → buscar regio_X i municipi_X
            const base = campPais.name.replace('pais_', '');
            nomRegio = 'regio_' + base;
            nomMunicipi = 'municipi_' + base;
        }
        
        const grup = {
            pais: campPais,
            regio: document.querySelector(`[name="${nomRegio}"]`),
            municipi: document.querySelector(`[name="${nomMunicipi}"]`)
        };
        
        if (grup.regio || grup.municipi) {
            grups.push(grup);
            console.log('✅ Grup detectat:', campPais.name, '→ regio:', nomRegio);
        }
    });
    
    return grups;
}

function extreuNomBase(nomCamp) {
    if (nomCamp.startsWith('pais_')) {
        const base = nomCamp.replace('pais_', '');
        return base + '_';
    }
    if (nomCamp === 'pais') {
        return '';  // Per camps sense prefix (pais, regio, municipi)
    }
    return '';
}

/**
 * Inicialitza un grup de camps relacionats
 */
function inicialitzarGrup(grup) {
    if (grup.pais) {
        carregarPaisos(grup.pais);
        
        grup.pais.addEventListener('change', function() {
            const paisId = this.value;
            console.log('🌍 País seleccionat ID:', paisId);
            
            // Si seleccionen "ALTRE", convertir tot a inputs lliures
            if (paisId === 'ALTRE') {
                convertirGrupATextLliure(grup);
                return;
            }
            
            if (paisId && grup.regio) {
                console.log('📍 Carregant regions per país ID:', paisId);
                carregarRegions(paisId, grup.regio);
                
                if (grup.municipi) {
                    grup.municipi.value = '';
                    grup.municipi.disabled = true;
                    grup.municipi.placeholder = t('seleccionaPrimerRegio');
                }
            } else if (!paisId && grup.regio) {
                // Quan desseleccionen el país, netejar regió
                grup.regio.innerHTML = `<option value="">${t('seleccionaPrimerPais')}</option>`;
                grup.regio.disabled = true;
            }
        });
    }
    
    if (grup.regio && grup.municipi) {
        grup.regio.addEventListener('change', function() {
            const regioId = this.value;
            console.log('🏛️ Regió seleccionada ID:', regioId);
            if (regioId) {
                carregarMunicipis(regioId, grup.municipi);
            }
        });
    }
}

/**
 * Carrega tots els països disponibles
 */
async function carregarPaisos(selectPais) {
    try {
        console.log('🔄 Carregant països...');
        const response = await fetch('/api/paisos');
        const paisos = await response.json();
        
        selectPais.innerHTML = `<option value="">${t('seleccionaPais')}</option>`;
        
        paisos.forEach(pais => {
            const option = document.createElement('option');
            option.value = pais.id;
            option.textContent = pais.nom;
            selectPais.appendChild(option);
        });
        
        // Opció per escriure país nou
        const optionNou = document.createElement('option');
        optionNou.value = 'ALTRE';
        optionNou.textContent = 'Altre país...';
        selectPais.appendChild(optionNou);

        selectPais.disabled = false; 
        
        console.log(`✅ ${paisos.length} països carregats`);
    } catch (error) {
        console.error('❌ Error carregant països:', error);
    }
}

/**
 * Carrega regions/províncies d'un país
 */
async function carregarRegions(paisId, selectRegio) {
    console.log('🔄 Iniciant càrrega de regions per país:', paisId);
    selectRegio.disabled = true;
    selectRegio.innerHTML = `<option value="">${t('carregant')}</option>`;
    
    try {
        const url = `/api/regions/${paisId}`;
        console.log('📡 Fent petició a:', url);
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const regions = await response.json();
        console.log('📦 Regions rebudes:', regions.length);
        
        selectRegio.innerHTML = `<option value="">${t('seleccionaRegio')}</option>`;
        
        regions.forEach(regio => {
            const option = document.createElement('option');
            option.value = regio.id;
            option.textContent = regio.nom;
            selectRegio.appendChild(option);
        });
        
        selectRegio.disabled = false;
        console.log(`✅ ${regions.length} regions carregades i select habilitat`);
    } catch (error) {
        console.error('❌ Error carregant regions:', error);
        selectRegio.innerHTML = `<option value="">${t('errorCarregant')}</option>`;
        selectRegio.disabled = false; // Habilitar fins i tot si hi ha error
    }
}

/**
 * Carrega municipis amb autocomplete editable
 */
async function carregarMunicipis(regioId, campMunicipi) {
    console.log('🔄 Carregant municipis per regió:', regioId);
    
    // Convertir el select en un input amb datalist si cal
    if (campMunicipi.tagName === 'SELECT') {
        campMunicipi = convertirAInputAmbDatalist(campMunicipi);
    }
    
    campMunicipi.disabled = true;
    campMunicipi.placeholder = t('carregant');
    
    try {
        const response = await fetch(`/api/municipis/${regioId}`);
        const municipis = await response.json();
        
        // Crear o actualitzar el datalist
        let datalist = document.getElementById(`datalist-${campMunicipi.id}`);
        if (!datalist) {
            datalist = document.createElement('datalist');
            datalist.id = `datalist-${campMunicipi.id}`;
            campMunicipi.setAttribute('list', datalist.id);
            campMunicipi.parentElement.appendChild(datalist);
        }
        
        datalist.innerHTML = '';
        municipis.forEach(municipi => {
            const option = document.createElement('option');
            option.value = municipi.nom;
            datalist.appendChild(option);
        });
        
        campMunicipi.disabled = false;
        campMunicipi.placeholder = t('seleccionaMunicipi');
        campMunicipi.dataset.regioId = regioId;
        
        console.log(`✅ ${municipis.length} municipis amb autocomplete`);
        
    } catch (error) {
        console.error('❌ Error carregant municipis:', error);
        campMunicipi.placeholder = t('errorCarregant');
    }
}

/**
 * Converteix un select en input amb datalist
 */
function convertirAInputAmbDatalist(selectElement) {
    const input = document.createElement('input');
    input.type = 'text';
    input.id = selectElement.id;
    input.name = selectElement.name;
    input.className = selectElement.className;
    input.placeholder = t('seleccionaMunicipi');
    
    selectElement.parentElement.replaceChild(input, selectElement);
    return input;
}

/**
 * Prepara els formularis per crear municipis automàticament
 */
function prepararEnviamentFormulari() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            const inputsMunicipi = form.querySelectorAll('input[name*="municipi"]');
            
            for (const input of inputsMunicipi) {
                const nomMunicipi = input.value.trim();
                const regioId = input.dataset.regioId;
                
                if (nomMunicipi && regioId) {
                    await assegurarMunicipiExisteix(regioId, nomMunicipi);
                }
            }
        });
    });
}

/**
 * Crea el municipi si no existeix
 */
async function assegurarMunicipiExisteix(regioId, nomMunicipi) {
    try {
        await fetch('/api/afegir-municipi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                regio_id: regioId,
                nom: nomMunicipi
            })
        });
    } catch (error) {
        console.error('Error creant municipi:', error);
    }
}

/**
 * Converteix un grup complet a inputs de text lliure
 */
function convertirGrupATextLliure(grup) {
    console.log('🌍 Convertint a text lliure per país nou');
    
    // Convertir país
    if (grup.pais && grup.pais.tagName === 'SELECT') {
        const inputPais = document.createElement('input');
        inputPais.type = 'text';
        inputPais.id = grup.pais.id;
        inputPais.name = grup.pais.name;
        inputPais.className = grup.pais.className;
        inputPais.placeholder = 'Escriu el nom del teu país';
        inputPais.required = grup.pais.required;
        grup.pais.parentElement.replaceChild(inputPais, grup.pais);
        grup.pais = inputPais;
    }
    
    // Convertir regió
    if (grup.regio && grup.regio.tagName === 'SELECT') {
        const inputRegio = document.createElement('input');
        inputRegio.type = 'text';
        inputRegio.id = grup.regio.id;
        inputRegio.name = grup.regio.name;
        inputRegio.className = grup.regio.className;
        inputRegio.placeholder = 'Escriu regió/província/estat';
        inputRegio.disabled = false;
        grup.regio.parentElement.replaceChild(inputRegio, grup.regio);
        grup.regio = inputRegio;
    }
    
    // Convertir municipi
    if (grup.municipi && grup.municipi.tagName === 'SELECT') {
        const inputMunicipi = document.createElement('input');
        inputMunicipi.type = 'text';
        inputMunicipi.id = grup.municipi.id;
        inputMunicipi.name = grup.municipi.name;
        inputMunicipi.className = grup.municipi.className;
        inputMunicipi.placeholder = 'Escriu el teu municipi/ciutat';
        inputMunicipi.disabled = false;
        grup.municipi.parentElement.replaceChild(inputMunicipi, grup.municipi);
        grup.municipi = inputMunicipi;
    }
    
    // Focus al primer camp
    if (grup.pais) {
        grup.pais.focus();
    }
}