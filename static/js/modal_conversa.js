function obreModalConversa(conversaId, usuariLogin) {
    fetch(`/converses/api/conversa/${conversaId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('modal-conversa-titol').innerText = data.titol || '—';
            document.getElementById('modal-conversa-tema').innerText = data.tema || '—';
            document.getElementById('modal-conversa-participant').innerText = data.participant_nom || '—';
            document.getElementById('modal-conversa-data').innerText = data.data_conversa || '—';
            document.getElementById('modal-conversa-lloc').innerText = data.lloc || '—';
            document.getElementById('modal-conversa-durada').innerText = data.durada_minuts || '—';
            document.getElementById('modal-conversa-contingut').innerText = data.contingut || '—';
            
            const autorSpan = document.getElementById('modal-conversa-autor');
            if (autorSpan && data.usuari_nom && data.usuari_login) {
                autorSpan.innerHTML = `<a href="/perfil/${data.usuari_login}" class="enllac-perfil" target="_blank">${data.usuari_nom}</a>`;
            }
            
        
            // Mostrar metodologia només si l'entrevistador ho permet I l'usuari està loguejat
            const metodologiaDiv = document.getElementById('modal-conversa-metodologia');
            const usuariLogat = document.body.dataset.usuari !== '';

            if (data.notes_metodologiques_publiques && usuariLogat && (data.notes_preparacio || data.notes_camp || data.observacions_post)) {
                document.getElementById('modal-conversa-notes-prep').innerText = data.notes_preparacio || '—';
                document.getElementById('modal-conversa-notes-camp').innerText = data.notes_camp || '—';
                document.getElementById('modal-conversa-obs-post').innerText = data.observacions_post || '—';
                metodologiaDiv.style.display = 'block';
            } else {
                metodologiaDiv.style.display = 'none';
            }
            // Gestionar botons segons usuari
            const usuariActual = document.body.dataset.usuari;
            const botoGuardar = document.getElementById('boto-guardar-conversa');
            const botoEliminarGuardada = document.getElementById('boto-eliminar-guardada-conversa');
            const botoEditar = document.getElementById('boto-editar-conversa');

            if (usuariLogat) {
                botoGuardar.style.display = 'inline-block';
                
                // Si és el creador, mostrar botó editar
                if (usuariActual === data.usuari_login) {
                    botoEditar.style.display = 'inline-block';
                    botoEditar.onclick = () => window.location.href = `/converses/${data.id}/editar_adabida`;
                }
            }
            document.getElementById('modal-conversa').style.display = 'flex';
        })
        .catch(err => {
            console.error('Error carregant conversa:', err);
            alert('Error carregant la conversa');
        });
}

function tancaModalConversa() {
    document.getElementById('modal-conversa').style.display = 'none';
}