// static/js/inici.js - Funcionalitat pàgina d'inici (VERSIÓ NETA)

// ============================================================================
// INICIALITZACIÓ
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    inicialitzarPagina();
});

function inicialitzarPagina() {
    // Login i errors
    inicialitzaLogin();
    gestionaErrorsLogin();
    inicialitzaDisclaimer();
    
    // Barra lateral
    carregarCategories();
    carregarPaisosBarraLateral();
    
    // Selector país i temes
    inicialitzarSelectorPais();
    inicialitzarSelectorCategoria();
    // Entrades
    inicialitzarEntrades();
    
    // Hash navigation
    gestionarHashNavegacio();
}

// ============================================================================
// LOGIN I AUTENTICACIÓ
// ============================================================================

function inicialitzaLogin() {
    const botoLogin = document.getElementById('login-toggle-principal');
    const submenu = document.getElementById('submenu-login');
    const botoLoginModal = document.getElementById('btn-login-modal');

    // Toggle login dropdown
    if (botoLogin && submenu) {
        botoLogin.addEventListener('click', function(e) {
            e.preventDefault();
            const isVisible = submenu.style.display === "block";
            submenu.style.display = isVisible ? "none" : "block";
        });
    }

    // Login des de modal
    if (botoLoginModal) {
        botoLoginModal.addEventListener('click', function(e) {
            e.preventDefault();
            tancarModalMotivadora();
            setTimeout(() => {
                if (submenu) submenu.style.display = 'block';
            }, 100);
        });
    }

    // Tancar si es clica fora
    document.addEventListener('click', function(e) {
        if (submenu && 
            !submenu.contains(e.target) && 
            e.target !== botoLogin) {
            submenu.style.display = "none";
        }
    });

    // Toggle visibilitat contrasenya
    const btnToggle = document.getElementById('toggle-visibilitat');
    const inputContra = document.getElementById('contrasenya');
    if (btnToggle && inputContra) {
        btnToggle.addEventListener('click', function() {
            const tipus = inputContra.getAttribute('type');
            inputContra.setAttribute('type', tipus === 'password' ? 'text' : 'password');
        });
    }
}

function gestionaErrorsLogin() {
    const errorDiv = document.getElementById('missatge-error-login');
    if (errorDiv && errorDiv.textContent.trim() !== "") {
        errorDiv.style.display = "block";
        setTimeout(() => errorDiv.style.display = "none", 4000);
    }
}

function inicialitzaDisclaimer() {
    window.mostraDisclaimer = function() {
        const modal = document.getElementById("disclaimer-modal");
        if (modal) {
            modal.style.display = "flex";
            document.body.style.overflow = "hidden";
        }
    };

    window.acceptarDisclaimer = function() {
        window.location.href = "/registre_individual";
    };
}

// ============================================================================
// MODALS
// ============================================================================

function mostrarMissatgeMotivador() {
    const modal = document.getElementById('modal-motivadora');
    if (modal) {
        modal.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }
}

function tancarModalMotivadora() {
    const modal = document.getElementById('modal-motivadora');
    if (modal) {
        modal.classList.remove('visible');
        document.body.style.overflow = 'auto';
    }
}

// Tancar modal si es clica fora
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modal-motivadora');
    if (modal && e.target === modal) {
        tancarModalMotivadora();
    }
});

// ============================================================================
// SUBMENÚS NAVEGACIÓ
// ============================================================================

function toggleSubmenu(event, submenuId) {
    event.preventDefault();
    const submenu = document.getElementById(submenuId);
    const toggle = event.currentTarget;
    
    if (submenu.classList.contains('visible')) {
        submenu.classList.remove('visible');
        toggle.classList.remove('obert');
    } else {
        // Tancar tots els altres
        document.querySelectorAll('.submenu').forEach(s => s.classList.remove('visible'));
        document.querySelectorAll('.menu-toggle').forEach(t => t.classList.remove('obert'));
        
        // Obrir aquest
        submenu.classList.add('visible');
        toggle.classList.add('obert');
    }
}

// ============================================================================
// BARRA LATERAL (TEMES/PAÏSOS)
// ============================================================================

let paisSeleccionat = null;

function canviarMode(mode) {
    document.getElementById('btn-tema').classList.toggle('active', mode === 'tema');
    document.getElementById('btn-pais').classList.toggle('active', mode === 'pais');
    
    document.getElementById('mode-tema').classList.toggle('active', mode === 'tema');
    document.getElementById('mode-pais').classList.toggle('active', mode === 'pais');
    document.getElementById('mode-pais-temes').classList.remove('active');
}

async function carregarCategories() {
    try {
        const res = await fetch('/api/barra-lateral/categories');
        const categories = await res.json();
        
        const html = categories.map(cat => `
            <div class="item-categoria" onclick="filtrarPerCategoria(${cat.id}, '${cat.nom}')">
                <span class="icona">${cat.icona}</span>
                <span>${cat.nom}</span>
            </div>
        `).join('');
        
        document.getElementById('llista-categories').innerHTML = html;
    } catch (error) {
        console.error('Error carregant categories:', error);
    }
}

async function carregarPaisosBarraLateral() {
    try {
        const res = await fetch('/api/barra-lateral/paisos');
        const paisos = await res.json();
        
        const html = paisos.map(pais => `
            <div class="item-pais" onclick="mostrarTemesPais('${pais.codi}', '${pais.nom}')">
                ${pais.nom}
            </div>
        `).join('');
        
        document.getElementById('llista-paisos').innerHTML = html;
    } catch (error) {
        console.error('Error carregant països:', error);
    }
}

async function mostrarTemesPais(codi, nom) {
    paisSeleccionat = { codi, nom };
    
    try {
        const res = await fetch(`/api/temes-pais/${codi}`);
        const data = await res.json();
        
        const temes = [...data.temes_globals, ...data.temes_pais];
        
        const html = temes.map(tema => `
            <div class="item-tema" onclick="filtrarPerTema('${tema.nom}')">
                ${tema.nom}
            </div>
        `).join('');
        
        document.getElementById('nom-pais-seleccionat').textContent = nom;
        document.getElementById('llista-temes-pais').innerHTML = html;
        
        document.getElementById('mode-pais').classList.remove('active');
        document.getElementById('mode-pais-temes').classList.add('active');
    } catch (error) {
        console.error('Error carregant temes:', error);
    }
}

function tornarPaisos() {
    paisSeleccionat = null;
    document.getElementById('mode-pais-temes').classList.remove('active');
    document.getElementById('mode-pais').classList.add('active');
}

async function filtrarPerCategoria(id, nom) {
    try {
        const res = await fetch(`/api/temes-categoria/${id}`);
        const data = await res.json();
        
        const html = data.temes.map(tema => `
            <div class="item-tema" onclick="filtrarPerTema('${tema.nom}')">
                ${tema.nom}
            </div>
        `).join('');
        
        document.getElementById('nom-categoria-seleccionada').textContent = nom;
        document.getElementById('llista-temes-categoria').innerHTML = html;
        
        document.getElementById('mode-tema').classList.remove('active');
        document.getElementById('mode-categoria-temes').classList.add('active');
    } catch (error) {
        console.error('Error carregant temes:', error);
    }
}

function tornarCategories() {
    document.getElementById('mode-categoria-temes').classList.remove('active');
    document.getElementById('mode-tema').classList.add('active');
}

window.tornarCategories = tornarCategories;

function filtrarPerTema(nom) {
    window.location.href = `/repositori?tema=${encodeURIComponent(nom)}`;
}

// ============================================================================
// SELECTOR PAÍS I TEMES
// ============================================================================

function inicialitzarSelectorPais() {
    const paisManual = document.getElementById('pais-manual');
    if (paisManual) {
        paisManual.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') guardarPaisNou();
        });
    }
    
    // Carregar selector i temes inicials
    setTimeout(() => {
        carregarPaisosSelector();
        carregarTemesPais('GLOBAL');
    }, 100);
}

function canviarPais() {
    const selector = document.getElementById('selector-pais');
    const selectorCategoria = document.getElementById('selector-categoria');
    const paisSeleccionat = selector.value;
    
    if (paisSeleccionat === 'AFEGIR_NOU') {
        mostrarModalAfegirPais();
    } else if (paisSeleccionat) {
        // Buidar selector categoria
        selectorCategoria.value = '';
        carregarTemesPais(paisSeleccionat);
    }
}

function mostrarModalAfegirPais() {
    const modal = document.getElementById('modal-afegir-pais');
    const input = document.getElementById('input-nom-pais');
    
    modal.style.display = 'flex';
    input.value = '';
    setTimeout(() => input.focus(), 100);
}
function tancarModalPais() {
    const modal = document.getElementById('modal-afegir-pais');
    const selector = document.getElementById('selector-pais');
    
    modal.style.display = 'none';
    selector.value = 'GLOBAL';
    carregarTemesPais('GLOBAL');
}

async function confirmarPaisNou() {
    const input = document.getElementById('input-nom-pais');
    const nom = input.value.trim();
    const T = window.TRADUCCIONS;
    
    if (!nom) {
        alert(T.escriuNomPais);
        input.focus();
        return;
    }
    
    try {
        const response = await fetch('/api/pais/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nom })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('modal-afegir-pais').style.display = 'none';
            await carregarPaisosSelector();
            document.getElementById('selector-pais').value = data.codi;
            carregarTemesPais(data.codi);
        } else {
            alert(data.error || T.errorCreantPais);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(T.errorConnexio);
    }
}

function guardarPaisNou() {
    const selector = document.getElementById('selector-pais');
    const paisManual = document.getElementById('pais-manual-input');
    const paisManualContainer = document.getElementById('pais-manual-container');
    const nomPais = paisManual.value.trim();
    
    if (!nomPais) {
        alert('Escriu el nom del país');
        paisManual.focus();
        return;
    }
    
    fetch('/api/pais/crear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nom: nomPais })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const novaOpcio = document.createElement('option');
            novaOpcio.value = data.codi;
            novaOpcio.text = data.nom;
            novaOpcio.selected = true;
            
            const opcioManual = selector.querySelector('option[value="manual"]');
            selector.insertBefore(novaOpcio, opcioManual);
            
            paisManualContainer.style.display = 'none';
            carregarTemesPais(data.codi);
            
            alert(`País "${data.nom}" creat correctament!`);
        } else {
            if (data.similar) {
                const confirmacio = confirm(`${data.error}\n\nVols seleccionar "${data.suggestion}"?`);
                if (confirmacio) {
                    for (let option of selector.options) {
                        if (option.text === data.suggestion) {
                            option.selected = true;
                            paisManualContainer.style.display = 'none';
                            carregarTemesPais(option.value);
                            return;
                        }
                    }
                }
            } else {
                alert('Error: ' + data.error);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al crear el país');
    });
}

function cancelarPaisManual() {
    const selector = document.getElementById('selector-pais');
    const paisManualContainer = document.getElementById('pais-manual-container');
    
    selector.value = 'GLOBAL'
    paisManualContainer.style.display = 'none';
}

async function carregarPaisosSelector() {
    try {
        const response = await fetch('/api/paisos');
        const data = await response.json();
        const selector = document.getElementById('selector-pais');
        const seleccioActual = selector.value;
        const T = window.TRADUCCIONS;
        
        selector.innerHTML = '';
        
        // Opció buida
        const opcioBuida = document.createElement('option');
        opcioBuida.value = '';
        opcioBuida.text = T.selecciona;
        selector.appendChild(opcioBuida);
        
        // GLOBAL
        const opcioGlobal = document.createElement('option');
        opcioGlobal.value = 'GLOBAL';
        opcioGlobal.text = T.temesGlobals;
        selector.appendChild(opcioGlobal);
        
        // Països
        data.forEach(pais => {
            const option = document.createElement('option');
            option.value = pais.codi_iso;
            option.text = pais.nom;
            selector.appendChild(option);
        });
        
        // Afegir nou
        const opcioAfegir = document.createElement('option');
        opcioAfegir.value = 'AFEGIR_NOU';
        opcioAfegir.text = T.afegirPais;
        opcioAfegir.style.fontStyle = 'italic';
        opcioAfegir.style.color = '#999';
        selector.appendChild(opcioAfegir);
        
        // Restaurar selecció
        if (seleccioActual && seleccioActual !== 'AFEGIR_NOU') {
            selector.value = seleccioActual;
        } else {
            selector.value = 'GLOBAL';
        }
        
    } catch (error) {
        console.error('Error carregant països:', error);
    }
}

async function carregarTemesPais(paisCodi) {
    try {
        const response = await fetch(`/api/temes-pais/${paisCodi}`);
        const data = await response.json();
        
        const totsTemes = [
            ...(data.temes_globals || []),
            ...(data.temes_pais || [])
        ];
        
        actualitzarGridTemes(totsTemes);
    } catch (error) {
        console.error('Error carregant temes:', error);
    }
}

function actualitzarGridTemes(temes) {
    const gridTemes = document.getElementById('grid-temes');
    if (!gridTemes) return;
    
    const usuariLogejat = window.USUARI_LOGEJAT || false;
    const T = window.TRADUCCIONS;
    gridTemes.innerHTML = '';
    
    if (temes.length === 0) {
        const missatge = document.createElement('p');
        missatge.style.fontStyle = 'italic';
        missatge.style.color = '#999';
        missatge.style.marginBottom = '20px';
        missatge.textContent = T.senseTemesPais;
        gridTemes.appendChild(missatge);
        gridTemes.appendChild(crearBotoAltreTema(usuariLogejat));
        return;
    }
    
    const temesVisibles = temes.slice(0, 9);
    const temesOcults = temes.slice(9);
    
    temesVisibles.forEach(tema => {
        gridTemes.appendChild(crearBotoTema(tema.nom, usuariLogejat));
    });
    
    if (temesOcults.length > 0) {
        const botoMes = document.createElement('button');
        botoMes.className = 'boto-tema boto-mes';
        botoMes.id = 'boto-mes-inicial';
        botoMes.textContent = T.mes;
        botoMes.onclick = () => toggleTemesAddicionals();
        gridTemes.appendChild(botoMes);
        
        const containerAddicionals = document.createElement('div');
        containerAddicionals.className = 'temes-addicionals';
        containerAddicionals.id = 'temes-addicionals';
        
        temesOcults.forEach(tema => {
            containerAddicionals.appendChild(crearBotoTema(tema.nom, usuariLogejat));
        });
        
        const botoMenys = document.createElement('button');
        botoMenys.className = 'boto-tema boto-mes';
        botoMenys.textContent = T.menys;
        botoMenys.onclick = () => toggleTemesAddicionals();
        containerAddicionals.appendChild(botoMenys);
        
        gridTemes.appendChild(containerAddicionals);
    }
    
    gridTemes.appendChild(crearBotoAltreTema(usuariLogejat));
}


function crearBotoTema(nomTema, usuariLogejat) {
    if (usuariLogejat) {
        const a = document.createElement('a');
        a.href = `/nova_entrada_personal?titol=${encodeURIComponent(nomTema)}`;
        a.className = 'boto-tema';
        a.textContent = nomTema;
        return a;
    } else {
        const button = document.createElement('button');
        button.className = 'boto-tema';
        button.textContent = nomTema;
        button.onclick = () => mostrarMissatgeMotivador();
        return button;
    }
}

function crearBotoAltreTema(usuariLogejat) {
    const T = window.TRADUCCIONS;
    const button = document.createElement('button');
    button.className = 'boto-tema boto-altre-tema';
    button.textContent = T.nousTemes;
    
    if (usuariLogejat) {
        button.onclick = () => mostrarModalNouTema();
    } else {
        button.onclick = () => mostrarMissatgeMotivador();
    }
    
    return button;
}

function toggleTemesAddicionals() {
    const temesAddicionals = document.getElementById('temes-addicionals');
    const botoMesInicial = document.getElementById('boto-mes-inicial');
    
    if (temesAddicionals && botoMesInicial) {
        if (temesAddicionals.classList.contains('visible')) {
            temesAddicionals.classList.remove('visible');
            botoMesInicial.style.display = 'block';
        } else {
            temesAddicionals.classList.add('visible');
            botoMesInicial.style.display = 'none';
        }
    }
}

// ============================================================================
// ENTRADES (ÚLTIMS TESTIMONIS)
// ============================================================================

function inicialitzarEntrades() {
    const botoVeureMes = document.getElementById('btn-veure-mes-entrades');
    const botoRefresh = document.getElementById('btn-refresh-entrades');
    
    if (botoVeureMes) {
        botoVeureMes.addEventListener('click', function() {
            const addicionals = document.getElementById('entrades-addicionals');
            const traduccions = window.TRADUCCIONS || {};
            
            if (addicionals.style.display === 'none') {
                addicionals.style.display = 'grid';
                this.innerHTML = `${traduccions.veureMenys || 'Veure menys'} ▲`;
            } else {
                addicionals.style.display = 'none';
                this.innerHTML = `${traduccions.veureMes || 'Veure més'} ▼`;
            }
        });
    }
    
    if (botoRefresh) {
        botoRefresh.addEventListener('click', async function() {
            this.classList.add('loading');
            this.disabled = true;
            
            try {
                const response = await fetch('/api/entrades-aleatories?limit=10');
                const data = await response.json();
                
                if (data.entrades && data.entrades.length > 0) {
                    location.reload();
                } else {
                    alert(window.TRADUCCIONS?.errorCarregarEntrades || 'Error');
                }
            } catch (error) {
                console.error('Error:', error);
                alert(window.TRADUCCIONS?.errorGeneric || 'Error');
            } finally {
                this.classList.remove('loading');
                this.disabled = false;
            }
        });
    }
}

// ============================================================================
// HASH NAVIGATION
// ============================================================================

function gestionarHashNavegacio() {
    const hash = window.location.hash;
    if (hash === "#galeria-exposicions") {
        if (typeof obreSeccio === "function") {
            obreSeccio("galeria");
        }
        setTimeout(() => {
            const boto = document.querySelector('[data-subpestanya="exposicions"]');
            if (boto) boto.click();
        }, 300);
    }
}

// ============================================================================
// MODAL NOU TEMA - AFEGIR a inici.js
// ============================================================================

function mostrarModalNouTema() {
    const modal = document.getElementById('modal-nou-tema');
    if (!modal) {
        console.error('Modal nou tema no trobat');
        return;
    }
    
    // Carregar categories disponibles
    carregarCategoriesModal();
    
    // Mostrar modal
    modal.classList.add('visible');
    document.body.style.overflow = 'hidden';
    
    // Focus al camp nom
    setTimeout(() => {
        document.getElementById('nom-tema-nou')?.focus();
    }, 100);
}

function tancarModalNouTema() {
    const modal = document.getElementById('modal-nou-tema');
    if (modal) {
        modal.classList.remove('visible');
        document.body.style.overflow = 'auto';
        
        // Netejar formulari
        document.getElementById('form-nou-tema').reset();
        document.getElementById('container-nova-categoria').style.display = 'none';
    }
}


async function carregarCategoriesModal() {
    try {
        const response = await fetch(`/api/barra-lateral/categories`);
        const data = await response.json();
        const container = document.getElementById('llista-categories-checkboxes');
        const T = window.TRADUCCIONS;
        
        if (!container) return;
        
        container.innerHTML = '';
        
        if (data && data.length > 0) {
            data.forEach(cat => {
                const label = document.createElement('label');
                label.className = 'checkbox';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = cat.id;
                checkbox.name = 'categories';
                
                const checkmark = document.createElement('span');
                checkmark.className = 'checkmark';
                
                label.appendChild(checkbox);
                label.appendChild(checkmark);
                label.appendChild(document.createTextNode(' ' + cat.nom));
                
                container.appendChild(label);
            });
        } else {
            container.innerHTML = `<p style="color: #999;">${T.senseCategoriesDisponibles}</p>`;
        }
        
    } catch (error) {
        console.error('Error carregant categories:', error);
    }
}
async function guardarNouTema() {
    const nomTema = document.getElementById('nom-tema-nou').value.trim();
    const nomCategoriaNova = document.getElementById('nom-categoria-nova').value.trim();
    const paisSeleccionat = document.getElementById('selector-pais')?.value || 'ES';
    const checkboxes = document.querySelectorAll('#llista-categories-checkboxes input[type="checkbox"]:checked');
    const categoriesIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
    const T = window.TRADUCCIONS;
    
    // Validació
    if (!nomTema) {
        alert(T.nomTemaObligatori);
        return;
    }
    
    if (categoriesIds.length === 0 && !nomCategoriaNova) {
        alert(T.triaCategoriaObligatoria);
        return;
    }
    
    const botoSubmit = document.querySelector('#form-nou-tema button[type="submit"]');
    const textOriginal = botoSubmit.textContent;
    botoSubmit.disabled = true;
    botoSubmit.textContent = T.guardant;
    
    try {
        let categoriesFinals = [...categoriesIds];
        
        // Crear categoria nova si hi ha nom
        if (nomCategoriaNova) {
            const responseCategoria = await fetch('/api/categoria/crear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nom: nomCategoriaNova,
                    pais_codi: paisSeleccionat
                })
            });
            
            const dataCategoria = await responseCategoria.json();
            
            if (!dataCategoria.success) {
                alert(T.errorCreantCategoria + ' ' + (dataCategoria.error || T.errorDesconegut));
                return;
            }
            
            categoriesFinals.push(dataCategoria.id);
        }
        
        // Crear tema amb múltiples categories
        const responseTema = await fetch('/api/tema/crear-multiple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nom: nomTema,
                categories: categoriesFinals
            })
        });
        
        const dataTema = await responseTema.json();
        
        if (dataTema.success) {
            tancarModalNouTema();
            window.location.href = `/nova_entrada_personal?titol=${encodeURIComponent(nomTema)}`;
        } else {
            alert(T.errorCreantTema + ' ' + (dataTema.error || T.errorDesconegut));
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert(T.errorConnexioTornar);
    } finally {
        botoSubmit.disabled = false;
        botoSubmit.textContent = textOriginal;
    }
}

// inici.js - afegir després de inicialitzarSelectorPais()

function inicialitzarSelectorCategoria() {
    carregarCategoriesSelector();
}

async function carregarCategoriesSelector() {
    try {
        const res = await fetch('/api/barra-lateral/categories');
        const categories = await res.json();
        const selector = document.getElementById('selector-categoria');
        const T = window.TRADUCCIONS;
        
        selector.innerHTML = `<option value="">${T.selecciona}</option>`;
        
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.text = cat.nom;
            selector.appendChild(option);
        });
    } catch (error) {
        console.error('Error carregant categories:', error);
    }
}
function canviarCategoria() {
    const selectorCategoria = document.getElementById('selector-categoria');
    const selectorPais = document.getElementById('selector-pais');
    const categoriaId = selectorCategoria.value;
    
    if (categoriaId) {
        // Buidar selector país
        selectorPais.value = '';
        carregarTemesCategoria(categoriaId);
    }
}

async function carregarTemesCategoria(categoriaId) {
    try {
        const res = await fetch(`/api/temes-categoria/${categoriaId}`);
        const data = await res.json();
        
        actualitzarGridTemes(data.temes);
    } catch (error) {
        console.error('Error carregant temes:', error);
    }
}
function toggleNovaCategoriaInput() {
    const check = document.getElementById('check-nova-categoria');
    const container = document.getElementById('container-nova-categoria');
    const input = document.getElementById('nom-categoria-nova');
    
    if (check && check.checked) {
        container.style.display = 'block';
        input.required = true;
        setTimeout(() => input.focus(), 100);
    } else {
        container.style.display = 'none';
        input.required = false;
        input.value = '';
    }
}
// Funcions globals
window.mostrarModalNouTema = mostrarModalNouTema;
window.tancarModalNouTema = tancarModalNouTema;
window.toggleNovaCategoriaInput = toggleNovaCategoriaInput;
window.guardarNouTema = guardarNouTema;
// ============================================================================
// FUNCIONS GLOBALS (cridades des de HTML onclick)
// ============================================================================

window.toggleSubmenu = toggleSubmenu;
window.mostrarMissatgeMotivador = mostrarMissatgeMotivador;
window.tancarModalMotivadora = tancarModalMotivadora;
window.canviarMode = canviarMode;
window.canviarPais = canviarPais;
window.guardarPaisNou = guardarPaisNou;
window.cancelarPaisManual = cancelarPaisManual;
window.mostrarTemesPais = mostrarTemesPais;
window.tornarPaisos = tornarPaisos;
window.filtrarPerCategoria = filtrarPerCategoria;
window.filtrarPerTema = filtrarPerTema;
window.mostrarModalAfegirPais = mostrarModalAfegirPais;
window.tancarModalPais = tancarModalPais;
window.confirmarPaisNou = confirmarPaisNou;
window.canviarCategoria = canviarCategoria;

// Executar en carregar la pàgina
document.addEventListener('DOMContentLoaded', function() {
    gestionaErrorsLogin();
});


function toggleNovaCategoriaInput() {
    const container = document.getElementById('container-nova-categoria');
    const input = document.getElementById('nom-categoria-nova');
    
    if (container.style.display === 'none') {
        container.style.display = 'block';
        input.required = true;
        setTimeout(() => input.focus(), 100);
    } else {
        container.style.display = 'none';
        input.required = false;
        input.value = '';
    }
}