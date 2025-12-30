// ========================================
// ARBRE GENEALÒGIC INTERACTIU AMB D3.JS
// ========================================

let dadesArbre = null;
let nodesFiltrats = [];
let connexionsFiltrades = [];
let svg, g, zoom;
let width, height;

// Inicialitzar arbre
document.addEventListener('DOMContentLoaded', function() {
    inicialitzarArbre();
});

async function inicialitzarArbre() {
    try {
        // Carregar dades de l'API
        const response = await fetch(API_URL);
        const data = await response.json();
        
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }
        
        dadesArbre = data;
        
        // Poblar selector de persones
        poblarSelectorPersones(data.nodes, data.usuari_actual_id);
        
        // Configurar SVG i zoom
        configurarSVG();
        
        // Renderitzar arbre inicial (centrat en usuari actual)
        renderitzarArbre(data.usuari_actual_id, 1);
        
        // Event listeners
        document.getElementById('select-persona').addEventListener('change', function(e) {
            const personaId = parseInt(e.target.value);
            const nivell = parseInt(document.getElementById('select-nivell').value);
            renderitzarArbre(personaId, nivell);
        });
        
        document.getElementById('select-nivell').addEventListener('change', function(e) {
            const personaId = parseInt(document.getElementById('select-persona').value);
            const nivell = parseInt(e.target.value);
            renderitzarArbre(personaId, nivell);
        });
        
        document.getElementById('btn-reset-zoom').addEventListener('click', function() {
            resetZoom();
        });
        
    } catch (error) {
        console.error('Error carregant arbre:', error);
    }
}

function poblarSelectorPersones(nodes, usuariActualId) {
    const select = document.getElementById('select-persona');
    select.innerHTML = '';
    
    // Ordenar per nom
    nodes.sort((a, b) => a.nom_complet.localeCompare(b.nom_complet));
    
    nodes.forEach(node => {
        const option = document.createElement('option');
        option.value = node.id;
        option.textContent = node.nom_complet;
        if (node.data_naixement) {
            const any = node.data_naixement.split('-')[0];
            option.textContent += ` (${any})`;
        }
        if (node.id === usuariActualId) {
            option.selected = true;
            option.textContent += ' (Tu)';
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
    
    // Netejar SVG anterior
    svg.selectAll('*').remove();
    
    // Grup principal amb zoom
    g = svg.append('g');
    
    // Configurar zoom
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

function renderitzarArbre(personaCentralId, nivell) {
    // Filtrar nodes segons nivell de parentiu
    nodesFiltrats = filtrarPerNivellParentiu(personaCentralId, nivell);
    
    // Crear estructura jeràrquica
    const jerarquia = crearJerarquia(personaCentralId);
    
    // Layout d'arbre
    const treeLayout = d3.tree()
        .size([height - 100, width - 200])
        .separation((a, b) => a.parent === b.parent ? 1 : 1.2);
    
    const root = d3.hierarchy(jerarquia);
    treeLayout(root);
    
    // Netejar SVG
    g.selectAll('*').remove();
    
    // Dibuixar connexions (línies)
    dibuixarConnexions(root);
    
    // Dibuixar matrimonis
    dibuixarMatrimonis();
    
    // Dibuixar nodes (persones)
    dibuixarNodes(root, personaCentralId);
    
    // Centrar vista
    centrarVista(root);
}

function filtrarPerNivellParentiu(personaCentralId, nivell) {
    if (nivell === 999) {
        return dadesArbre.nodes; // Tots
    }
    
    const nodesFiltrats = new Set();
    const mapa = crearMapaNodes();
    
    // Afegir persona central
    nodesFiltrats.add(personaCentralId);
    
    // Nivell 1: pares, fills, germans
    if (nivell >= 1) {
        afegirPares(personaCentralId, nodesFiltrats, mapa);
        afegirFills(personaCentralId, nodesFiltrats, mapa);
        afegirGermans(personaCentralId, nodesFiltrats, mapa);
    }
    
    // Nivell 2: avis, néts, tiets, cosins
    if (nivell >= 2) {
        const pares = obtenirPares(personaCentralId, mapa);
        pares.forEach(pareId => {
            afegirPares(pareId, nodesFiltrats, mapa); // Avis
            afegirGermans(pareId, nodesFiltrats, mapa); // Tiets
        });
        
        const fills = obtenirFills(personaCentralId, mapa);
        fills.forEach(fillId => {
            afegirFills(fillId, nodesFiltrats, mapa); // Néts
        });
        
        const germans = obtenirGermans(personaCentralId, mapa);
        germans.forEach(germaId => {
            afegirFills(germaId, nodesFiltrats, mapa); // Cosins
        });
    }
    
    // Nivell 3: besavis, besnéts, tiets-avis
    if (nivell >= 3) {
        const avis = [];
        const pares = obtenirPares(personaCentralId, mapa);
        pares.forEach(pareId => {
            const avisIds = obtenirPares(pareId, mapa);
            avis.push(...avisIds);
        });
        
        avis.forEach(aviId => {
            afegirPares(aviId, nodesFiltrats, mapa); // Besavis
            afegirGermans(aviId, nodesFiltrats, mapa); // Tiets-avis
        });
        
        const nets = [];
        const fills = obtenirFills(personaCentralId, mapa);
        fills.forEach(fillId => {
            const netsIds = obtenirFills(fillId, mapa);
            nets.push(...netsIds);
        });
        
        nets.forEach(netId => {
            afegirFills(netId, nodesFiltrats, mapa); // Besnéts
        });
    }
    
    return dadesArbre.nodes.filter(n => nodesFiltrats.has(n.id));
}

function crearMapaNodes() {
    const mapa = {};
    dadesArbre.nodes.forEach(node => {
        mapa[node.id] = node;
    });
    return mapa;
}

function afegirPares(nodeId, conjunt, mapa) {
    const node = mapa[nodeId];
    if (!node) return;
    
    if (node.pare_id) conjunt.add(node.pare_id);
    if (node.mare_id) conjunt.add(node.mare_id);
}

function afegirFills(nodeId, conjunt, mapa) {
    dadesArbre.nodes.forEach(n => {
        if (n.pare_id === nodeId || n.mare_id === nodeId) {
            conjunt.add(n.id);
        }
    });
}

function afegirGermans(nodeId, conjunt, mapa) {
    const node = mapa[nodeId];
    if (!node) return;
    
    dadesArbre.nodes.forEach(n => {
        if (n.id === nodeId) return;
        if ((node.pare_id && n.pare_id === node.pare_id) || 
            (node.mare_id && n.mare_id === node.mare_id)) {
            conjunt.add(n.id);
        }
    });
}

function obtenirPares(nodeId, mapa) {
    const node = mapa[nodeId];
    const pares = [];
    if (node.pare_id) pares.push(node.pare_id);
    if (node.mare_id) pares.push(node.mare_id);
    return pares;
}

function obtenirFills(nodeId, mapa) {
    return dadesArbre.nodes.filter(n => n.pare_id === nodeId || n.mare_id === nodeId).map(n => n.id);
}

function obtenirGermans(nodeId, mapa) {
    const node = mapa[nodeId];
    if (!node) return [];
    
    return dadesArbre.nodes
        .filter(n => n.id !== nodeId && 
                ((node.pare_id && n.pare_id === node.pare_id) || 
                 (node.mare_id && n.mare_id === node.mare_id)))
        .map(n => n.id);
}


function mostrarDetalls(node) {
    // Redirigir a la pàgina del membre
    const urlMembre = `/familia/membre/${node.id}`;
    window.location.href = urlMembre;
}

function renderitzarArbre(personaCentralId, nivell) {
    nodesFiltrats = filtrarPerNivellParentiu(personaCentralId, nivell);
    
    // Calcular generacions des de la persona central
    const generacions = calcularGeneracions(personaCentralId);
    
    // Netejar
    g.selectAll('*').remove();
    
    // Dibuixar tot
    dibuixarArbrePerGeneracions(generacions, personaCentralId);
}

function calcularGeneracions(personaCentralId) {
    const mapa = crearMapaNodes();
    const generacions = {};
    const visitats = new Set();
    
    function afegir(nodeId, nivell) {
        if (!mapa[nodeId] || visitats.has(nodeId)) return;
        if (!nodesFiltrats.find(n => n.id === nodeId)) return;
        
        visitats.add(nodeId);
        if (!generacions[nivell]) generacions[nivell] = [];
        generacions[nivell].push(mapa[nodeId]);
        
        // Pares amunt
        const node = mapa[nodeId];
        if (node.pare_id) afegir(node.pare_id, nivell - 1);
        if (node.mare_id) afegir(node.mare_id, nivell - 1);
        
        // Fills avall
        obtenirFills(nodeId, mapa).forEach(fid => afegir(fid, nivell + 1));
    }
    
    afegir(personaCentralId, 0);
    return generacions;
}
function dibuixarArbrePerGeneracions(generacions, personaCentralId) {
    const nivells = Object.keys(generacions).map(Number).sort((a, b) => a - b);
    const posicions = {};
    
    const ESPAI_Y = 150;
    const ESPAI_X = 200;
    const offsetY = -nivells[0] * ESPAI_Y + 100;
    
    // Calcular posicions
    nivells.forEach(niv => {
        const nodes = generacions[niv];
        const y = niv * ESPAI_Y + offsetY;
        nodes.forEach((node, i) => {
            const x = (i - nodes.length / 2 + 0.5) * ESPAI_X + width / 2;
            posicions[node.id] = {x, y, node};
        });
    });
    
    // Dibuixar connexions intel·ligents
    const fillsProcessats = new Set();
    
    nodesFiltrats.forEach(fill => {
        if (fillsProcessats.has(fill.id)) return;
        if (!fill.pare_id && !fill.mare_id) return;
        
        const posFill = posicions[fill.id];
        const posPare = fill.pare_id ? posicions[fill.pare_id] : null;
        const posMare = fill.mare_id ? posicions[fill.mare_id] : null;
        
        if (!posFill) return;
        
        if (posPare && posMare) {
            // Ambdós pares: línia entre ells, després al fill
            const midX = (posPare.x + posMare.x) / 2;
            const midY = (posPare.y + posMare.y) / 2 + 25;
            
            // Línia horitzontal entre pares
            g.append('line')
                .attr('x1', posPare.x).attr('y1', posPare.y + 25)
                .attr('x2', posMare.x).attr('y2', posMare.y + 25)
                .attr('class', 'link-arbre');
            
            // Línia vertical al mig cap avall
            g.append('line')
                .attr('x1', midX).attr('y1', midY)
                .attr('x2', midX).attr('y2', posFill.y - 40)
                .attr('class', 'link-arbre');
            
            // Línia al fill
            g.append('line')
                .attr('x1', midX).attr('y1', posFill.y - 40)
                .attr('x2', posFill.x).attr('y2', posFill.y - 25)
                .attr('class', 'link-arbre');
            
            fillsProcessats.add(fill.id);
            
        } else if (posPare) {
            // Només pare
            g.append('line')
                .attr('x1', posPare.x).attr('y1', posPare.y + 25)
                .attr('x2', posFill.x).attr('y2', posFill.y - 25)
                .attr('class', 'link-arbre');
        } else if (posMare) {
            // Només mare
            g.append('line')
                .attr('x1', posMare.x).attr('y1', posMare.y + 25)
                .attr('x2', posFill.x).attr('y2', posFill.y - 25)
                .attr('class', 'link-arbre');
        }
    });
    
    // Dibuixar nodes (resta igual)
    Object.values(posicions).forEach(({x, y, node}) => {
        const esActual = node.id === personaCentralId;
        const classe = esActual ? 'node-home' : !node.viu ? 'node-difunt' : 'node-desconegut';
        
        const g2 = g.append('g')
            .attr('class', `node-arbre ${classe}`)
            .attr('transform', `translate(${x},${y})`)
            .on('click', () => mostrarDetalls(node));
        
        g2.append('rect')
            .attr('class', 'node-rect')
            .attr('x', -80).attr('y', -25)
            .attr('width', 160).attr('height', 50);
        
        g2.append('text')
            .attr('class', 'node-text')
            .attr('dy', -5).attr('text-anchor', 'middle')
            .text(`${node.nom || ''} ${node.primer_cognom || ''}`.trim().substring(0, 20));
        
        if (node.data_naixement) {
            const txt = node.data_naixement.split('-')[0] + 
                (node.data_defuncio ? '-' + node.data_defuncio.split('-')[0] : '');
            g2.append('text')
                .attr('class', 'node-text-petit')
                .attr('dy', 10).attr('text-anchor', 'middle')
                .text(txt);
        }
    });
    
    // Centrar
    setTimeout(() => {
        const bbox = g.node().getBBox();
        const scale = 0.85;
        const tx = (width - bbox.width * scale) / 2 - bbox.x * scale;
        const ty = (height - bbox.height * scale) / 2 - bbox.y * scale;
        svg.transition().duration(750)
            .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
    }, 100);
}