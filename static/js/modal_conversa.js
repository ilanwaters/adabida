function obreModalConversa(conversaId, usuariLogin) {
    fetch(`/converses/api/conversa/${conversaId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('modal-conversa-titol').innerText = data.titol || '—';
            document.getElementById('modal-conversa-tema').innerText = data.tema || '—';
            document.getElementById('modal-conversa-lloc-data').innerText =
                [data.lloc, data.data_conversa].filter(Boolean).join(' · ');
            document.getElementById('modal-conversa-durada').innerText = data.durada_minuts || '—';
            document.getElementById('modal-conversa-contingut').innerText = data.contingut || '—';
            const nomComplet = [data.participant_nom, data.participant_cognoms].filter(Boolean).join(' ');
            const detalls = [data.participant_lloc, data.participant_data_naixement].filter(Boolean).join(', ');
            document.getElementById('modal-conversa-entrevistat-format').innerText =
                detalls ? `${nomComplet} (${detalls})` : nomComplet || '—';
            document.getElementById('modal-conversa-observacions-generals').innerText = data.observacions_generals || '—';
            const autorSpan = document.getElementById('modal-conversa-autor');
            if (autorSpan && data.usuari_nom && data.usuari_login) {
                autorSpan.innerHTML = `<a href="/perfil/${data.usuari_login}" class="enllac-perfil" target="_blank">${data.usuari_nom}</a>`;
            }

            // Metodologia: bloc plegable, es mostra només si l'entrevistador ho permet i l'usuari està loguejat
            const metodologiaBloc = document.getElementById('modal-conversa-metodologia');
            const usuariLogat = document.body.dataset.usuari !== '';

            if (data.notes_metodologiques_publiques && usuariLogat && (data.notes_preparacio || data.notes_camp || data.observacions_post)) {
                document.getElementById('modal-conversa-notes-prep').innerText = data.notes_preparacio || '—';
                document.getElementById('modal-conversa-notes-camp').innerText = data.notes_camp || '—';
                document.getElementById('modal-conversa-obs-post').innerText = data.observacions_post || '—';
                metodologiaBloc.style.display = 'block';
                metodologiaBloc.querySelector('.contingut-plegable-modal').style.display = 'none';
            } else {
                metodologiaBloc.style.display = 'none';
            }

            // Botons segons usuari
            const usuariActual = document.body.dataset.usuari;
            const botoGuardar = document.getElementById('boto-guardar-conversa');
            const botoEditar = document.getElementById('boto-editar-conversa');

            if (usuariLogat) {
                botoGuardar.style.display = 'inline-block';
                if (usuariActual === data.usuari_login) {
                    botoEditar.style.display = 'inline-block';
                    botoEditar.onclick = () => window.location.href = `/converses/${data.id}/editar_adabida`;
                }
            }

            // Arxius: imatges en graella, resta (àudio/vídeo/documents) al bloc plegable
            const graellaDiv = document.getElementById('modal-conversa-arxius-imatges');
            const mediaDiv = document.getElementById('modal-conversa-arxius-media');
            const comptadorSpan = document.getElementById('modal-conversa-comptador-media');
            graellaDiv.innerHTML = '';
            mediaDiv.innerHTML = '';

            if (data.arxius && data.arxius.length > 0 && data.entrada_id) {
                let comptadorMedia = 0;

                data.arxius.forEach(fitxer => {
                    const ruta = `/umberto/${data.usuari_login}/${data.entrada_id}/${fitxer.nom_fitxer}`;

                    if (fitxer.tipus_media === 'imatge') {
                        graellaDiv.insertAdjacentHTML('beforeend',
                            `<div class="arxiu-miniatura-peu">
                                <a href="${ruta}" target="_blank"><img src="${ruta}" alt="${fitxer.nom_fitxer}"></a>
                             </div>`);
                    } else if (fitxer.tipus_media === 'audio') {
                        mediaDiv.insertAdjacentHTML('beforeend',
                            `<audio controls src="${ruta}" style="width:100%; margin-bottom:10px;"></audio>`);
                        comptadorMedia++;
                    } else if (fitxer.tipus_media === 'video') {
                        mediaDiv.insertAdjacentHTML('beforeend',
                            `<video controls src="${ruta}" style="width:100%; margin-bottom:10px;"></video>`);
                        comptadorMedia++;
                    } else {
                        mediaDiv.insertAdjacentHTML('beforeend',
                            `<a href="${ruta}" target="_blank" style="display:block; margin-bottom:10px;">📎 ${fitxer.nom_fitxer}</a>`);
                        comptadorMedia++;
                    }
                });

                comptadorSpan.textContent = comptadorMedia > 0 ? `(${comptadorMedia})` : '';
            } else {
                comptadorSpan.textContent = '';
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