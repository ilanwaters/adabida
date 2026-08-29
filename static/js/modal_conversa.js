function mostraSiTeValor(idSpan, valor, formatador = (v) => v) {
    const span = document.getElementById(idSpan);
    const linia = span.closest('p');
    if (valor) {
        span.innerText = formatador(valor);
        if (linia) linia.style.display = '';
    } else {
        if (linia) linia.style.display = 'none';
    }
}

function obreModalConversa(conversaId, usuariLogin) {
    const T = window.TRAD_MODAL_CONVERSA || {};

    fetch(`/converses/api/conversa/${conversaId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('modal-conversa-titol').innerText = data.titol || '—';

            mostraSiTeValor('modal-conversa-tema', data.tema);

            const partsRealitzada = [];
            if (data.lloc) partsRealitzada.push(`${T.a || 'a'} ${data.lloc}`);
            if (data.data_conversa) partsRealitzada.push(`${T.elDia || 'el dia'} ${data.data_conversa}`);
            document.getElementById('modal-conversa-realitzada-format').innerText =
                partsRealitzada.length ? `, ${T.realitzada || 'realitzada'} ${partsRealitzada.join(', ')}` : '';

            mostraSiTeValor('modal-conversa-durada', data.durada_minuts);

            mostraSiTeValor('modal-conversa-contingut', data.contingut);

            const nomComplet = [data.participant_nom, data.participant_cognoms].filter(Boolean).join(' ');
            const detalls = [data.participant_lloc, data.participant_data_naixement].filter(Boolean).join(', ');
            document.getElementById('modal-conversa-entrevistat-format').innerText =
                detalls ? `${nomComplet} (${detalls})` : nomComplet || '—';

            mostraSiTeValor('modal-conversa-observacions-generals', data.observacions_generals);

            const autorSpan = document.getElementById('modal-conversa-autor');
            if (autorSpan && data.usuari_nom && data.usuari_login) {
                autorSpan.innerHTML = `<a href="/perfil/${data.usuari_login}" class="enllac-perfil" target="_blank">${data.usuari_nom}</a>`;
            }
            document.getElementById('modal-conversa-meta-creacio').innerText = data.data_creacio ? `${T.creat || 'Creat'}: ${data.data_creacio}` : '';
            document.getElementById('modal-conversa-meta-modificacio').innerText = data.data_modificacio ? `${T.modificat || 'Modificat'}: ${data.data_modificacio}` : '';

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
            const botoEditar = document.getElementById('boto-editar-conversa');
            const botoEliminar = document.getElementById('boto-eliminar-conversa');

            if (usuariLogat) {
                if (usuariActual === data.usuari_login) {
                    botoEditar.style.display = 'inline-block';
                    botoEditar.href = `/converses/${data.id}/editar_adabida`;

                    botoEliminar.style.display = 'inline-block';
                    botoEliminar.dataset.id = data.id;
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
            alert(T.errorCarregant || 'Error carregant la conversa');
        });
}

function tancaModalConversa() {
    document.getElementById('modal-conversa').style.display = 'none';
}

window.toggleBlocModalText = function(element) {
  const contingut = element.nextElementSibling;
  const obert = contingut.style.display === "block";
  contingut.style.display = obert ? "none" : "block";
};

window.confirmaEliminacioConversa = function() {
  const T = window.TRAD_MODAL_CONVERSA || {};
  if (confirm(T.confirmaEliminarConversa || "Segur que vols eliminar aquesta conversa?")) {
    const id = document.getElementById("boto-eliminar-conversa").dataset.id;
    fetch(`/converses/${id}/eliminar_adabida`, { method: "POST" })
      .then(res => {
        if (res.ok) {
          alert(T.conversaEliminada || "Conversa eliminada correctament.");
          window.location.href = "/pagina_personal";
        } else {
          res.text().then(msg => {
            console.error("Error:", msg);
            alert((T.errorEliminantConversa || "No s'ha pogut eliminar") + ":\n" + msg);
          });
        }
      });
  }
};

