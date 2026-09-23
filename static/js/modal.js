// static/js/modal.js

function obreModal(entradaId, usuariId,origen = null) {
  fetch(`/api/entrada/${usuariId}/${entradaId}`)
    .then(res => res.json())
    .then(data => {
      window.entradaIdActual = data.id;

      document.getElementById('modal-titol').innerText = data.titol || "—";

      const any = data.any?.trim();
      const ubicacio = [data.municipi, data.regio, data.pais].filter(Boolean).join(", ");
      const tema = data.tema?.trim();

      let parentesi = [ubicacio, any].filter(Boolean).join(", ");
      parentesi = parentesi ? ` (${parentesi})` : "";

      document.getElementById('modal-tema').innerText = tema || "";
      document.getElementById("modal-ubicacio-any-parentesi").textContent = parentesi;

      const dataSpan = document.getElementById('modal-data');
      if (dataSpan) dataSpan.innerText = data.data_creacio || "";

      const metaAutor = document.getElementById('modal-meta-autor');

      const metaCreacio = document.getElementById('modal-meta-creacio');
      if (metaCreacio) metaCreacio.textContent = data.data_creacio ? `Creat: ${data.data_creacio}` : '';

      const metaModificacio = document.getElementById('modal-meta-modificacio');
      if (metaModificacio) metaModificacio.textContent = data.data_modificacio ? `Modificat: ${data.data_modificacio}` : '';
      
console.log("DEBUG data.usuari_nom:", data.usuari_nom);
console.log("DEBUG data.usuari_login:", data.usuari_login);

if (metaAutor && data.usuari_nom && data.usuari_login) {
  metaAutor.innerHTML = `<a href="/perfil/${data.usuari_login}" class="enllac-perfil" target="_blank">${data.usuari_nom}</a>`;
} else if (metaAutor) {
  metaAutor.textContent = data.usuari_nom || '';
}

      document.getElementById('modal-contingut').innerHTML = data.contingut || "";

            const imatgesDiv = document.getElementById('modal-arxius-imatges');
      const mediaDiv = document.getElementById('modal-arxius-media');
      const comptadorMedia = document.getElementById('comptador-media');
      imatgesDiv.innerHTML = "";
      mediaDiv.innerHTML = "";
      let totalMedia = 0;

      const arxiusConversa = [];
      const comptadorsTipus = {};
      function etiquetaArxiu(fitxer) {
        let tipusEtiqueta;
        if (fitxer.tipus === "webm" && fitxer.tipus_media === "video") {
          tipusEtiqueta = "Vídeo";
        } else if (fitxer.tipus === "webm" && fitxer.tipus_media === "audio") {
          tipusEtiqueta = "Àudio";
        } else {
          tipusEtiqueta = "Document";
        }
        comptadorsTipus[tipusEtiqueta] = (comptadorsTipus[tipusEtiqueta] || 0) + 1;
        const titolEntrada = (data.titol || "").trim();
        return titolEntrada ? `${titolEntrada} · ${tipusEtiqueta} ${comptadorsTipus[tipusEtiqueta]}` : `${tipusEtiqueta} ${comptadorsTipus[tipusEtiqueta]}`;
      }
      data.arxius.forEach(fitxer => {
        if (fitxer.es_conversa) {
          arxiusConversa.push(fitxer);
          return;
        }
        const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;
        const link = document.createElement("a");
        link.href = ruta;
        link.target = "_blank";

        const contenidor = document.createElement("div");
        contenidor.classList.add("arxiu-miniatura-peu");

        if (fitxer.tipus.match(/(jpg|png|jpeg|webp)/i)) {
          link.setAttribute("data-lightbox", "galeria-" + data.id);
          link.setAttribute("data-title", construeixPeuLightbox(fitxer));

          const img = document.createElement("img");
          img.src = ruta;
          img.style.maxWidth = "100px";
          img.style.margin = "10px";

          link.appendChild(img);
          contenidor.appendChild(link);

          const peu = document.createElement("p");
          peu.classList.add("peu-curt-arxiu");
          peu.textContent = fitxer.titol || "";
          contenidor.appendChild(peu);

          imatgesDiv.appendChild(contenidor);
                } else if (fitxer.tipus === "webm" && fitxer.tipus_media === "audio") {
          const audio = document.createElement("audio");
          audio.controls = true;
          audio.src = ruta;
          audio.style.width = "250px";
          audio.style.minWidth = "250px";
          contenidor.appendChild(audio);

          const peu = document.createElement("p");
          peu.classList.add("peu-complet-arxiu");
          peu.textContent = construeixPeuLightbox(fitxer) || etiquetaArxiu(fitxer);
          contenidor.appendChild(peu);

          mediaDiv.appendChild(contenidor);
          totalMedia++;
        } else {
          const icona = document.createElement("img");
          let iconaPath;
          if (fitxer.tipus === "webm" && fitxer.tipus_media === "video") {
            iconaPath = `/umberto/${data.usuari_login}/${data.id}/mini/${fitxer.nom_fitxer}.png`;
            icona.onerror = () => { icona.onerror = null; icona.src = "/static/icons/video_webm.png"; };
          } else if (fitxer.tipus === "webm" && fitxer.tipus_media) {
            iconaPath = "/static/icons/webm.png";
          } else {
            iconaPath = `/static/icons/${fitxer.tipus}.png`;
          }
          icona.src = iconaPath;
          icona.title = fitxer.nom_fitxer;
          icona.style.maxWidth = "40px";
          icona.style.margin = "10px";
          link.appendChild(icona);
          contenidor.appendChild(link);

          const peu = document.createElement("p");
          peu.classList.add("peu-complet-arxiu");
          peu.textContent = construeixPeuLightbox(fitxer) || etiquetaArxiu(fitxer);
          contenidor.appendChild(peu);

          mediaDiv.appendChild(contenidor);
          totalMedia++;
        }
      });

      comptadorMedia.textContent = totalMedia > 0 ? `(${totalMedia})` : "";
   // Buscar la millor imatge principal per mostrar
let arxiuPrincipal = null;

// 0. Prioritat màxima: portada triada per l'usuari
if (data.portada) {
  arxiuPrincipal = data.portada;
} else {
  // 1. Prioritat: cercar una imatge real
  for (const fitxer of data.arxius) {
    if (fitxer.tipus.match(/(jpg|png|jpeg|webp|gif)/i)) {
      arxiuPrincipal = fitxer;
      break;
    }
  }

  // 2. Si no hi ha imatge, agafar el primer arxiu (vídeo, àudio, etc.)
  if (!arxiuPrincipal && data.arxius.length > 0) {
    arxiuPrincipal = data.arxius[0];
  }
}

// Mostrar la imatge principal
if (arxiuPrincipal) {
  const url = `/umberto/${data.usuari_login}/${data.id}/${arxiuPrincipal.nom_fitxer}`;
  const img = document.getElementById('modal-img');
  
  if (arxiuPrincipal.tipus.match(/(jpg|png|jpeg|webp|gif)/i)) {
    // És imatge - mostrar la imatge real
    img.src = url;
    } else {
    // És àudio/vídeo/document - mostrar la icona gran
    if (arxiuPrincipal.tipus === "webm" && arxiuPrincipal.tipus_media === "video") {
      img.onerror = () => { img.onerror = null; img.src = "/static/icons/video_webm.png"; };
      img.src = `/umberto/${data.usuari_login}/${data.id}/mini/${arxiuPrincipal.nom_fitxer}.png`;
    } else if (arxiuPrincipal.tipus === "webm" && arxiuPrincipal.tipus_media) {
      if (arxiuPrincipal.tipus_media === "audio") {
        img.src = "/static/icons/audio_webm.png";
      } else {
        img.src = "/static/icons/webm.png";
      }
    } else {
      img.src = `/static/icons/${arxiuPrincipal.tipus}.png`;
    }
  }
  
  img.style.maxWidth = "400px";
  img.style.height = "auto";
  document.getElementById('modal-enllac').href = url;
} else {
  // No hi ha cap arxiu
  document.getElementById('modal-img').src = "/static/icons/sense_imatge.png";
}
    
            // Bloc conversa vinculada
                    // Bloc conversa vinculada
        const blocConversa = document.getElementById("modal-conversa-bloc");
        if (data.conversa) {
        const c = data.conversa;
        const lloc = [c.lloc_municipi, c.lloc_regio].filter(Boolean).join(", ");
      

        const nomsParticipants = c.participants.map(p => {
        const nomComplet = [p.nom, p.primer_cognom, p.segon_cognom].filter(Boolean).join(" ");
        const naixement = [p.lloc_municipi, p.lloc_regio, p.data_naixement].filter(Boolean).join(", ");
        return naixement ? `${nomComplet} (${naixement})` : nomComplet;
      }).join(" i ");

      let realitzada = "";
      if (lloc && c.data) {
        realitzada = ` realitzada a ${lloc} el ${c.data}`;
      } else if (lloc) {
        realitzada = ` realitzada a ${lloc}`;
      } else if (c.data) {
        realitzada = ` realitzada el ${c.data}`;
      }

          document.getElementById("modal-conversa-resum").textContent = (nomsParticipants ? `Conversa amb ${nomsParticipants}` : "Conversa") + realitzada || "—";
          document.getElementById("modal-conversa-observacions").textContent = c.observacions_generals || "";

          const conversaArxiusDiv = document.getElementById("modal-conversa-arxius");
          conversaArxiusDiv.innerHTML = "";
          arxiusConversa.forEach(fitxer => {
            const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;

            const link = document.createElement("a");
            link.href = ruta;
            link.target = "_blank";

            const contenidor = document.createElement("div");
            contenidor.classList.add("arxiu-miniatura-peu");

                        if (fitxer.tipus_media === "video") {
              const miniatura = `/umberto/${data.usuari_login}/${data.id}/mini/${fitxer.nom_fitxer}.png`;
              const img = document.createElement("img");
              img.src = miniatura;
              img.style.width = "100%";
              img.style.maxHeight = "80px";
              img.style.objectFit = "cover";
              img.onerror = () => { img.src = "/static/icons/video_webm.png"; img.style.objectFit = "contain"; };
              link.appendChild(img);
              contenidor.appendChild(link);
            } else {
              const audio = document.createElement("audio");
              audio.controls = true;
              audio.src = ruta;
              audio.style.width = "260px";
              contenidor.style.width = "260px";
              contenidor.appendChild(audio);
            }
          

            const peu = document.createElement("p");
            peu.classList.add("peu-curt-arxiu");
            peu.textContent = fitxer.titol || "";
            contenidor.appendChild(peu);

            conversaArxiusDiv.appendChild(contenidor);
          });

          blocConversa.style.display = "block";
          document.getElementById("modal-conversa-contingut").style.display = "none";
          document.getElementById("modal-conversa-fletxa").textContent = "▶";
        } else {
          blocConversa.style.display = "none";
        }

      // 🔁 Mostra o amaga botons segons l’origen
// 🔁 Reinicia estat botons abans de mostrar la modal
// 🔁 Reinicia estat botons abans de mostrar la modal
const botoGuardar = document.getElementById("boto-guardar");
const botoEliminar = document.getElementById("boto-eliminar-guardada");

if (botoGuardar) {
  botoGuardar.disabled = false;
  botoGuardar.textContent = "Guardar";
}

// 🔁 Decideix quin botó mostrar segons si ja estava guardada
if (data.ja_guardada) {
  if (botoGuardar) botoGuardar.style.display = "none";
  if (botoEliminar) botoEliminar.style.display = "inline-block";
} else {
  if (botoGuardar) botoGuardar.style.display = "inline-block";
  if (botoEliminar) botoEliminar.style.display = "none";
}



      document.getElementById("modal-entrada").style.display = "flex";
    });
}

function tancaModalEntrada() {
  document.getElementById("modal-entrada").style.display = "none";
}
function guardaEntradaFavorita() {
  const entradaId = window.entradaIdActual;

  fetch(`/api/guardar_entrada/${entradaId}`, {
    method: "POST"
  })
    .then(res => {
      if (res.ok) {
        alert("✅ Entrada guardada com a favorit!");
        const boto = document.getElementById("boto-guardar");
        if (boto) {
          boto.disabled = true;
          boto.textContent = "✅ Guardada";
        }
      } else {
        alert("❌ No s'ha pogut guardar.");
      }
    })
    .catch(err => {
      console.error("Error en guardar entrada:", err);
      alert("⚠️ Error del servidor.");
    });
}

function eliminaEntradaGuardada() {
  const entradaId = window.entradaIdActual;

  fetch(`/api/eliminar_entrada_guardada/${entradaId}`, {
    method: "POST"
  })
    .then(res => {
      if (res.ok) {
        alert("❌ Entrada eliminada dels guardats.");
        document.getElementById("modal-entrada").style.display = "none";
        // Opcional: tornar a carregar la llista de guardades
        if (typeof carregaEntradesGuardades === "function") {
          carregaEntradesGuardades(document.body.dataset.usuari);
        }
      } else {
        alert("⚠️ No s’ha pogut eliminar.");
      }
    })
    .catch(err => {
      console.error("Error eliminant entrada:", err);
      alert("❌ Error del servidor.");
    });
}

function tancaModal() {
  document.getElementById("modal-entrada").style.display = "none";
}


// Aquesta funció assigna esdeveniment a tots els botons de tancar modal
function activaTancarModals() {
  const botonsTancar = document.querySelectorAll('.boto-tancar');
  botonsTancar.forEach(boto => {
    boto.addEventListener('click', () => {
      const modal = boto.closest('.modal');
      if (modal) modal.style.display = 'none';
    });
  });
}

// Crida inicial (per si les modals ja existeixen)
document.addEventListener('DOMContentLoaded', () => {
  activaTancarModals();
});

function toggleConversaModal() {
  const contingut = document.getElementById("modal-conversa-contingut");
  const arxius = document.getElementById("modal-conversa-arxius");
  const fletxa = document.getElementById("modal-conversa-fletxa");
  const obert = contingut.style.display === "block";
  contingut.style.display = obert ? "none" : "block";
  if (arxius) arxius.style.display = obert ? "none" : "grid";
  fletxa.textContent = obert ? "▶" : "▼";
}

function construeixPeuLightbox(fitxer) {
  const parts = [];
  if (fitxer.titol) parts.push(fitxer.titol);

  const ubicacio = [fitxer.municipi, fitxer.regio, fitxer.pais].filter(Boolean).join(", ");
  const anyUbicacio = [ubicacio, fitxer.any_arxiu].filter(Boolean).join(", ");
  if (anyUbicacio) parts.push(anyUbicacio);

  if (fitxer.descripcio) parts.push(fitxer.descripcio);
  if (fitxer.referencia) parts.push(`Consulta: ${fitxer.referencia}`);

  return parts.join(" — ");
}

function toggleBlocModal(element) {
  const contingut = element.nextElementSibling;
  const obert = contingut.style.display === "grid";
  contingut.style.display = obert ? "none" : "grid";
}