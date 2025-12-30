/**
 * Sistema de càrrega en cascada d'ubicacions (Països → Regions → Municipis)
 * Per usar en formularis amb múltiples conjunts d'ubicacions
 */

// Variables globals per emmagatzemar dades
let paisosData = [];
let regionsCache = {};
let municipisCache = {};

/**
 * Inicialitza el sistema d'ubicacions
 * Crida aquesta funció quan carrega la pàgina
 */
async function inicialitzarUbicacions() {
    await carregarPaisos();
}

/**
 * Carrega tots els països disponibles i pobla els selects
 */
async function carregarPaisos() {
    try {
        const response = await fetch('/api/paisos');
        if (!response.ok) throw new Error('Error carregant països');
        
        paisosData = await response.json();
        
        // Poblar tots els selects de països que existeixin
        const selectsPaisos = ['pais_naixement', 'pais_defuncio', 'pais_actual'];
        selectsPaisos.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (!select) return;
            
            select.innerHTML = '<option value="">-- Selecciona país --</option>';
            
            paisosData.forEach(pais => {
                const option = document.createElement('option');
                option.value = pais.id;
                option.textContent = pais.nom;
                select.appendChild(option);
            });
        });
        
        console.log(`✅ ${paisosData.length} països carregats`);
    } catch (error) {
        console.error('❌ Error carregant països:', error);
        mostrarError('No s\'han pogut carregar els països');
    }
}

/**
 * Carrega les regions d'un país quan se selecciona
 * @param {string} tipus - 'naixement', 'defuncio' o 'actual'
 */
async function carregarRegions(tipus) {
    const paisSelect = document.getElementById(`pais_${tipus}`);
    const regioSelect = document.getElementById(`regio_${tipus}`);
    const municipiSelect = document.getElementById(`municipi_${tipus}`);
    
    if (!paisSelect || !regioSelect || !municipiSelect) return;
    
    const paisId = paisSelect.value;
    
    // Reset regió i municipi
    regioSelect.innerHTML = '<option value="">-- Carregant regions... --</option>';
    regioSelect.disabled = true;
    municipiSelect.innerHTML = '<option value="">-- Primer selecciona regió --</option>';
    municipiSelect.disabled = true;
    
    if (!paisId) {
        regioSelect.innerHTML = '<option value="">-- Primer selecciona país --</option>';
        return;
    }
    
    try {
        // Usar cache si ja hem carregat aquest país
        if (regionsCache[paisId]) {
            poblarRegions(regionsCache[paisId], regioSelect);
            return;
        }
        
        const response = await fetch(`/api/regions/${paisId}`);
        if (!response.ok) throw new Error('Error carregant regions');
        
        const regions = await response.json();
        regionsCache[paisId] = regions;
        
        poblarRegions(regions, regioSelect);
        
    } catch (error) {
        console.error('❌ Error carregant regions:', error);
        regioSelect.innerHTML = '<option value="">-- Error carregant regions --</option>';
        mostrarError('No s\'han pogut carregar les regions');
    }
}

/**
 * Pobla el select de regions amb les dades
 */
function poblarRegions(regions, selectElement) {
    selectElement.innerHTML = '<option value="">-- Selecciona regió --</option>';
    
    if (!regions || regions.length === 0) {
        selectElement.innerHTML = '<option value="">-- Sense regions disponibles --</option>';
        selectElement.disabled = true;
        return;
    }
    
    regions.forEach(regio => {
        const option = document.createElement('option');
        option.value = regio.id;
        option.textContent = regio.nom;
        selectElement.appendChild(option);
    });
    
    selectElement.disabled = false;
    console.log(`✅ ${regions.length} regions carregades`);
}

/**
 * Carrega els municipis d'una regió quan se selecciona
 * @param {string} tipus - 'naixement', 'defuncio' o 'actual'
 */
async function carregarMunicipis(tipus) {
    const regioSelect = document.getElementById(`regio_${tipus}`);
    const municipiSelect = document.getElementById(`municipi_${tipus}`);
    
    if (!regioSelect || !municipiSelect) return;
    
    const regioId = regioSelect.value;
    
    // Reset municipi
    municipiSelect.innerHTML = '<option value="">-- Carregant municipis... --</option>';
    municipiSelect.disabled = true;
    
    if (!regioId) {
        municipiSelect.innerHTML = '<option value="">-- Primer selecciona regió --</option>';
        return;
    }
    
    try {
        // Usar cache si ja hem carregat aquesta regió
        if (municipisCache[regioId]) {
            poblarMunicipis(municipisCache[regioId], municipiSelect);
            return;
        }
        
        const response = await fetch(`/api/municipis/${regioId}`);
        if (!response.ok) throw new Error('Error carregant municipis');
        
        const municipis = await response.json();
        municipisCache[regioId] = municipis;
        
        poblarMunicipis(municipis, municipiSelect);
        
    } catch (error) {
        console.error('❌ Error carregant municipis:', error);
        municipiSelect.innerHTML = '<option value="">-- Error carregant municipis --</option>';
        mostrarError('No s\'han pogut carregar els municipis');
    }
}

/**
 * Pobla el select de municipis amb les dades
 */
function poblarMunicipis(municipis, selectElement) {
    selectElement.innerHTML = '<option value="">-- Selecciona municipi --</option>';
    
    if (!municipis || municipis.length === 0) {
        selectElement.innerHTML = '<option value="">-- Sense municipis disponibles --</option>';
        selectElement.disabled = true;
        return;
    }
    
    municipis.forEach(municipi => {
        const option = document.createElement('option');
        option.value = municipi.id;
        option.textContent = municipi.nom;
        selectElement.appendChild(option);
    });
    
    selectElement.disabled = false;
    console.log(`✅ ${municipis.length} municipis carregats`);
}

/**
 * Mostra un missatge d'error a l'usuari
 */
function mostrarError(missatge) {
    // Pots personalitzar això amb un toast o alert més elegant
    console.error(missatge);
}

/**
 * Reinicia tots els selects d'ubicacions d'un tipus
 * @param {string} tipus - 'naixement', 'defuncio' o 'actual'
 */
function resetUbicacions(tipus) {
    const paisSelect = document.getElementById(`pais_${tipus}`);
    const regioSelect = document.getElementById(`regio_${tipus}`);
    const municipiSelect = document.getElementById(`municipi_${tipus}`);
    
    if (paisSelect) paisSelect.value = '';
    if (regioSelect) {
        regioSelect.innerHTML = '<option value="">-- Primer selecciona país --</option>';
        regioSelect.disabled = true;
    }
    if (municipiSelect) {
        municipiSelect.innerHTML = '<option value="">-- Primer selecciona regió --</option>';
        municipiSelect.disabled = true;
    }
}

// Inicialitzar quan carrega la pàgina
document.addEventListener('DOMContentLoaded', function() {
    inicialitzarUbicacions();
});