function mostrarFills() {
    const conjugeSelect = document.getElementById('conjuge_id');
    const seccioFills = document.getElementById('seccio-fills');
    
    if (!conjugeSelect.value) {
        seccioFills.style.display = 'none';
        return;
    }
    
    seccioFills.style.display = 'block';
    const conjugeId = parseInt(conjugeSelect.value);
    
    // Automarcar fills
    document.querySelectorAll('input[name="fills[]"]').forEach(checkbox => {
        const pareId = parseInt(checkbox.dataset.pare) || null;
        const mareId = parseInt(checkbox.dataset.mare) || null;
        
        if ((pareId === window.membreId && mareId === conjugeId) || 
            (pareId === conjugeId && mareId === window.membreId)) {
            checkbox.checked = true;
        }
    });
}

function obrirModalMatrimoni() {
    document.getElementById('modalMatrimoni').classList.add('actiu');
    document.body.style.overflow = 'hidden';
}

function tancarModalMatrimoni() {
    document.getElementById('modalMatrimoni').classList.remove('actiu');
    document.body.style.overflow = 'auto';
}

function tancarModalSiFora(event) {
    if (event.target.id === 'modalMatrimoni') {
        tancarModalMatrimoni();
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        tancarModalMatrimoni();
    }
});