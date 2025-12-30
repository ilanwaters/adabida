// static/js/nova_entrada.js - Funcionalitat específica per nova entrada

document.addEventListener('DOMContentLoaded', function() {
    inicialitzaBlocsPlegables();
    inicialitzaFormulari();
    inicialitzaEliminacioArxius();
});

/**
 * Inicialitza els blocs plegables
 */
function inicialitzaBlocsPlegables() {
    // Tancar tots els blocs per defecte
    document.querySelectorAll(".bloc-plegable").forEach(bloc => {
        bloc.classList.add("tancat");
    });
}

/**
 * Funcions dels blocs plegables
 */
window.toggleBloc = function(element) {
    const bloc = element.parentElement;
    bloc.classList.toggle('tancat');
};

/**
 * Inicialitza funcionalitat del formulari
 */
function inicialitzaFormulari() {
    // Preparar acció del formulari per edició
    window.preparaAccioFormulari = function(formulari) {
        const idEntrada = formulari.querySelector('input[name="entrada_id"]');
        if (idEntrada) {
            formulari.action = `/actualitzar_entrada/${idEntrada.value}`;
        }
        return true;
    };
}

/**
 * Confirmació per eliminar arxius
 */
function inicialitzaEliminacioArxius() {
    const botoEliminar = document.querySelector('button[name="accio"][value="eliminar_arxius"]');
    if (botoEliminar) {
        botoEliminar.addEventListener("click", function(e) {
            const missatge = botoEliminar.getAttribute('data-confirm-message') || 
                           "Segur que vols eliminar els arxius seleccionats?";
            const confirmat = confirm(missatge);
            if (!confirmat) {
                e.preventDefault();
            }
        });
    }
}

/**
 * Funcions globals per la pàgina nova entrada
 */
window.confirmaAccio = function(missatge) {
    return confirm(missatge || 'Segur que vols continuar?');
};