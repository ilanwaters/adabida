// ========================================
// ARBRE GENEALÒGIC AMB LÒGICA FAMILIAR
// ========================================

let dadesArbre = null;
let nodesFiltrats = [];
let svg, g, zoom;
let width, height;

// Inicialitzar arbre
document.addEventListener('DOMContentLoaded', function() {
    inicialitzarArbre();
});

async function inicialitzarArbre() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }
        
        dadesArbre = data;
        
        // Trobar creador de la família per defecte
        const creadorId = data.usuari_actual_id;
        
        poblarSelectorPersones(data.nodes, creadorId);
        configurarSVG();
        renderitzarArbre(creadorId);
        
        // Event listeners
        document.getElementById('select-persona').addEventListener('change', function(e) {
            const personaId = parseInt(e.target.value);
            renderitzarArbre(personaId);
        });
        document.getElementById('select-nivell').addEventListener('change', function() {
            const personaId = parseInt(document.getElementById('select-persona').value);
            renderitzarArbre(personaId);
        });
                document.getElementById('btn-reset-zoom').addEventListener('click', resetZoom);
        
    } catch (error) {
        console.error('Error carregant arbre:', error);
    }
}


function poblarSelectorPersones(nodes, defecteId) {
    const select = document.getElementById('select-persona');
    select.innerHTML = '';
    
    nodes.sort((a, b) => a.nom_complet.localeCompare(b.nom_complet));
    
    nodes.forEach(node => {
        const option = document.createElement('option');
        option.value = node.id;
        option.textContent = node.nom_complet || `Membre ${node.id}`;
        if (node.data_naixement) {
            const any = node.data_naixement.split('-')[0];
            option.textContent += ` (${any})`;
        }
        if (node.id === defecteId) {
            option.selected = true;
        }
        select.appendChild(option);
    });
}

function configurarSVG() {
    const container = document.getElementById('arbre-container');
    width = container.clientWidth;
    height = container.clientHeight;
    
    svg = d3.select('#arbre-svg')
        .attr('width', width)
        .attr('height', height);
    
    svg.selectAll('*').remove();
    g = svg.append('g');
    
    zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', function(event) {
            g.attr('transform', event.transform);
        });
    
    svg.call(zoom);
}

function resetZoom() {
    svg.transition()
        .duration(750)
        .call(zoom.transform, d3.zoomIdentity);
}

function renderitzarArbre(personaCentralId) {
    g.selectAll('*').remove();
    
    const maxNivell = parseInt(document.getElementById('select-nivell').value) || 3;
    const generacions = calcularGeneracions(personaCentralId, maxNivell);
    // Dibuixar arbre
    dibuixarArbrePerGeneracions(generacions, personaCentralId);
}

// ========================================
// LÒGICA PRINCIPAL: CALCULAR GENERACIONS
// ========================================

function calcularGeneracions(personaCentralId, maxNivell = 3) {
    const mapa = crearMapaNodes();
    const generacions = {};
    
    // ========== NIVELL 0 ==========
    const nivell0Ascendents = []; // Només usuari 0 i parella per ascendents
    
    // Usuari 0
    generacions[personaCentralId] = 0;
    nivell0Ascendents.push(personaCentralId);
    
    // Parella usuari 0
    const parellaId = obtenirParella(personaCentralId);
    if (parellaId) {
        generacions[parellaId] = 0;
        nivell0Ascendents.push(parellaId);
    }
    

        // Germans usuari 0 (només línia directa, sense cunyats ni família política)
    const germans = obtenirGermans(personaCentralId, mapa);
    germans.forEach(germaId => {
        generacions[germaId] = 0;
    });
    
        // ========== ASCENDENTS ==========
    // A Nivell 1 només puja per línia pròpia (sense sogres); a nivells superiors, també per la parella
    let nivellActual = (maxNivell === 1) ? [personaCentralId] : nivell0Ascendents;
    let nivell = 1;

    while (nivellActual.length > 0 && nivell <= maxNivell) {
        const seguent = [];
    
        nivellActual.forEach(personaId => {
            const persona = mapa[personaId];
            if (!persona) return;
        
            if (persona.pare_id) {
                generacions[persona.pare_id] = nivell;
                seguent.push(persona.pare_id);
            
            // AFEGIR PARELLA DEL PARE
                const parellaParee = obtenirParella(persona.pare_id);
                if (parellaParee && !generacions[parellaParee]) {
                    generacions[parellaParee] = nivell;
                    seguent.push(parellaParee);
                }
            }
            if (persona.mare_id) {
                generacions[persona.mare_id] = nivell;
                seguent.push(persona.mare_id);
            
            // AFEGIR PARELLA DE LA MARE
                const parellaMare = obtenirParella(persona.mare_id);
                if (parellaMare && !generacions[parellaMare]) {
                    generacions[parellaMare] = nivell;
                    seguent.push(parellaMare);
                }
            }
        });
    
        nivellActual = seguent;
        nivell++;
    }

        // ========== DESCENDENTS ==========
    // A Nivell 1 només fills propis; a nivells superiors, també nebots (fills dels germans)
    const totesPersonesNivell0 = [personaCentralId];
    if (parellaId) totesPersonesNivell0.push(parellaId);
    if (maxNivell >= 2) {
        germans.forEach(germaId => {
            totesPersonesNivell0.push(germaId);
            const parellaGerma = obtenirParella(germaId);
            if (parellaGerma) {
                generacions[parellaGerma] = 0;
                totesPersonesNivell0.push(parellaGerma);
            }
        });
    }

    let nivellDescendent = totesPersonesNivell0;
    nivell = -1;
    
    while (nivellDescendent.length > 0 && nivell >= -maxNivell) {
        const seguent = [];
        
        nivellDescendent.forEach(personaId => {
            const fills = obtenirFills(personaId, mapa);
            
            fills.forEach(fillId => {
                if (!generacions[fillId]) {
                    generacions[fillId] = nivell;
                    seguent.push(fillId);
                    
                    // Parella del fill
                    const parellaFill = obtenirParella(fillId);
                    if (parellaFill && !generacions[parellaFill]) {
                        generacions[parellaFill] = nivell;
                        seguent.push(parellaFill);
                    }
                }
            });
        });
        
        nivellDescendent = seguent;
        nivell--;
    }
    
    return generacions;
}

// ========================================
// FUNCIONS AUXILIARS
// ========================================

function crearMapaNodes() {
    const mapa = {};
    dadesArbre.nodes.forEach(node => {
        mapa[node.id] = node;
    });
    return mapa;
}

function obtenirParella(personaId) {
    const matrimoni = dadesArbre.matrimonis.find(m => 
        (m.membre_1_id === personaId || m.membre_2_id === personaId) &&
        m.estat === 'actiu'
    );
    
    if (!matrimoni) return null;
    
    return matrimoni.membre_1_id === personaId ? 
           matrimoni.membre_2_id : 
           matrimoni.membre_1_id;
}

function obtenirGermans(personaId, mapa) {
    const persona = mapa[personaId];
    if (!persona) return [];
    
    return dadesArbre.nodes
        .filter(n => n.id !== personaId && 
                ((persona.pare_id && n.pare_id === persona.pare_id) || 
                 (persona.mare_id && n.mare_id === persona.mare_id)))
        .map(n => n.id);
}

function obtenirPares(personaId, mapa) {
    const persona = mapa[personaId];
    const pares = [];
    if (persona.pare_id) pares.push(persona.pare_id);
    if (persona.mare_id) pares.push(persona.mare_id);
    return pares;
}

function obtenirFills(personaId, mapa) {
    return dadesArbre.nodes
        .filter(n => n.pare_id === personaId || n.mare_id === personaId)
        .map(n => n.id);
}
// ========================================
// PAS A: CALCULAR AMPLADA DE SUBARBRES
// ========================================

function calcularAmplada(personaId, mapa, generacions, cache = {}) {
    if (cache[personaId] !== undefined) return cache[personaId];

    const fills = obtenirFills(personaId, mapa)
        .filter(fId => generacions[fId] !== undefined);

    if (fills.length === 0) {
        cache[personaId] = 1;
        return 1;
    }

    let amplada = 0;
    fills.forEach(fillId => {
        amplada += calcularAmplada(fillId, mapa, generacions, cache);
    });

    cache[personaId] = amplada;
    return amplada;
}

// ========================================
// PAS A.2: AMPLADA D'UNA UNITAT FAMILIAR (persona + parella)
// ========================================

function calcularAmpladaUnitat(personaId, mapa, generacions, cache = {}) {
    const parellaId = obtenirParella(personaId);
    
    const fillsPropis = obtenirFills(personaId, mapa)
        .filter(fId => generacions[fId] !== undefined);
    const fillsParella = parellaId 
        ? obtenirFills(parellaId, mapa).filter(fId => generacions[fId] !== undefined)
        : [];
    
    // Units (evitar comptar fills duplicats si comparteixen fills)
    const totsFills = [...new Set([...fillsPropis, ...fillsParella])];
    
    if (totsFills.length === 0) {
        return 1; // unitat sense fills = 1 slot
    }
    
    let amplada = 0;
    totsFills.forEach(fillId => {
        amplada += calcularAmpladaUnitat(fillId, mapa, generacions, cache);
    });
    
    return amplada;
}
// ========================================
// PAS A.3: AMPLADA TOTAL DE NIVELL 0
// ========================================

function calcularAmplesNivell0(personaCentralId, mapa, generacions) {
    const amples = {};
    
    // Unitat central
    amples[personaCentralId] = calcularAmpladaUnitat(personaCentralId, mapa, generacions);
    
    // Germans (cadascun com a unitat pròpia)
    const germans = obtenirGermans(personaCentralId, mapa)
        .filter(gId => generacions[gId] === 0);
    
    germans.forEach(germaId => {
        amples[germaId] = calcularAmpladaUnitat(germaId, mapa, generacions);
    });
    
    return amples;
}
// ========================================
// DIBUIXAR ARBRE
// ========================================

function dibuixarArbrePerGeneracions(generacions, personaCentralId) {
    const ESPAI_Y = 150;
    const ESPAI_X = 200;
    const mapa = crearMapaNodes();
    const cacheAmplades = {};
    const amplesNivell0 = calcularAmplesNivell0(personaCentralId, mapa, generacions);
    console.log('Amples de tot nivell 0:', amplesNivell0);
    // Organitzar per nivells
    const nivells = {};
    Object.keys(generacions).forEach(id => {
        const niv = generacions[id];
        if (!nivells[niv]) nivells[niv] = [];
        nivells[niv].push(parseInt(id));
    });
    
    const posicions = {};
    const nivellsOrdenats = Object.keys(nivells).map(Number).sort((a, b) => a - b);
    const offsetY = -nivellsOrdenats[0] * ESPAI_Y + 100;
    
    // ========== ASSIGNAR SLOTS ==========
    const slots = assignarSlots(personaCentralId, generacions, mapa);
    
    // ========== CALCULAR POSICIONS ==========
    Object.keys(slots).forEach(personaId => {
        const niv = generacions[personaId];
        const slot = slots[personaId];
        
        const x = slot * ESPAI_X + width / 2;
        const y = -niv * ESPAI_Y + offsetY;
        
        posicions[personaId] = {x, y};
    });
    
    // Dibuixar
    dibuixarLlinesMatrimoni(posicions);
    dibuixarLlinesPareFill(posicions);
    dibuixarNodes(posicions, personaCentralId);
    
    // Centrar vista
    setTimeout(() => {
    // Centrar en l'usuari principal
        const posUsuari = posicions[personaCentralId];
        const parellaId = obtenirParella(personaCentralId);
        const posParella = parellaId ? posicions[parellaId] : null;
    
        const xCentre = posParella ? (posUsuari.x + posParella.x) / 2 : posUsuari.x;
        const yCentre = posUsuari.y;
    
        const scale = 0.8;
        const tx = width / 2 - xCentre * scale;
        const ty = height / 2 - yCentre * scale;
    
        svg.transition().duration(750)
            .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
    }, 100);
}
function assignarSlots(adminId, generacions, mapa) {
    const slots = {};
    
    // ========== NIVELL 0 ==========
    slots[adminId] = 0;
    
    const parellaAdmin = obtenirParella(adminId);
    if (parellaAdmin) {
        slots[parellaAdmin] = 1;
    }
    
    // Germans admin (esquerra)
    const germansAdmin = obtenirGermans(adminId, mapa);
    let slotEsquerra = -2;
    germansAdmin.forEach(germaId => {
        if (generacions[germaId] === 0) {
            slots[germaId] = slotEsquerra;
            
            const parellaGerma = obtenirParella(germaId);
            if (parellaGerma && generacions[parellaGerma] === 0) {
                slots[parellaGerma] = slotEsquerra - 1;
            }
            
            slotEsquerra -= 2;
        }
    });
    
    // Germans esposa (dreta)
    if (parellaAdmin) {
        const germansEsposa = obtenirGermans(parellaAdmin, mapa);
        let slotDreta = 3;
        germansEsposa.forEach(germaId => {
            if (generacions[germaId] === 0) {
                slots[germaId] = slotDreta;
                
                const parellaGerma = obtenirParella(germaId);
                if (parellaGerma && generacions[parellaGerma] === 0) {
                    slots[parellaGerma] = slotDreta + 1;
                }
                
                slotDreta += 2;
            }
        });
    }
    
    // ========== ASCENDENTS ==========
    for (let niv = 1; niv <= 3; niv++) {
        const personesPendents = [];
        const slotsOcupats = new Set(Object.values(slots).filter(s => s !== undefined));
        
        // 1. Pares directes
        // 1. Pares directes - ordenar per posició dels fills
        const parellesPares = [];

        Object.keys(generacions).forEach(personaId => {
            if (generacions[personaId] === niv && slots[personaId] === undefined) {
                const pid = parseInt(personaId);
                const fills = obtenirFills(pid, mapa)
                    .filter(fId => generacions[fId] === niv - 1 && slots[fId] !== undefined);
        
                if (fills.length > 0) {
                    const slotsFills = fills.map(fId => slots[fId]);
                    const slotMig = (Math.min(...slotsFills) + Math.max(...slotsFills)) / 2;
            
                    const parellaId = obtenirParella(pid);
                    if (parellaId && generacions[parellaId] === niv && !slots[parellaId]) {
                        parellesPares.push({
                            pare1: pid,
                            pare2: parellaId,
                            slotMig: slotMig
                        });
                    }
                }
            }
        });

// Ordenar parelles d'esquerra a dreta segons fills
        parellesPares.sort((a, b) => a.slotMig - b.slotMig);

// Assignar slots a parelles ordenades
        parellesPares.forEach(parella => {
            let slotPare = Math.floor(parella.slotMig);
    
            while (slotsOcupats.has(slotPare) || slotsOcupats.has(slotPare + 1)) {
                if (slotPare < parella.slotMig) {
                    slotPare--;
                } else {
                    slotPare++;
                }
            }
    
            slots[parella.pare1] = slotPare;
            slots[parella.pare2] = slotPare + 1;
            slotsOcupats.add(slotPare);
            slotsOcupats.add(slotPare + 1);
            personesPendents.push(parella.pare1, parella.pare2);
        });

// Pares sense parella
        Object.keys(generacions).forEach(personaId => {
            if (generacions[personaId] === niv && slots[personaId] === undefined) {
                const pid = parseInt(personaId);
                const fills = obtenirFills(pid, mapa)
                    .filter(fId => generacions[fId] === niv - 1 && slots[fId] !== undefined);
        
                if (fills.length > 0) {
                    const slotsFills = fills.map(fId => slots[fId]);
                    const slotMig = (Math.min(...slotsFills) + Math.max(...slotsFills)) / 2;
            
                    let slot = Math.floor(slotMig);
                    while (slotsOcupats.has(slot)) {
                        slot++;
                    }
                    slots[pid] = slot;
                    slotsOcupats.add(slot);
                    personesPendents.push(pid);
                }
            }
        });
        // 2. Germans
        personesPendents.forEach(personaId => {
            const germans = obtenirGermans(personaId, mapa)
                .filter(gId => generacions[gId] === niv && !slots[gId]);
            
            const slotBase = slots[personaId];
            const esEsquerra = slotBase < 0.5;
            
            germans.forEach(germaId => {
                let slotGerma;
                let intent = 1;
                do {
                    slotGerma = esEsquerra ? slotBase - intent : slotBase + intent;
                    intent++;
                } while (slotsOcupats.has(slotGerma));
                
                slots[germaId] = slotGerma;
                slotsOcupats.add(slotGerma);
                
                const parellaGerma = obtenirParella(germaId);
                if (parellaGerma && generacions[parellaGerma] === niv && !slots[parellaGerma]) {
                    let slotParella = esEsquerra ? slotGerma - 1 : slotGerma + 1;
                    
                    while (slotsOcupats.has(slotParella)) {
                        slotParella = esEsquerra ? slotParella - 1 : slotParella + 1;
                    }
                    
                    slots[parellaGerma] = slotParella;
                    slotsOcupats.add(slotParella);
                }
            });
        });
    }
    
    // ========== DESCENDENTS ==========
    Object.keys(generacions).forEach(personaId => {
        const niv = generacions[personaId];
        if (niv < 0 && slots[personaId] === undefined) {
            const persona = mapa[personaId];
            if (persona && (persona.pare_id || persona.mare_id)) {
                const slotsPares = [];
                if (persona.pare_id && slots[persona.pare_id] !== undefined) {
                    slotsPares.push(slots[persona.pare_id]);
                }
                if (persona.mare_id && slots[persona.mare_id] !== undefined) {
                    slotsPares.push(slots[persona.mare_id]);
                }
                
                if (slotsPares.length > 0) {
                    const slotMig = slotsPares.reduce((a, b) => a + b, 0) / slotsPares.length;
                    
                    const germans = obtenirGermans(parseInt(personaId), mapa)
                        .filter(gId => generacions[gId] === niv);
                    
                    const fillsMatrimoni = [parseInt(personaId), ...germans];
                    fillsMatrimoni.forEach((fillId, idx) => {
                        slots[fillId] = slotMig + (idx - fillsMatrimoni.length / 2 + 0.5) * 0.8;
                        
                        const parellaFill = obtenirParella(fillId);
                        if (parellaFill && generacions[parellaFill] === niv && !slots[parellaFill]) {
                            slots[parellaFill] = slots[fillId] + 0.5;
                        }
                    });
                }
            }
        }
    });
    
    
    // ========== NORMALITZAR SLOTS PER NIVELL ==========
    const normalitzats = {};

// Agrupar per nivell
    const perNivell = {};
    Object.keys(slots).forEach(personaId => {
        const niv = generacions[personaId];
        if (!perNivell[niv]) perNivell[niv] = [];
        perNivell[niv].push(parseInt(personaId));
    });

// Normalitzar cada nivell independentment
    Object.keys(perNivell).forEach(niv => {
        const persones = perNivell[niv];
    
    // Ordenar per slot original
        persones.sort((a, b) => slots[a] - slots[b]);
    
    // Assignar slots consecutius començant a 0
        const processats = new Set();
        let index = 0;
    
        persones.forEach(pid => {
            if (processats.has(pid)) return;
        
            const parellaId = obtenirParella(pid);
        
            if (parellaId && slots[parellaId] !== undefined && !processats.has(parellaId) && generacions[parellaId] === parseInt(niv)) {
                normalitzats[pid] = index;
                normalitzats[parellaId] = index + 1;
                processats.add(pid);
                processats.add(parellaId);
                index += 2;
            } else if (!processats.has(pid)) {
                normalitzats[pid] = index;
                processats.add(pid);
                index += 1;
            }
        });


        const offset = (index - 1) / 2;
        persones.forEach(pid => {
            normalitzats[pid] -= offset;
        });
    });
    return normalitzats;
}
      
function ordenarNivell0(persones) {
    const processades = new Set();
    const ordenades = [];
    
    dadesArbre.matrimonis.forEach(mat => {
        if (persones.includes(mat.membre_1_id) && persones.includes(mat.membre_2_id) &&
            !processades.has(mat.membre_1_id) && !processades.has(mat.membre_2_id)) {
            ordenades.push(mat.membre_1_id, mat.membre_2_id);
            processades.add(mat.membre_1_id);
            processades.add(mat.membre_2_id);
        }
    });
    
    persones.forEach(pId => {
        if (!processades.has(pId)) {
            ordenades.push(pId);
            processades.add(pId);
        }
    });
    
    return ordenades;
}

function ordenarPerFills(persones, posicions, mapa, nivell) {
    const ESPAI_X = 90;
    const processades = new Set();
    let xActual = 0;
    
    // Agrupar per matrimonis
    const matrimonisAquestNivell = [];
    dadesArbre.matrimonis.forEach(mat => {
        if (persones.includes(mat.membre_1_id) && persones.includes(mat.membre_2_id)) {
            matrimonisAquestNivell.push([mat.membre_1_id, mat.membre_2_id]);
            processades.add(mat.membre_1_id);
            processades.add(mat.membre_2_id);
        }
    });
    
    // Posicionar cada matrimoni centrat respecte fills
    matrimonisAquestNivell.forEach(([pare, mare]) => {
        const fills = obtenirFills(pare, mapa).filter(fId => posicions[fId]);
        
        if (fills.length > 0) {
            // Centrar entre fills
            const xFills = fills.map(fId => posicions[fId].x);
            const xMin = Math.min(...xFills);
            const xMax = Math.max(...xFills);
            const xCentre = (xMin + xMax) / 2;
            
            posicions[pare] = {x: xCentre - ESPAI_X/4};
            posicions[mare] = {x: xCentre + ESPAI_X/4};
        } else {
            // Sense fills: posició lliure
            posicions[pare] = {x: xActual};
            posicions[mare] = {x: xActual + ESPAI_X};
            xActual += ESPAI_X * 2;
        }
    });
    
    // Resta de persones (sense parella a aquest nivell)
    persones.forEach(pId => {
        if (!processades.has(pId)) {
            const fills = obtenirFills(pId, mapa).filter(fId => posicions[fId]);
            
            if (fills.length > 0) {
                const xFills = fills.map(fId => posicions[fId].x);
                const xCentre = (Math.min(...xFills) + Math.max(...xFills)) / 2;
                posicions[pId] = {x: xCentre};
            } else {
                posicions[pId] = {x: xActual};
                xActual += ESPAI_X;
            }
            processades.add(pId);
        }
    });
    
    return Array.from(processades);
}



function dibuixarLlinesMatrimoni(posicions) {
    dadesArbre.matrimonis.forEach(mat => {
        const pos1 = posicions[mat.membre_1_id];
        const pos2 = posicions[mat.membre_2_id];
        
        if (!pos1 || !pos2) return;
        
        g.append('line')
            .attr('x1', pos1.x)
            .attr('y1', pos1.y)
            .attr('x2', pos2.x)
            .attr('y2', pos2.y)
            .attr('stroke', '#a8b0c3')
            .attr('stroke-width', 2)
            .style('opacity', 0.9);
    });
}

function dibuixarLlinesPareFill(posicions) {
    const mapa = crearMapaNodes();
    
    dadesArbre.nodes.forEach(node => {
        const posFill = posicions[node.id];
        if (!posFill) return;
        
        const pare = node.pare_id ? mapa[node.pare_id] : null;
        const mare = node.mare_id ? mapa[node.mare_id] : null;
        
        if (pare && mare && posicions[pare.id] && posicions[mare.id]) {
            const posPare = posicions[pare.id];
            const posMare = posicions[mare.id];
            
            const puntMigX = (posPare.x + posMare.x) / 2;
            const puntMigY = Math.max(posPare.y, posMare.y);
            const punIntermigY = puntMigY + 40;
            
            const distanciaH = Math.abs(posFill.x - puntMigX);
            const r1 = Math.min(12, distanciaH / 2);
            const signe1 = posFill.x >= puntMigX ? 1 : -1;
            g.append('path')
                .attr('d', `M ${puntMigX},${puntMigY}
                            L ${puntMigX},${punIntermigY - r1}
                            Q ${puntMigX},${punIntermigY} ${puntMigX + signe1 * r1},${punIntermigY}
                            L ${posFill.x - signe1 * r1},${punIntermigY}
                            Q ${posFill.x},${punIntermigY} ${posFill.x},${punIntermigY + r1}
                            L ${posFill.x},${posFill.y - 30}`)
                .attr('fill', 'none')
                .attr('stroke', '#b8bfd1')
                .attr('stroke-width', 1.8)
                .style('opacity', 0.85);
        }
        
        else if (pare && posicions[pare.id]) {
        const posPare = posicions[pare.id];
        const punIntermigY = posPare.y + 40;
    
            g.append('path')
                .attr('d', `M ${posPare.x},${posPare.y} L ${posPare.x},${punIntermigY} L ${posFill.x},${punIntermigY} L ${posFill.x},${posFill.y - 30}`)
                .attr('fill', 'none')
                .attr('stroke', '#b8bfd1')
                .attr('stroke-width', 1.8)
                .style('opacity', 0.7);
        }
// Cas 3: Només mare (LÍNIA 318-329)
        else if (mare && posicions[mare.id]) {
            const posMare = posicions[mare.id];
            const punIntermigY = posMare.y + 40;
    
            g.append('path')
                .attr('d', `M ${posMare.x},${posMare.y} L ${posMare.x},${punIntermigY} L ${posFill.x},${punIntermigY} L ${posFill.x},${posFill.y - 30}`)
                .attr('fill', 'none')
                .attr('stroke', '#3498db')
                .attr('stroke-width', 2)
                .style('opacity', 0.5);
        }
    });
}

function dibuixarNodes(posicions, personaCentralId) {
    const mapa = crearMapaNodes();
    
    Object.keys(posicions).forEach(id => {
        const persona = mapa[id];
        if (!persona) return;
    

        const {x, y} = posicions[id];
        const esActual = parseInt(id) === personaCentralId;
        const nodeGrup = g.append('g')
            .attr('transform', `translate(${x}, ${y})`)
            .style('cursor', 'pointer')
            .on('click', () => window.location.href = `/familia/membre/${persona.id}`);

        
        nodeGrup.append('rect')
            .attr('x', -80)
            .attr('y', -32)
            .attr('width', 160)
            .attr('height', 64)
            .attr('fill', esActual ? '#5b6ee8' : '#fefefe')
            .attr('stroke', esActual ? '#5b6ee8' : '#d8d8d8')
            .attr('stroke-width', esActual ? 2 : 1.5)
            .attr('rx', 10)
            .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.08))');
        const nomComplet = `${persona.nom || ''} ${persona.primer_cognom || ''}`.trim();
        const nomMostrat = nomComplet.length > 18 ? nomComplet.substring(0, 17) + '…' : nomComplet;
        
        nodeGrup.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', -5)
            .attr('font-size', '13px')
            .attr('font-family', "'Segoe UI', system-ui, sans-serif")
            .attr('font-weight', '600')
            .attr('fill', esActual ? '#ffffff' : '#2a2a2a')
            .text(nomMostrat);
        
        if (persona.data_naixement) {
            const any = persona.data_naixement.split('-')[0];
            nodeGrup.append('text')
                .attr('text-anchor', 'middle')
                .attr('dy', 12)
                .attr('font-size', '11px')
                .attr('fill', esActual ? '#fff' : '#666')
                .text(any);
        }
    });
}