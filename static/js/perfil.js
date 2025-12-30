// static/js/perfil.js - Funcionalitat específica per la pàgina de perfil

document.addEventListener('DOMContentLoaded', function() {
    inicialitzaBlocsPlegables();
    inicialitzaMissatges();
});

/**
 * Inicialitza els blocs plegables
 */
function inicialitzaBlocsPlegables() {
    // Tancar tots els blocs per defecte
    document.querySelectorAll(".bloc-plegable").forEach(bloc => {
        bloc.classList.add("tancat");
    });

    // Obre el bloc de "Missatges" si es passa ?obrir=missatges per URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("obrir") === "missatges") {
        const bloc = document.querySelector('.bloc-plegable');
        if (bloc && bloc.classList.contains('tancat')) {
            toggleBloc(bloc.querySelector(".titol-plegable"));
        }
    }
}

window.toggleBloc = function(element) {
    const bloc = element.parentElement;
    bloc.classList.toggle('tancat');
};

function inicialitzaMissatges() {
    // La funcionalitat de missatges està disponible globalment
    // No cal inicialitzar res especial aquí
}

window.canviaBustia = function(quina) {
    const rebuts = document.getElementById("bustia-rebuts");
    const enviats = document.getElementById("bustia-enviats");
    const pestanyes = document.querySelectorAll(".pestanya-bustia");
    
    if (!rebuts || !enviats) return;
    
    pestanyes.forEach(p => p.classList.remove("activa"));

    if (quina === "rebuts") {
        rebuts.style.display = "block";
        enviats.style.display = "none";
        pestanyes[0]?.classList.add("activa");
    } else {
        rebuts.style.display = "none";
        enviats.style.display = "block";
        pestanyes[1]?.classList.add("activa");
    }
};

/**
 * Funció global per obrir modal de missatge
 * (aquesta funció està definida a modal_missatge.js)
 */
window.obreMissatge = window.obreMissatge || function(missatgeId) {
    console.log('Obrint missatge ID:', missatgeId);
    // La implementació real està a modal_missatge.js
};