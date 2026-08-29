/**
 * Sistema de consentiment informat amb signatura digital
 */

let canvas, ctx;
let signant = false;
let signatura_present = false;

document.addEventListener('DOMContentLoaded', function() {
    inicialitzarCanvas();
    inicialitzarAutoOmpliment();
});

/**
 * Inicialitza el canvas de signatura
 */
function inicialitzarCanvas() {
    canvas = document.getElementById('canvas-signatura');
    if (!canvas) return;
    
    ctx = canvas.getContext('2d');
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    
    // Events mouse
    canvas.addEventListener('mousedown', iniciarSignatura);
    canvas.addEventListener('mousemove', dibuixarSignatura);
    canvas.addEventListener('mouseup', aturarSignatura);
    canvas.addEventListener('mouseleave', aturarSignatura);
    
    // Events touch (mòbil/tauleta)
    canvas.addEventListener('touchstart', iniciarSignaturaTactil);
    canvas.addEventListener('touchmove', dibuixarSignaturaTactil);
    canvas.addEventListener('touchend', aturarSignatura);
    
    // Botó esborrar
    const botoNeteja = document.getElementById('neteja-signatura');
    if (botoNeteja) {
        botoNeteja.addEventListener('click', esborrarSignatura);
    }
}

function iniciarSignatura(e) {
    signant = true;
    const rect = canvas.getBoundingClientRect();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    signatura_present = true;
}

function dibuixarSignatura(e) {
    if (!signant) return;
    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
}

function aturarSignatura() {
    signant = false;
    if (signatura_present) {
        guardarSignatura();
    }
}

function iniciarSignaturaTactil(e) {
    e.preventDefault();
    signant = true;
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    ctx.beginPath();
    ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
    signatura_present = true;
}

function dibuixarSignaturaTactil(e) {
    if (!signant) return;
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
    ctx.stroke();
}

function guardarSignatura() {
    const signaturaData = canvas.toDataURL('image/png');
    document.getElementById('signatura-data').value = signaturaData;
}

function esborrarSignatura() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('signatura-data').value = '';
    signatura_present = false;
}

/**
 * Auto-ompliment del document de consentiment
 */
function inicialitzarAutoOmpliment() {
    // Camps de l'entrevistat
    const campsNom = ['entrevistat_nom', 'entrevistat_cognom1', 'entrevistat_cognom2'];
    campsNom.forEach(campId => {
        const camp = document.getElementById(campId);
        if (camp) {
            camp.addEventListener('input', actualitzarNomConsentiment);
        }
    });
    
    // Camp de lloc
    const campLloc = document.getElementById('municipi_lloc');
    if (campLloc) {
        campLloc.addEventListener('input', actualitzarLlocDataConsentiment);
    }
}

function actualitzarNomConsentiment() {
    const nom = document.getElementById('entrevistat_nom')?.value || '';
    const cognom1 = document.getElementById('entrevistat_cognom1')?.value || '';
    const cognom2 = document.getElementById('entrevistat_cognom2')?.value || '';
    
    const nomComplet = [nom, cognom1, cognom2].filter(x => x).join(' ') || '___________________________';
    
    document.getElementById('nom-cognoms-consentiment').textContent = nomComplet;
}

function actualitzarLlocDataConsentiment() {
    const municipi = document.getElementById('municipi_lloc')?.value || '';
    const avui = new Date().toLocaleDateString('ca-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const text = municipi ? `${municipi}, ${avui}` : `___________________________, ${avui}`;

    document.getElementById('lloc-data-consentiment').textContent = text;
}
